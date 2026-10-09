from sqlalchemy.orm import Session
from app.models.product import Product

def create_product(db:Session,product:Product):
    db.add(product)
    db.commit()
    db.refresh(product)

    return product

def get_products(db:Session):
    return db.query(Product).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_product_by_sku(db:Session,sku:str):
    return db.query(Product).filter(Product.sku==sku).first()

def update_product(db:Session,product:Product):
    db.commit()
    db.refresh(product)

    return product