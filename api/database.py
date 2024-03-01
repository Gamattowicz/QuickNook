import databases
import sqlalchemy
from sqlalchemy.sql import func

from api.config import config
from api.models.user import UserRole

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
    sqlalchemy.Column("price", sqlalchemy.String),
    sqlalchemy.Column(
        "category_id", sqlalchemy.ForeignKey("categories.id"), nullable=False
    ),
    sqlalchemy.Column("image", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("thumbnail", sqlalchemy.String, nullable=True),
)

order_table = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("delivery_address", sqlalchemy.String),
    sqlalchemy.Column("order_date", sqlalchemy.DateTime, default=func.now()),
    sqlalchemy.Column("payment_due_date", sqlalchemy.DateTime),
    sqlalchemy.Column("total_price", sqlalchemy.String),
    sqlalchemy.Column("customer_id", sqlalchemy.ForeignKey("users.id"), nullable=False),
)

order_item_table = sqlalchemy.Table(
    "order_items",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("order_id", sqlalchemy.ForeignKey("orders.id"), nullable=False),
    sqlalchemy.Column(
        "product_id", sqlalchemy.ForeignKey("products.id"), nullable=False
    ),
    sqlalchemy.Column("quantity", sqlalchemy.Integer),
)

user_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("confirmed", sqlalchemy.Boolean, default=False),
    sqlalchemy.Column("role", sqlalchemy.String, default=UserRole.client.value),
)

engine = sqlalchemy.create_engine(
    config.DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)
database = databases.Database(
    config.DATABASE_URL, force_rollback=config.DB_FORCE_ROLL_BACK
)
