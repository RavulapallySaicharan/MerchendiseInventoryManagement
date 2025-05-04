from database import get_session
from models import Product, Supplier, Batch, Role, User, ProductImage
from datetime import date

def add_admin_role():
    session = get_session()
    session.query(User).filter(User.username == "admin").update({"role_id": 1})
    session.commit()

def add_suppliers():
    session = get_session()

    suppliers = [
        Supplier(
            name="Rusthead Designs",
            contact_person="Rusthead Team",
            phone="000-000-0001",
            email="support@rusthead.com",
            address="https://rusthead.com"
        ),
        Supplier(
            name="Zazzle",
            contact_person="Zazzle Team",
            phone="000-000-0002",
            email="support@zazzle.com",
            address="https://www.zazzle.com"
        ),
        Supplier(
            name="Grandstand Glassware",
            contact_person="Grandstand Sales",
            phone="000-000-0003",
            email="info@egrandstand.com",
            address="https://egrandstand.com"
        ),
    ]

    for supplier in suppliers:
        existing_supplier = session.query(Supplier).filter_by(name=supplier.name).first()
        if not existing_supplier:
            session.add(supplier)

    session.commit()
    session.close()


def add_products():
    session = get_session()

    # Fetch supplier IDs by name
    rusthead_id = session.query(Product.supplier_id).join(Product.supplier).filter_by(name="Rusthead Designs").first()
    zazzle_id = session.query(Product.supplier_id).join(Product.supplier).filter_by(name="Zazzle").first()
    grandstand_id = session.query(Product.supplier_id).join(Product.supplier).filter_by(name="Grandstand Glassware").first()

    # Fallbacks in case any supplier ID is not found
    rusthead_id = rusthead_id[0] if rusthead_id else 1
    zazzle_id = zazzle_id[0] if zazzle_id else 2
    grandstand_id = grandstand_id[0] if grandstand_id else 3

    flat_products = [
        # T-SHIRTS ($20)
        ("T-Shirt - Blue - Small", "Clothing", 3, 20.0, 14.0, rusthead_id),
        ("T-Shirt - Blue - Medium", "Clothing", 2, 20.0, 14.0, rusthead_id),
        ("T-Shirt - Blue - Large", "Clothing", 6, 20.0, 14.0, rusthead_id),
        ("T-Shirt - Blue - XL", "Clothing", 4, 20.0, 14.0, rusthead_id),
        ("T-Shirt - Blue - XXL", "Clothing", 3, 20.0, 14.0, rusthead_id),
        ("T-Shirt - Orange - Small", "Clothing", 3, 20.0, 14.0, rusthead_id),
        ("T-Shirt - Orange - Medium", "Clothing", 3, 20.0, 14.0, rusthead_id),
        ("T-Shirt - Orange - Large", "Clothing", 3, 20.0, 14.0, rusthead_id),
        ("T-Shirt - Orange - XL", "Clothing", 2, 20.0, 14.0, rusthead_id),
        ("T-Shirt - Orange - XXL", "Clothing", 2, 20.0, 14.0, rusthead_id),
        ("T-Shirt - Purple - Small", "Clothing", 2, 20.0, 14.0, rusthead_id),
        ("T-Shirt - Purple - Medium", "Clothing", 0, 20.0, 14.0, rusthead_id),
        ("T-Shirt - Purple - Large", "Clothing", 3, 20.0, 14.0, rusthead_id),
        ("T-Shirt - Purple - XL", "Clothing", 2, 20.0, 14.0, rusthead_id),
        ("T-Shirt - Purple - XXL", "Clothing", 1, 20.0, 14.0, rusthead_id),
        ("T-Shirt - Green - Small", "Clothing", 3, 20.0, 14.0, rusthead_id),
        ("T-Shirt - Green - Medium", "Clothing", 0, 20.0, 14.0, rusthead_id),
        ("T-Shirt - Green - Large", "Clothing", 1, 20.0, 14.0, rusthead_id),
        ("T-Shirt - Green - XL", "Clothing", 1, 20.0, 14.0, rusthead_id),
        ("T-Shirt - Green - XXL", "Clothing", 2, 20.0, 14.0, rusthead_id),

        # Truck Shirt - Short Sleeve ($25)
        ("Truck Shirt - SS - Small", "Clothing", 2, 25.0, 18.0, rusthead_id),
        ("Truck Shirt - SS - Medium", "Clothing", 3, 25.0, 18.0, rusthead_id),
        ("Truck Shirt - SS - Large", "Clothing", 10, 25.0, 18.0, rusthead_id),
        ("Truck Shirt - SS - XL", "Clothing", 8, 25.0, 18.0, rusthead_id),
        ("Truck Shirt - SS - XXL", "Clothing", 5, 25.0, 18.0, rusthead_id),

        # Truck Shirt - Long Sleeve ($30)
        ("Truck Shirt - LS - Small", "Clothing", 4, 30.0, 22.0, rusthead_id),
        ("Truck Shirt - LS - Medium", "Clothing", 6, 30.0, 22.0, rusthead_id),
        ("Truck Shirt - LS - Large", "Clothing", 20, 30.0, 22.0, rusthead_id),
        ("Truck Shirt - LS - XL", "Clothing", 5, 30.0, 22.0, rusthead_id),
        ("Truck Shirt - LS - XXL", "Clothing", 7, 30.0, 22.0, rusthead_id),

        # Tote Bags ($15)
        ("Tote Bag", "Bag", 10, 15.0, 10.0, zazzle_id),

        # Mugs ($15)
        ("Mug", "Kitchenware", 20, 15.0, 10.0, grandstand_id),

        # Hats - Baseball Style ($25)
        ("Hat - Baseball - Beige", "Hat", 3, 25.0, 18.0, rusthead_id),
        ("Hat - Baseball - Navy", "Hat", 4, 25.0, 18.0, rusthead_id),

        # Hats - 5 Panel ($25)
        ("Hat - 5 Panel - Yellow", "Hat", 1, 25.0, 18.0, rusthead_id),
        ("Hat - 5 Panel - Red", "Hat", 3, 25.0, 18.0, rusthead_id),
        ("Hat - 5 Panel - Navy", "Hat", 1, 25.0, 18.0, rusthead_id),
        ("Hat - 5 Panel - Purple", "Hat", 6, 25.0, 18.0, rusthead_id),
        ("Hat - 5 Panel - White", "Hat", 2, 25.0, 18.0, rusthead_id),
        ("Hat - 5 Panel - Teal", "Hat", 1, 25.0, 18.0, rusthead_id),
        ("Hat - 5 Panel - Black", "Hat", 3, 25.0, 18.0, rusthead_id),
    ]

    for name, category, stock_level, price, cost_price, supplier_id in flat_products:
        existing = session.query(Product).filter_by(name=name).first()
        if not existing:
            session.add(Product(
                name=name,
                category=category,
                stock_level=stock_level,
                reorder_threshold=5,
                price=price,
                cost_price=cost_price,
                supplier_id=supplier_id,
                image_url=""
            ))

    session.commit()
    session.close()
    add_product_images()

