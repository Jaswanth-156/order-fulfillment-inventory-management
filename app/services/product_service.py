from sqlalchemy.orm import Session

from app.models import product
from app.models.product import Product
from app.repositories import product_repository

def create_product(
        db:Session,
        sku:str,
        name:str,
        description:str|None,
        category_id:int,
        price,
        cost_price,
):
    existing_product=product_repository.get_product_by_sku(db,sku)

    if existing_product:
        raise ValueError("SKU already exists")

    product = Product(
        sku=sku,
        name=name,
        description=description,
        category_id=category_id,
        price=price,
        cost_price=cost_price
    )

    return product_repository.create_product(db,product)

def get_products(db:Session):
    return product_repository.get_products(db)

def get_product(db: Session, product_id: int):
    product = product_repository.get_product_by_id(db, product_id)

    if not product:
        raise ValueError("Product not found")

    return product


def update_product(
    db: Session,
    product_id: int,
    name: str | None = None,
    description: str | None = None,
    category_id: int | None = None,
    price=None,
    cost_price=None,
):
    product = product_repository.get_product_by_id(db, product_id)

    if not product:
        raise ValueError("Product not found")

    if name is not None:
        product.name = name

    if description is not None:
        product.description = description

    if category_id is not None:
        product.category_id = category_id

    if price is not None:
        product.price = price

    if cost_price is not None:
        product.cost_price = cost_price

    return product_repository.update_product(db, product)


def activate_product(db: Session, product_id: int):
    product = product_repository.get_product_by_id(db, product_id)

    if not product:
        raise ValueError("Product not found")

    product.is_active = True

    return product_repository.update_product(db, product)


def deactivate_product(db: Session, product_id: int):
    product = product_repository.get_product_by_id(db, product_id)

    if not product:
        raise ValueError("Product not found")

    product.is_active = False

    return product_repository.update_product(db, product)