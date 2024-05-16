import os


def get_database_url() -> str:
    username = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")
    server = os.getenv("POSTGRES_SERVER", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "inzage-data")

    connection_string = f"postgresql://{username}:{password}@{server}:{port}/{db}"
    return connection_string