def add_product_images():
    session = get_session()

    # Sample product images - replace with your actual product IDs
    images = [
        ProductImage(product_id=1, image_url="/images/tshirts/blue-front.jpg"),
        ProductImage(product_id=1, image_url="/images/tshirts/blue-back.jpg"),
        ProductImage(product_id=2, image_url="/images/tshirts/blue-front.jpg"),
        ProductImage(product_id=2, image_url="/images/tshirts/blue-back.jpg"),
        ProductImage(product_id=3, image_url="/images/tshirts/blue-front.jpg"),
        ProductImage(product_id=3, image_url="/images/tshirts/blue-back.jpg"),
        ProductImage(product_id=4, image_url="/images/tshirts/blue-front.jpg"),
        ProductImage(product_id=4, image_url="/images/tshirts/blue-back.jpg"),
        ProductImage(product_id=5, image_url="/images/tshirts/blue-front.jpg"),
        ProductImage(product_id=5, image_url="/images/tshirts/blue-back.jpg"),
        ProductImage(product_id=6, image_url="/images/tshirts/orange-front.jpg"),
        ProductImage(product_id=6, image_url="/images/tshirts/orange-back.jpg"),
        ProductImage(product_id=7, image_url="/images/tshirts/orange-front.jpg"),
        ProductImage(product_id=7, image_url="/images/tshirts/orange-back.jpg"),
        ProductImage(product_id=8, image_url="/images/tshirts/orange-front.jpg"),
        ProductImage(product_id=8, image_url="/images/tshirts/orange-back.jpg"),
        ProductImage(product_id=9, image_url="/images/tshirts/orange-front.jpg"),
        ProductImage(product_id=9, image_url="/images/tshirts/orange-back.jpg"),
        ProductImage(product_id=10, image_url="/images/tshirts/orange-front.jpg"),
        ProductImage(product_id=10, image_url="/images/tshirts/orange-back.jpg"),
        ProductImage(product_id=11, image_url="/images/tshirts/purple-front.jpg"),
        ProductImage(product_id=11, image_url="/images/tshirts/purple-back.jpg"),
        ProductImage(product_id=12, image_url="/images/tshirts/purple-front.jpg"),
        ProductImage(product_id=12, image_url="/images/tshirts/purple-back.jpg"),
        ProductImage(product_id=13, image_url="/images/tshirts/purple-front.jpg"),
        ProductImage(product_id=13, image_url="/images/tshirts/purple-back.jpg"),
        ProductImage(product_id=14, image_url="/images/tshirts/purple-front.jpg"),
        ProductImage(product_id=14, image_url="/images/tshirts/purple-back.jpg"),
        ProductImage(product_id=15, image_url="/images/tshirts/purple-front.jpg"),
        ProductImage(product_id=15, image_url="/images/tshirts/purple-back.jpg"),
        ProductImage(product_id=16, image_url="/images/tshirts/green-front.jpg"),
        ProductImage(product_id=16, image_url="/images/tshirts/green-back.jpg"),
        ProductImage(product_id=16, image_url="/images/tshirts/green-zoom.jpg"),
        ProductImage(product_id=17, image_url="/images/tshirts/green-front.jpg"),
        ProductImage(product_id=17, image_url="/images/tshirts/green-back.jpg"),
        ProductImage(product_id=17, image_url="/images/tshirts/green-zoom.jpg"),
        ProductImage(product_id=18, image_url="/images/tshirts/green-front.jpg"),
        ProductImage(product_id=18, image_url="/images/tshirts/green-back.jpg"),
        ProductImage(product_id=18, image_url="/images/tshirts/green-zoom.jpg"),
        ProductImage(product_id=19, image_url="/images/tshirts/green-front.jpg"),
        ProductImage(product_id=19, image_url="/images/tshirts/green-back.jpg"),
        ProductImage(product_id=19, image_url="/images/tshirts/green-zoom.jpg"),  
        ProductImage(product_id=20, image_url="/images/tshirts/green-front.jpg"),
        ProductImage(product_id=20, image_url="/images/tshirts/green-back.jpg"),
        ProductImage(product_id=20, image_url="/images/tshirts/green-zoom.jpg"),
        ProductImage(product_id=21, image_url="/images/tshirts/truck-shirt-ss.jpg"),
        ProductImage(product_id=21, image_url="/images/tshirts/truck-shirt-ss-zoom.jpg"),
        ProductImage(product_id=22, image_url="/images/tshirts/truck-shirt-ss.jpg"),
        ProductImage(product_id=22, image_url="/images/tshirts/truck-shirt-ss-zoom.jpg"),
        ProductImage(product_id=23, image_url="/images/tshirts/truck-shirt-ss.jpg"),
        ProductImage(product_id=23, image_url="/images/tshirts/truck-shirt-ss-zoom.jpg"),
        ProductImage(product_id=24, image_url="/images/tshirts/truck-shirt-ss.jpg"),
        ProductImage(product_id=24, image_url="/images/tshirts/truck-shirt-ss-zoom.jpg"),
        ProductImage(product_id=25, image_url="/images/tshirts/truck-shirt-ss.jpg"),
        ProductImage(product_id=25, image_url="/images/tshirts/truck-shirt-ss-zoom.jpg"),
        ProductImage(product_id=26, image_url="/images/tshirts/truck-shirt-ls.jpg"),
        ProductImage(product_id=27, image_url="/images/tshirts/truck-shirt-ls.jpg"),
        ProductImage(product_id=28, image_url="/images/tshirts/truck-shirt-ls.jpg"),
        ProductImage(product_id=29, image_url="/images/tshirts/truck-shirt-ls.jpg"),
        ProductImage(product_id=30, image_url="/images/tshirts/truck-shirt-ls.jpg"),
        ProductImage(product_id=31, image_url="/images/tote-bag.jpg"),
        ProductImage(product_id=32, image_url="/images/mug.jpg"),
        ProductImage(product_id=33, image_url="/images/hat/hat.jpg"),
        ProductImage(product_id=34, image_url="/images/hat/hat.jpg"),
        ProductImage(product_id=35, image_url="/images/hat/hat-yellow.jpg"),
        ProductImage(product_id=36, image_url="/images/hat/hat-red.jpg"),
        ProductImage(product_id=37, image_url="/images/hat/hat-voilet.jpg"),
        ProductImage(product_id=38, image_url="/images/hat/hat-voilet.jpg"),
        ProductImage(product_id=39, image_url="/images/hat/hat-white.jpg"),
        ProductImage(product_id=40, image_url="/images/hat/hat.jpg"),
        ProductImage(product_id=41, image_url="/images/hat/hat-black.jpg")
    ]

    for img in images:
        session.add(img)

    session.commit()
    session.close()


