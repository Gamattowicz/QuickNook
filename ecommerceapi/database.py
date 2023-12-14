import databases
import sqlalchemy

from ecommerceapi.config import config

metadata = sqlalchemy.MetaData()

category_table = sqlalchemy.Table(
    "categories",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
)

product_table = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("price", sqlalchemy.Integer),
    sqlalchemy.Column(
        "category_id", sqlalchemy.ForeignKey("categories.id"), nullable=False
    ),
)

user_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("confirmed", sqlalchemy.Boolean, default=False),
)

engine = sqlalchemy.create_engine(
    config.DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)
database = databases.Database(
    config.DATABASE_URL, force_rollback=config.DB_FORCE_ROLL_BACK
)
