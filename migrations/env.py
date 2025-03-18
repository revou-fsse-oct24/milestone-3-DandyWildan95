from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your app and models
from src.app import create_app
from src.models.base import db
from src.models.user import User
from src.models.account import Account
from src.models.transaction import Transaction

# Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here
target_metadata = db.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    app = create_app()
    with app.app_context():
        url = app.config.get('SQLALCHEMY_DATABASE_URI')
        context.configure(
            url=url,
            target_metadata=target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
        )

        with context.begin_transaction():
            context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    app = create_app()
    with app.app_context():
        connectable = engine_from_config(
            app.config,
            prefix="SQLALCHEMY_",
            poolclass=pool.NullPool,
        )

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