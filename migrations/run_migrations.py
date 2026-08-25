import os
from pathlib import Path
from app.database.postgres_client import get_postgres_connection

MIGRATIONS_DIR = Path(__file__).parent


def ensure_migrations_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            filename VARCHAR(255) PRIMARY KEY,
            applied_at TIMESTAMP DEFAULT NOW()
        );
    """)


def get_applied_migrations(cursor):
    cursor.execute("SELECT filename FROM schema_migrations;")
    return {row[0] for row in cursor.fetchall()}


def run_migrations():
    conn = get_postgres_connection()
    conn.autocommit = False
    cursor = conn.cursor()

    try:
        ensure_migrations_table(cursor)
        conn.commit()

        applied = get_applied_migrations(cursor)

        sql_files = sorted(
            f for f in os.listdir(MIGRATIONS_DIR) if f.endswith(".sql")
        )

        for filename in sql_files:
            if filename in applied:
                print(f"SKIP  {filename} (already applied)")
                continue

            filepath = MIGRATIONS_DIR / filename
            sql = filepath.read_text()

            print(f"APPLY {filename}")
            cursor.execute(sql)
            cursor.execute(
                "INSERT INTO schema_migrations (filename) VALUES (%s);",
                (filename,),
            )
            conn.commit()

        print("Migrations complete.")

    except Exception as e:
        conn.rollback()
        print(f"Migration failed: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    run_migrations()