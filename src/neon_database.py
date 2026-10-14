"""Neon persistence. Dependencies are imported only when a URL is configured.

The fixed cardekho_lab schema isolates this assignment. Each source/policy
combination is one immutable batch. Repeating it verifies and reuses that
batch. No DROP, DELETE, TRUNCATE, or if_exists='replace' is used.
"""
import hashlib
import os

SCHEMA = "cardekho_lab"

def create_neon_engine(project_root):
    # Return None for an unconfigured local-only run.
    from pathlib import Path
    env_file = Path(project_root) / ".env"
    try:
        from dotenv import load_dotenv
    except ImportError:
        if env_file.exists() or os.environ.get("DATABASE_URL"):
            raise RuntimeError("Install requirements.txt before enabling Neon.") from None
        return None
    load_dotenv(env_file, override=False)
    secret = os.environ.get("DATABASE_URL", "").strip()
    if not secret or "YOUR_" in secret:
        return None
    try:
        from sqlalchemy import create_engine
        from sqlalchemy.engine import make_url
        from sqlalchemy.pool import NullPool
        url = make_url(secret)
        if url.drivername not in ("postgres", "postgresql", "postgresql+psycopg2"):
            raise ValueError("Unsupported driver")
        if not url.host or not url.username or not url.database:
            raise ValueError("Incomplete URL")
        query = dict(url.query)
        if query.get("sslmode") not in ("require", "verify-ca", "verify-full"):
            query["sslmode"] = "require"
        url = url.set(drivername="postgresql+psycopg2", query=query)
        return create_engine(
            url, poolclass=NullPool, hide_parameters=True,
            connect_args={"connect_timeout": 15},
        )
    except Exception:
        raise RuntimeError(
            "Could not configure Neon. Install requirements.txt and check the "
            "PostgreSQL URL in .env. Do not print or share the URL."
        ) from None

def batch_id(source_sha256, policy_version):
    return hashlib.sha256((source_sha256 + ":" + policy_version).encode()).hexdigest()

def _metadata(raw, cleaned, audit):
    import pandas as pd
    from sqlalchemy import (
        MetaData, Table, Column, Text, BigInteger, Float, Boolean,
        ForeignKey, DateTime, func,
    )
    metadata = MetaData(schema=SCHEMA)
    runs = Table(
        "runs", metadata,
        Column("run_id", Text, primary_key=True),
        Column("source_sha256", Text, nullable=False),
        Column("policy_version", Text, nullable=False),
        Column("loaded_at", DateTime(timezone=True), server_default=func.now()),
        Column("raw_rows", BigInteger, nullable=False),
        Column("clean_rows", BigInteger, nullable=False),
        Column("audit_rows", BigInteger, nullable=False),
    )
    def frame_table(name, frame, key):
        columns = [Column("run_id", Text, ForeignKey(f"{SCHEMA}.runs.run_id"), primary_key=True)]
        for col in frame.columns:
            dtype = frame[col].dtype
            if pd.api.types.is_bool_dtype(dtype):
                sql_type = Boolean
            elif pd.api.types.is_integer_dtype(dtype):
                sql_type = BigInteger
            elif pd.api.types.is_numeric_dtype(dtype):
                sql_type = Float
            else:
                sql_type = Text
            columns.append(Column(col, sql_type, primary_key=(col == key)))
        return Table(name, metadata, *columns)
    return metadata, runs, {
        "raw_cars": frame_table("raw_cars", raw, "source_row"),
        "clean_cars": frame_table("clean_cars", cleaned, "source_row"),
        "cleaning_audit": frame_table("cleaning_audit", audit, "metric"),
    }

def upload_frames(engine, raw, cleaned, audit, source_sha256, policy_version):
    """Atomic upload and read-back counts; repeat runs do not duplicate data."""
    from sqlalchemy import text, select, func
    identifier = batch_id(source_sha256, policy_version)
    metadata, runs, tables = _metadata(raw, cleaned, audit)
    frames = {"raw_cars": raw, "clean_cars": cleaned, "cleaning_audit": audit}
    try:
        with engine.begin() as connection:
            # Serialize uploads from this project, including first-table creation.
            connection.execute(text("SELECT pg_advisory_xact_lock(4815162342)"))
            connection.execute(text("CREATE SCHEMA IF NOT EXISTS cardekho_lab"))
            metadata.create_all(connection)
            exists = connection.execute(
                select(runs.c.run_id).where(runs.c.run_id == identifier)
            ).scalar_one_or_none()
            if exists is None:
                connection.execute(runs.insert().values(
                    run_id=identifier, source_sha256=source_sha256,
                    policy_version=policy_version, raw_rows=len(raw),
                    clean_rows=len(cleaned), audit_rows=len(audit),
                ))
                for name, frame in frames.items():
                    payload = frame.copy()
                    payload.insert(0, "run_id", identifier)
                    payload.to_sql(
                        name, connection, schema=SCHEMA, if_exists="append",
                        index=False, method="multi", chunksize=200,
                    )
            verified = {}
            for name, frame in frames.items():
                table = tables[name]
                count = connection.execute(
                    select(func.count()).select_from(table).where(table.c.run_id == identifier)
                ).scalar_one()
                if count != len(frame):
                    raise ValueError("Stored row count does not match")
                verified[name] = count
        return identifier, "Uploaded" if exists is None else "Existing batch verified", verified
    except Exception:
        raise RuntimeError(
            "Neon upload or verification failed; the transaction was rolled back. "
            "Check connectivity, schema permissions, and installed dependencies. "
            "Existing tables with an incompatible structure require a new schema "
            "name or a deliberate migration. Do not share credentials."
        ) from None

def query_results(engine, run_id):
    """Read the stored cleaned data using bound query parameters."""
    import pandas as pd
    from sqlalchemy import text
    try:
        with engine.connect() as connection:
            preview = pd.read_sql_query(text(
                "SELECT source_row, brand, model, year, selling_price, engine_cc, "
                "max_power_bhp, fuel_economy_value, fuel_economy_unit "
                "FROM cardekho_lab.clean_cars WHERE run_id = :run_id "
                "ORDER BY source_row LIMIT 10"
            ), connection, params={"run_id": run_id})
            summary = pd.read_sql_query(text(
                "SELECT brand, COUNT(*) AS car_count, "
                "ROUND(AVG(selling_price)::numeric, 2) AS average_price_inr "
                "FROM cardekho_lab.clean_cars WHERE run_id = :run_id "
                "GROUP BY brand ORDER BY car_count DESC, brand LIMIT 10"
            ), connection, params={"run_id": run_id})
        return preview, summary
    except Exception:
        raise RuntimeError("Neon read-back failed. Check the connection and schema.") from None