def add_batches():
    session = get_session()

    batches = [
        Batch(product_id=1, supplier_id=1, batch_number="ABC123", quantity_received=100, received_date=date(2025, 2, 10), expiration_date=None, batch_status="Active"),
        Batch(product_id=2, supplier_id=2, batch_number="DEF456", quantity_received=50, received_date=date(2025, 2, 5), expiration_date=date(2026, 2, 5), batch_status="Active"),
        Batch(product_id=3, supplier_id=3, batch_number="GHI789", quantity_received=200, received_date=date(2025, 1, 15), expiration_date=None, batch_status="Active"),
        Batch(product_id=4, supplier_id=4, batch_number="JKL012", quantity_received=75, received_date=date(2025, 2, 1), expiration_date=date(2025, 8, 1), batch_status="Active"),
    ]

    for batch_data in batches:
        existing_batch = session.query(Batch).filter_by(batch_number=batch_data.batch_number).first()
        if not existing_batch:
            session.add(batch_data)

    session.commit()
    session.close()

def add_default_roles():
    session = get_session()

    roles = [ Role(id = 1, name = 'Admin'), Role(id = 2, name = 'Customer'), Role(id = 3, name = 'Supplier')]

    for role in roles:
        existing_role = session.query(Role).filter_by(name=role.name).first()
        if not existing_role:
            session.add(role)

    session.commit()
    session.close()
