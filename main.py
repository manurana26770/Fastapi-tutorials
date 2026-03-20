from fastapi import FastAPI
from models import Products
from pydantic import BaseModel
from database import session, engine
import database_models

from sqlalchemy.orm import Session
from fastapi import Depends
app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "Hello, World!"

products = [
    Products(id=1,name="phone", description="budget phone", price=20000, quantity=4),
    Products(id=2, name="laptop", description="gaming laptop", price=99999, quantity=10),
    Products(id=3,name="pen", description="pilot fountain pen", price=1000, quantity=9),
    Products(id=4, name="table lamp", description="Emits reading light and white light", price=1500, quantity=10),
    Products(id=5,name="earphones", description="oppo enco buds", price=5000, quantity=4),
    Products(id=6, name="dairy", description="google developer cloud diary", price=2000, quantity=10)
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()
    count = db.query(database_models.Products).count()
    
    if count == 0:
        for product in products:
            db.add(database_models.Products(id=product.id, name=product.name, description=product.description, price=product.price, quantity=product.quantity))
        db.commit() 
    
init_db()
    
    
@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Products).all()
    return db_products 
    
    
@app.get("/product/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Products).filter(database_models.Products.id == id).first()
    if db_product:
        return db_product
    return "product not found"


@app.post("/product")
def add_product(product: Products, db: Session = Depends(get_db)):
    db.add(database_models.Products(id=product.id, name=product.name, description=product.description, price=product.price, quantity=product.quantity))
    db.commit()
    return product


@app.put("/products/{id}")
def update_products(id:int, updated_product: Products, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Products).filter(database_models.Products.id == id).first()
    if db_product:
        db_product.name = updated_product.name
        db_product.description = updated_product.description
        db_product.price = updated_product.price
        db_product.quantity = updated_product.quantity
        db.commit()
        return db_product
    return "product not found"


@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Products).filter(database_models.Products.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "product deleted"
    return "product not found"