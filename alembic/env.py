from app.db import Base, engine
from logging.config import fileConfig
from alembic import context
from dotenv import load_dotenv
import app.models
from app.models.tournament import Tournament, Player
import os

load_dotenv()


config = context.config
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))
print(os.getenv("DATABASE_URL"))
if not os.getenv("DATABASE_URL"):
    raise ValueError("DATABASE_URL environment variable is not set")

fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()