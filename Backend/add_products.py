from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Product

# Assuming the database URL is set up correctly
DATABASE_URL = "sqlite:///./app.db"  # Change this to your actual database URL

def add_products():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Define products to add
    products = [
        Product(name="Branded T-shirt", category="Clothing", stock_level=10, reorder_threshold=20, price=15.99, supplier_id=1),
        Product(name="Mug", category="Kitchenware", stock_level=200, reorder_threshold=50, price=5.99, supplier_id=2),
        Product(name="Keychain", category="Accessories", stock_level=300, reorder_threshold=75, price=2.99, supplier_id=3),
        Product(name="Reusable Ice Cream Container", category="Kitchenware", stock_level=150, reorder_threshold=30, price=10.99, supplier_id=4),
    ]

    for product_data in products:
        existing_product = session.query(Product).filter_by(name=product_data.name).first()
        if not existing_product:
            try:
                #product = Product(**product_data)
                session.add(product_data)
                session.commit()
            except Exception as e:
                session.rollback()  # If any error occurs, rollback the session
                print(f"Error adding product {product_data.name}: {e}")

    session.close()

if __name__ == "__main__":
    add_products()
