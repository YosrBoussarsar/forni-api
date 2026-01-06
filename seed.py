from app import create_app, db
from models.user import UserModel
from models.bakery import BakeryModel
from models.product import ProductModel
from models.surplus_bag import SurplusBagModel
from models.order import OrderModel
from models.review import ReviewModel
from datetime import datetime, timedelta


app = create_app()

from werkzeug.security import generate_password_hash


with app.app_context():
    print("Clearing database...")
    db.drop_all()
    db.create_all()

    print("Creating users...")
    admin = UserModel(
        email="admin@forni.tn",
        password_hash=generate_password_hash("Admin123!"),
        first_name="Admin",
        last_name="User",
        phone = "92929292",
        role="admin"
)

    owner = UserModel(
        email="owner@forni.tn",
        password_hash=generate_password_hash("Owner123!"),
        first_name="Bakery",
        last_name="Owner",
        phone = "94949494",
        role="bakery_owner"
    )

    customer = UserModel(
        email="customer@forni.tn",
        password_hash=generate_password_hash("Customer123!"),
        first_name="John",
        last_name="Doe",
        phone = "93939393",
        role="customer"
    )

    # Additional diverse customers for reviews
    customer2 = UserModel(
        email="sarah.jones@email.com",
        password_hash=generate_password_hash("Customer123!"),
        first_name="Sarah",
        last_name="Jones",
        phone="96969696",
        role="customer"
    )

    customer3 = UserModel(
        email="ahmed.ben@email.com",
        password_hash=generate_password_hash("Customer123!"),
        first_name="Ahmed",
        last_name="Ben Ali",
        phone="97979797",
        role="customer"
    )

    customer4 = UserModel(
        email="marie.dubois@email.com",
        password_hash=generate_password_hash("Customer123!"),
        first_name="Marie",
        last_name="Dubois",
        phone="98989898",
        role="customer"
    )

    customer5 = UserModel(
        email="karim.messaoudi@email.com",
        password_hash=generate_password_hash("Customer123!"),
        first_name="Karim",
        last_name="Messaoudi",
        phone="99999999",
        role="customer"
    )

    customer6 = UserModel(
        email="leila.trabelsi@email.com",
        password_hash=generate_password_hash("Customer123!"),
        first_name="Leila",
        last_name="Trabelsi",
        phone="91919191",
        role="customer"
    )

    db.session.add_all([admin, owner, customer, customer2, customer3, customer4, customer5, customer6])
    db.session.commit()

    print("Creating bakeries...")
    bakery1 = BakeryModel(
        name="La Baguette Dorée",
        address="123 Rue de Paris",
        city="Tunis",
        owner_id=owner.id,
        description="Fresh French-style bread and pastries"
    )

    bakery2 = BakeryModel(
        name="Sweet Crumbs",
        address="45 Avenue Habib Bourguiba",
        city="Tunis",
        owner_id=owner.id,
        description="Cupcakes, cookies, and artisan desserts"
    )

    bakery3 = BakeryModel(
        name="Pain Artisan",
        address="78 Rue de Marseille",
        city="Tunis",
        owner_id=owner.id,
        description="Traditional artisan breads and sourdough"
    )

    bakery4 = BakeryModel(
        name="Pâtisserie Royale",
        address="12 Avenue Mohamed V",
        city="Tunis",
        owner_id=owner.id,
        description="Elegant French pastries and wedding cakes"
    )

    bakery5 = BakeryModel(
        name="Le Croissant d'Or",
        address="56 Rue de Carthage",
        city="Tunis",
        owner_id=owner.id,
        description="Breakfast pastries and viennoiseries"
    )

    bakery6 = BakeryModel(
        name="Boulangerie du Soleil",
        address="89 Avenue de la Liberté",
        city="Sousse",
        owner_id=owner.id,
        description="Traditional Tunisian and French breads"
    )

    bakery7 = BakeryModel(
        name="Délices de Carthage",
        address="34 Rue Ibn Khaldoun",
        city="Tunis",
        owner_id=owner.id,
        description="Mediterranean sweets and pastries"
    )

    bakery8 = BakeryModel(
        name="La Brioche Maison",
        address="67 Avenue Habib Thameur",
        city="Sfax",
        owner_id=owner.id,
        description="Homemade brioches and sweet breads"
    )

    bakery9 = BakeryModel(
        name="Artisan du Pain",
        address="23 Rue de Rome",
        city="Tunis",
        owner_id=owner.id,
        description="Organic sourdough and whole grain breads"
    )

    bakery10 = BakeryModel(
        name="Sucré & Salé",
        address="45 Avenue Farhat Hached",
        city="Sousse",
        owner_id=owner.id,
        description="Sweet and savory baked goods"
    )

    bakery11 = BakeryModel(
        name="Le Fournil Doré",
        address="91 Rue de Constantine",
        city="Tunis",
        owner_id=owner.id,
        description="Classic French bakery with daily specials"
    )

    bakery12 = BakeryModel(
        name="Pain & Chocolat",
        address="18 Avenue Bourguiba",
        city="Hammamet",
        owner_id=owner.id,
        description="Chocolate specialties and fresh pastries"
    )

    bakery13 = BakeryModel(
        name="Boulangerie Moderne",
        address="52 Rue de la République",
        city="Bizerte",
        owner_id=owner.id,
        description="Modern bakery with traditional recipes"
    )

    bakery14 = BakeryModel(
        name="Les Gourmandises",
        address="76 Avenue de France",
        city="Tunis",
        owner_id=owner.id,
        description="Gourmet pastries and artisan desserts"
    )

    bakery15 = BakeryModel(
        name="Au Bon Pain",
        address="29 Rue d'Alger",
        city="Monastir",
        owner_id=owner.id,
        description="Fresh bread and traditional baguettes"
    )

    db.session.add_all([bakery1, bakery2, bakery3, bakery4, bakery5, bakery6, bakery7, 
                        bakery8, bakery9, bakery10, bakery11, bakery12, bakery13, bakery14, bakery15])
    db.session.commit()

    print("Creating products...")
    products = [
        # Bakery 1 - La Baguette Dorée
        ProductModel(name="Croissant", price=2.5, bakery_id=bakery1.id, tags="croissant,pastry,breakfast,french"),
        ProductModel(name="Pain au Chocolat", price=3.0, bakery_id=bakery1.id, tags="pastry,chocolate,breakfast,french"),
        ProductModel(name="Baguette", price=1.5, bakery_id=bakery1.id, tags="bread,baguette,french"),
        ProductModel(name="Éclair", price=4.0, bakery_id=bakery1.id, tags="pastry,dessert,chocolate,french"),
        ProductModel(name="Macaron Box (6)", price=12.0, bakery_id=bakery1.id, tags="macaron,dessert,french,sweet"),
        
        # Bakery 2 - Sweet Crumbs
        ProductModel(name="Chocolate Cake Slice", price=4.0, bakery_id=bakery2.id, tags="cake,chocolate,dessert,sweet"),
        ProductModel(name="Red Velvet Cupcake", price=3.5, bakery_id=bakery2.id, tags="cupcake,dessert,sweet"),
        ProductModel(name="Chocolate Chip Cookie", price=2.0, bakery_id=bakery2.id, tags="cookie,chocolate,sweet,snack"),
        ProductModel(name="Brownie", price=3.0, bakery_id=bakery2.id, tags="brownie,chocolate,dessert,sweet"),
        ProductModel(name="Cheesecake Slice", price=5.0, bakery_id=bakery2.id, tags="cheesecake,dessert,sweet"),
        
        # Bakery 3 - Pain Artisan
        ProductModel(name="Sourdough Loaf", price=6.0, bakery_id=bakery3.id, tags="bread,sourdough,artisan,healthy"),
        ProductModel(name="Whole Wheat Bread", price=5.0, bakery_id=bakery3.id, tags="bread,whole-wheat,healthy"),
        ProductModel(name="Rye Bread", price=5.5, bakery_id=bakery3.id, tags="bread,rye,artisan,healthy"),
        ProductModel(name="Multigrain Roll", price=2.0, bakery_id=bakery3.id, tags="bread,multigrain,healthy,roll"),
        
        # Bakery 4 - Pâtisserie Royale
        ProductModel(name="Opera Cake Slice", price=6.0, bakery_id=bakery4.id, tags="cake,dessert,french,chocolate,premium"),
        ProductModel(name="Mille-feuille", price=5.5, bakery_id=bakery4.id, tags="pastry,dessert,french,premium"),
        ProductModel(name="Tarte Tatin", price=7.0, bakery_id=bakery4.id, tags="tart,dessert,french,apple,premium"),
        ProductModel(name="Religieuse", price=5.0, bakery_id=bakery4.id, tags="pastry,dessert,french,premium"),
        ProductModel(name="Paris-Brest", price=6.5, bakery_id=bakery4.id, tags="pastry,dessert,french,premium"),
        
        # Bakery 5 - Le Croissant d'Or
        ProductModel(name="Almond Croissant", price=3.5, bakery_id=bakery5.id, tags="croissant,pastry,breakfast,almond"),
        ProductModel(name="Pain aux Raisins", price=3.0, bakery_id=bakery5.id, tags="pastry,breakfast,raisin,french"),
        ProductModel(name="Chausson aux Pommes", price=3.5, bakery_id=bakery5.id, tags="pastry,apple,breakfast,french"),
        ProductModel(name="Brioche", price=4.0, bakery_id=bakery5.id, tags="brioche,breakfast,sweet,french"),
        
        # Bakery 6 - Boulangerie du Soleil
        ProductModel(name="Traditional Baguette", price=1.8, bakery_id=bakery6.id, tags="bread,baguette,french,traditional"),
        ProductModel(name="Ciabatta", price=4.0, bakery_id=bakery6.id, tags="bread,italian,ciabatta"),
        ProductModel(name="Focaccia", price=4.5, bakery_id=bakery6.id, tags="bread,italian,focaccia,savory"),
        ProductModel(name="Olive Bread", price=5.0, bakery_id=bakery6.id, tags="bread,olive,savory,artisan"),
        
        # Bakery 7 - Délices de Carthage
        ProductModel(name="Baklava", price=8.0, bakery_id=bakery7.id, tags="dessert,sweet,middle-eastern,pastry"),
        ProductModel(name="Makroud", price=6.0, bakery_id=bakery7.id, tags="dessert,sweet,tunisian,traditional"),
        ProductModel(name="Zlabia", price=5.0, bakery_id=bakery7.id, tags="dessert,sweet,tunisian,traditional"),
        ProductModel(name="Kaak Warka", price=7.0, bakery_id=bakery7.id, tags="dessert,sweet,tunisian,traditional"),
        
        # Bakery 8 - La Brioche Maison
        ProductModel(name="Chocolate Brioche", price=4.5, bakery_id=bakery8.id, tags="brioche,chocolate,breakfast,sweet"),
        ProductModel(name="Sugar Brioche", price=4.0, bakery_id=bakery8.id, tags="brioche,breakfast,sweet"),
        ProductModel(name="Cinnamon Roll", price=3.5, bakery_id=bakery8.id, tags="roll,cinnamon,breakfast,sweet"),
        ProductModel(name="Brioche Loaf", price=7.0, bakery_id=bakery8.id, tags="brioche,bread,breakfast,sweet"),
        
        # Bakery 9 - Artisan du Pain
        ProductModel(name="Organic Sourdough", price=8.0, bakery_id=bakery9.id, tags="bread,sourdough,organic,healthy,artisan"),
        ProductModel(name="Spelt Bread", price=7.0, bakery_id=bakery9.id, tags="bread,spelt,organic,healthy,artisan"),
        ProductModel(name="Seeded Loaf", price=6.5, bakery_id=bakery9.id, tags="bread,seeds,healthy,artisan"),
        ProductModel(name="Kamut Bread", price=7.5, bakery_id=bakery9.id, tags="bread,kamut,organic,healthy,artisan"),
        
        # Bakery 10 - Sucré & Salé
        ProductModel(name="Quiche Lorraine", price=6.0, bakery_id=bakery10.id, tags="quiche,savory,french,lunch"),
        ProductModel(name="Spinach Feta Roll", price=4.5, bakery_id=bakery10.id, tags="roll,savory,vegetarian,lunch"),
        ProductModel(name="Apple Tart", price=5.0, bakery_id=bakery10.id, tags="tart,dessert,apple,sweet"),
        ProductModel(name="Lemon Meringue Pie", price=5.5, bakery_id=bakery10.id, tags="pie,dessert,lemon,sweet"),
        
        # Bakery 11 - Le Fournil Doré
        ProductModel(name="Country Bread", price=5.0, bakery_id=bakery11.id, tags="bread,rustic,traditional,artisan"),
        ProductModel(name="Walnut Bread", price=6.0, bakery_id=bakery11.id, tags="bread,walnut,artisan,nuts"),
        ProductModel(name="Olive Fougasse", price=5.5, bakery_id=bakery11.id, tags="bread,olive,french,savory"),
        ProductModel(name="Epi Bread", price=4.5, bakery_id=bakery11.id, tags="bread,french,traditional"),
        
        # Bakery 12 - Pain & Chocolat
        ProductModel(name="Chocolate Tart", price=6.0, bakery_id=bakery12.id, tags="tart,chocolate,dessert,sweet"),
        ProductModel(name="Chocolate Mousse Cup", price=4.5, bakery_id=bakery12.id, tags="mousse,chocolate,dessert,sweet"),
        ProductModel(name="Hot Chocolate Bomb", price=5.0, bakery_id=bakery12.id, tags="chocolate,sweet,specialty"),
        ProductModel(name="Chocolate Croissant", price=3.5, bakery_id=bakery12.id, tags="croissant,chocolate,pastry,breakfast"),
        
        # Bakery 13 - Boulangerie Moderne
        ProductModel(name="Modern Baguette", price=2.0, bakery_id=bakery13.id, tags="bread,baguette,french"),
        ProductModel(name="Artisan Roll", price=1.5, bakery_id=bakery13.id, tags="bread,roll,artisan"),
        ProductModel(name="Flatbread", price=3.0, bakery_id=bakery13.id, tags="bread,flatbread"),
        ProductModel(name="Sandwich Baguette", price=4.0, bakery_id=bakery13.id, tags="bread,baguette,sandwich,lunch"),
        
        # Bakery 14 - Les Gourmandises
        ProductModel(name="Fruit Tart", price=7.0, bakery_id=bakery14.id, tags="tart,dessert,fruit,sweet"),
        ProductModel(name="Pistachio Éclair", price=5.0, bakery_id=bakery14.id, tags="pastry,dessert,pistachio,french"),
        ProductModel(name="Strawberry Cream Puff", price=4.5, bakery_id=bakery14.id, tags="pastry,dessert,strawberry,sweet"),
        ProductModel(name="Caramel Macaron", price=2.5, bakery_id=bakery14.id, tags="macaron,dessert,caramel,sweet"),
        
        # Bakery 15 - Au Bon Pain
        ProductModel(name="Fresh Baguette", price=1.5, bakery_id=bakery15.id, tags="bread,baguette,french,fresh"),
        ProductModel(name="Dinner Roll (6)", price=3.0, bakery_id=bakery15.id, tags="bread,roll,dinner"),
        ProductModel(name="French Stick", price=2.5, bakery_id=bakery15.id, tags="bread,baguette,french"),
        ProductModel(name="Baguette Bundle (3)", price=4.0, bakery_id=bakery15.id, tags="bread,baguette,french,bundle"),
    ]

    db.session.add_all(products)
    db.session.commit()

    print("Creating surplus bags...")

    surplus_bags = [
        # Bakery 1
        SurplusBagModel(
            bakery_id=bakery1.id,
            title="Morning Pastry Mix",
            description="A mix of croissants, pain au chocolat, and brioche",
            category="pastries",
            tags="sweet,pastry,breakfast,french",
            original_value=12.00,
            sale_price=5.00,
            quantity_available=3,
            pickup_start=datetime.utcnow(),
            pickup_end=datetime.utcnow() + timedelta(hours=2),
            status="available"
        ),
        SurplusBagModel(
            bakery_id=bakery1.id,
            title="French Pastries Surprise",
            description="Assorted French pastries from today's batch",
            category="pastries",
            tags="sweet,pastry,french,dessert",
            original_value=15.00,
            sale_price=6.50,
            quantity_available=2,
            pickup_start=datetime.utcnow(),
            pickup_end=datetime.utcnow() + timedelta(hours=3),
            status="available"
        ),
        
        # Bakery 2
        SurplusBagModel(
            bakery_id=bakery2.id,
            title="Cupcake Surprise Box",
            description="Assorted cupcakes from today's batch",
            category="desserts",
            tags="sweet,dessert,cupcake",
            original_value=15.00,
            sale_price=6.00,
            quantity_available=2,
            pickup_start=datetime.utcnow(),
            pickup_end=datetime.utcnow() + timedelta(hours=3),
            status="available"
        ),
        SurplusBagModel(
            bakery_id=bakery2.id,
            title="Cookie & Brownie Mix",
            description="Fresh cookies and brownies",
            category="desserts",
            tags="sweet,dessert,chocolate,cookie",
            original_value=10.00,
            sale_price=4.00,
            quantity_available=4,
            pickup_start=datetime.utcnow(),
            pickup_end=datetime.utcnow() + timedelta(hours=4),
            status="available"
        ),
        
        # Bakery 3
        SurplusBagModel(
            bakery_id=bakery3.id,
            title="Artisan Bread Bundle",
            description="Mix of sourdough, whole wheat, and rye bread",
            category="bread",
            tags="bread,artisan,healthy,savory",
            original_value=18.00,
            sale_price=7.00,
            quantity_available=3,
            pickup_start=datetime.utcnow(),
            pickup_end=datetime.utcnow() + timedelta(hours=5),
            status="available"
        ),
        SurplusBagModel(
            bakery_id=bakery3.id,
            title="Bread & Rolls Mix",
            description="Fresh bread loaves and multigrain rolls",
            category="bread",
            tags="bread,healthy,savory",
            original_value=12.00,
            sale_price=5.00,
            quantity_available=5,
            pickup_start=datetime.utcnow(),
            pickup_end=datetime.utcnow() + timedelta(hours=6),
            status="available"
        ),
        
        # Bakery 4
        SurplusBagModel(
            bakery_id=bakery4.id,
            title="Premium Pastries Box",
            description="Gourmet French pastries including mille-feuille and opera cake",
            category="pastries",
            tags="sweet,pastry,french,premium,dessert",
            original_value=25.00,
            sale_price=10.00,
            quantity_available=2,
            pickup_start=datetime.utcnow(),
            pickup_end=datetime.utcnow() + timedelta(hours=2),
            status="available"
        ),
        SurplusBagModel(
            bakery_id=bakery4.id,
            title="Dessert Selection",
            description="Assorted elegant desserts",
            category="desserts",
            tags="sweet,dessert,french,premium",
            original_value=20.00,
            sale_price=8.00,
            quantity_available=3,
            pickup_start=datetime.utcnow(),
            pickup_end=datetime.utcnow() + timedelta(hours=3),
            status="available"
        ),
        
        # Bakery 5
        SurplusBagModel(
            bakery_id=bakery5.id,
            title="Breakfast Treats",
            description="Almond croissants, pain aux raisins, and brioches",
            category="pastries",
            tags="sweet,pastry,breakfast,french",
            original_value=14.00,
            sale_price=5.50,
            quantity_available=4,
            pickup_start=datetime.utcnow(),
            pickup_end=datetime.utcnow() + timedelta(hours=2),
            status="available"
        ),
        
        # Bakery 6
        SurplusBagModel(
            bakery_id=bakery6.id,
            title="Traditional Bread Mix",
            description="Baguettes, ciabatta, and focaccia",
            category="bread",
            original_value=11.00,
            sale_price=4.50,
            quantity_available=6,
            pickup_start=datetime.utcnow(),
            pickup_end=datetime.utcnow() + timedelta(hours=4),
            status="available"
        ),
        SurplusBagModel(
            bakery_id=bakery6.id,
            title="Mediterranean Bread Bag",
            description="Olive bread and focaccia selection",
            category="bread",
            original_value=13.00,
            sale_price=5.50,
            quantity_available=3,
            pickup_start=datetime.utcnow(),
            pickup_end=datetime.utcnow() + timedelta(hours=5),
            status="available"
        ),
        
        # Bakery 7
        SurplusBagModel(
            bakery_id=bakery7.id,
            title="Tunisian Sweets Box",
            description="Traditional baklava, makroud, and zlabia",
            category="desserts",
            original_value=22.00,
            sale_price=9.00,
            quantity_available=2,
            pickup_start=datetime.utcnow(),
            pickup_end=datetime.utcnow() + timedelta(hours=3),
            status="available"
        ),
        SurplusBagModel(
            bakery_id=bakery7.id,
            title="Mediterranean Desserts",
            description="Assorted traditional sweets",
            category="desserts",
            original_value=18.00,
            sale_price=7.00,
            quantity_available=4,
            pickup_start=datetime.utcnow(),
            pickup_end=datetime.utcnow() + timedelta(hours=4),
            status="available"
        ),
        
        # Bakery 8
        SurplusBagModel(
            bakery_id=bakery8.id,
            title="Brioche Lovers Box",
            description="Chocolate brioche, sugar brioche, and cinnamon rolls",
            category="pastries",
            original_value=16.00,
            sale_price=6.50,
            quantity_available=3,
            pickup_start=datetime.utcnow(),
            pickup_end=datetime.utcnow() + timedelta(hours=2),
            status="available"
        ),
        
        # Bakery 9
        SurplusBagModel(
            bakery_id=bakery9.id,
            title="Organic Bread Collection",
            description="Organic sourdough and specialty grain breads",
            category="bread",
            original_value=24.00,
            sale_price=10.00,
            quantity_available=2,
            pickup_start=datetime.utcnow(),
            pickup_end=datetime.utcnow() + timedelta(hours=6),
            status="available"
        ),
        SurplusBagModel(
            bakery_id=bakery9.id,
            title="Healthy Grains Mix",
            description="Spelt, seeded, and kamut breads",
            category="bread",
            original_value=20.00,
            sale_price=8.50,
            quantity_available=3,
            pickup_start=datetime.utcnow(),
            pickup_end=datetime.utcnow() + timedelta(hours=5),
            status="available"
        ),
        
        # Bakery 10
        SurplusBagModel(
            bakery_id=bakery10.id,
            title="Savory & Sweet Mix",
            description="Quiches, tarts, and sweet pies",
            category="mixed",
            original_value=19.00,
            sale_price=7.50,
            quantity_available=2,
            pickup_start=datetime.utcnow(),
            pickup_end=datetime.utcnow() + timedelta(hours=3),
            status="available"
        ),
        
        # Bakery 11
        SurplusBagModel(
            bakery_id=bakery11.id,
            title="Country Bread Selection",
            description="Country bread, walnut bread, and fougasse",
            category="bread",
            original_value=17.00,
            sale_price=7.00,
            quantity_available=4,
            pickup_start=datetime.utcnow(),
            pickup_end=datetime.utcnow() + timedelta(hours=4),
            status="available"
        ),
        
        # Bakery 12
        SurplusBagModel(
            bakery_id=bakery12.id,
            title="Chocolate Lovers Paradise",
            description="All things chocolate - tarts, mousse, and croissants",
            category="desserts",
            original_value=21.00,
            sale_price=8.50,
            quantity_available=3,
            pickup_start=datetime.utcnow(),
            pickup_end=datetime.utcnow() + timedelta(hours=2),
            status="available"
        ),
        
        # Bakery 13
        SurplusBagModel(
            bakery_id=bakery13.id,
            title="Daily Bread Bundle",
            description="Fresh baguettes, rolls, and flatbreads",
            category="bread",
            original_value=10.00,
            sale_price=4.00,
            quantity_available=5,
            pickup_start=datetime.utcnow(),
            pickup_end=datetime.utcnow() + timedelta(hours=5),
            status="available"
        ),
        
        # Bakery 14
        SurplusBagModel(
            bakery_id=bakery14.id,
            title="Gourmet Pastries Box",
            description="Fruit tarts, éclairs, and cream puffs",
            category="pastries",
            original_value=23.00,
            sale_price=9.50,
            quantity_available=2,
            pickup_start=datetime.utcnow(),
            pickup_end=datetime.utcnow() + timedelta(hours=2),
            status="available"
        ),
        SurplusBagModel(
            bakery_id=bakery14.id,
            title="Macaron & Treats",
            description="Assorted macarons and petit fours",
            category="desserts",
            original_value=18.00,
            sale_price=7.50,
            quantity_available=3,
            pickup_start=datetime.utcnow(),
            pickup_end=datetime.utcnow() + timedelta(hours=3),
            status="available"
        ),
        
        # Bakery 15
        SurplusBagModel(
            bakery_id=bakery15.id,
            title="Baguette Bundle",
            description="Fresh traditional baguettes",
            category="bread",
            original_value=8.00,
            sale_price=3.50,
            quantity_available=7,
            pickup_start=datetime.utcnow(),
            pickup_end=datetime.utcnow() + timedelta(hours=6),
            status="available"
        ),
    ]

    db.session.add_all(surplus_bags)
    db.session.commit()

    print("Creating orders...")

    # Reference first surplus bag for orders
    first_bag = surplus_bags[0]
    second_bag = surplus_bags[2]
    third_bag = surplus_bags[4]

    order1 = OrderModel(
        user_id=customer.id,
        bakery_id=bakery1.id,
        surplus_bag_id=first_bag.id,
        total_price=first_bag.sale_price,
        status="completed"
    )

    order2 = OrderModel(
        user_id=customer.id,
        bakery_id=bakery2.id,
        surplus_bag_id=second_bag.id,
        total_price=second_bag.sale_price,
        status="pending"
    )

    order3 = OrderModel(
        user_id=customer.id,
        bakery_id=bakery3.id,
        surplus_bag_id=third_bag.id,
        total_price=third_bag.sale_price,
        status="completed"
    )

    db.session.add_all([order1, order2, order3])
    db.session.commit()


    print("Creating reviews...")
    reviews = [
        # Bakery 1 reviews - Mix of ratings
        ReviewModel(
            user_id=customer2.id,
            bakery_id=bakery1.id,
            rating=5,
            comment="Amazing pastries! The croissants are flaky and buttery, just perfect."
        ),
        ReviewModel(
            user_id=customer.id,
            bakery_id=bakery1.id,
            rating=4,
            comment="Great quality, though a bit pricey. Still worth it!"
        ),
        ReviewModel(
            user_id=customer3.id,
            bakery_id=bakery1.id,
            rating=3,
            comment="Good pastries but the wait time was quite long during peak hours."
        ),
        
        # Bakery 2 reviews
        ReviewModel(
            user_id=customer4.id,
            bakery_id=bakery2.id,
            rating=5,
            comment="Best cupcakes in town! The chocolate cake is heavenly."
        ),
        ReviewModel(
            user_id=customer5.id,
            bakery_id=bakery2.id,
            rating=5,
            comment="Beautiful presentation and delicious treats. Highly recommend!"
        ),
        ReviewModel(
            user_id=customer.id,
            bakery_id=bakery2.id,
            rating=4,
            comment="Love their brownies! Very rich and fudgy."
        ),
        ReviewModel(
            user_id=customer6.id,
            bakery_id=bakery2.id,
            rating=3,
            comment="Tasty but a bit too sweet for my preference. Service was friendly though."
        ),
        
        # Bakery 3 reviews
        ReviewModel(
            user_id=customer2.id,
            bakery_id=bakery3.id,
            rating=5,
            comment="The sourdough is incredible! You can taste the quality."
        ),
        ReviewModel(
            user_id=customer3.id,
            bakery_id=bakery3.id,
            rating=5,
            comment="Best artisan bread I've ever had. The crust is perfect!"
        ),
        ReviewModel(
            user_id=customer4.id,
            bakery_id=bakery3.id,
            rating=4,
            comment="Excellent bread, though I wish they had more variety."
        ),
        
        # Bakery 4 reviews
        ReviewModel(
            user_id=customer.id,
            bakery_id=bakery4.id,
            rating=5,
            comment="Absolutely exquisite pastries! Worth every dinar."
        ),
        ReviewModel(
            user_id=customer5.id,
            bakery_id=bakery4.id,
            rating=4,
            comment="Beautiful cakes for special occasions. Very elegant."
        ),
        ReviewModel(
            user_id=customer6.id,
            bakery_id=bakery4.id,
            rating=5,
            comment="The opera cake is divine! Like being in Paris."
        ),
        ReviewModel(
            user_id=customer2.id,
            bakery_id=bakery4.id,
            rating=3,
            comment="Quality is great but quite expensive. Only for special treats."
        ),
        
        # Bakery 5 reviews
        ReviewModel(
            user_id=customer3.id,
            bakery_id=bakery5.id,
            rating=5,
            comment="Perfect breakfast spot! Fresh croissants every morning."
        ),
        ReviewModel(
            user_id=customer.id,
            bakery_id=bakery5.id,
            rating=4,
            comment="Good variety of viennoiseries. The almond croissant is my favorite!"
        ),
        ReviewModel(
            user_id=customer4.id,
            bakery_id=bakery5.id,
            rating=2,
            comment="Croissants were a bit dry when I visited. Maybe just an off day?"
        ),
        
        # Bakery 6 reviews
        ReviewModel(
            user_id=customer5.id,
            bakery_id=bakery6.id,
            rating=4,
            comment="Traditional bread done right. Great for daily staples."
        ),
        ReviewModel(
            user_id=customer6.id,
            bakery_id=bakery6.id,
            rating=5,
            comment="The focaccia is amazing! So flavorful and fresh."
        ),
        ReviewModel(
            user_id=customer2.id,
            bakery_id=bakery6.id,
            rating=3,
            comment="Decent bread, nothing extraordinary but reliable."
        ),
        
        # Bakery 7 reviews
        ReviewModel(
            user_id=customer.id,
            bakery_id=bakery7.id,
            rating=5,
            comment="Best baklava in Tunis! Authentic and delicious."
        ),
        ReviewModel(
            user_id=customer3.id,
            bakery_id=bakery7.id,
            rating=5,
            comment="The makroud tastes just like my grandmother used to make!"
        ),
        ReviewModel(
            user_id=customer4.id,
            bakery_id=bakery7.id,
            rating=4,
            comment="Great selection of traditional sweets. Always fresh."
        ),
        ReviewModel(
            user_id=customer5.id,
            bakery_id=bakery7.id,
            rating=4,
            comment="Authentic Tunisian pastries. The zlabia is perfectly sweet!"
        ),
        
        # Bakery 8 reviews
        ReviewModel(
            user_id=customer6.id,
            bakery_id=bakery8.id,
            rating=5,
            comment="The brioche is soft and fluffy. Simply perfect!"
        ),
        ReviewModel(
            user_id=customer2.id,
            bakery_id=bakery8.id,
            rating=4,
            comment="Love the cinnamon rolls! Great for weekend breakfast."
        ),
        ReviewModel(
            user_id=customer.id,
            bakery_id=bakery8.id,
            rating=3,
            comment="Good brioche but service could be faster during busy times."
        ),
        
        # Bakery 9 reviews
        ReviewModel(
            user_id=customer3.id,
            bakery_id=bakery9.id,
            rating=5,
            comment="Best organic bread! You can really taste the difference."
        ),
        ReviewModel(
            user_id=customer4.id,
            bakery_id=bakery9.id,
            rating=5,
            comment="Healthy and delicious. The seeded loaf is my go-to."
        ),
        ReviewModel(
            user_id=customer5.id,
            bakery_id=bakery9.id,
            rating=4,
            comment="Great quality organic products. A bit pricey but worth it for health."
        ),
        
        # Bakery 10 reviews
        ReviewModel(
            user_id=customer6.id,
            bakery_id=bakery10.id,
            rating=4,
            comment="Great variety of savory and sweet options. The quiche is excellent!"
        ),
        ReviewModel(
            user_id=customer.id,
            bakery_id=bakery10.id,
            rating=5,
            comment="Perfect for lunch! The spinach feta roll is my favorite."
        ),
        ReviewModel(
            user_id=customer2.id,
            bakery_id=bakery10.id,
            rating=3,
            comment="Good selection but the apple tart was too tart for my taste."
        ),
        
        # Bakery 11 reviews
        ReviewModel(
            user_id=customer3.id,
            bakery_id=bakery11.id,
            rating=5,
            comment="Classic French bakery done right. The walnut bread is incredible."
        ),
        ReviewModel(
            user_id=customer4.id,
            bakery_id=bakery11.id,
            rating=4,
            comment="Good quality bread. Great for sandwiches."
        ),
        ReviewModel(
            user_id=customer5.id,
            bakery_id=bakery11.id,
            rating=4,
            comment="The olive fougasse is delicious! Will definitely come back."
        ),
        
        # Bakery 12 reviews
        ReviewModel(
            user_id=customer6.id,
            bakery_id=bakery12.id,
            rating=5,
            comment="Heaven for chocolate lovers! Everything is so rich and delicious."
        ),
        ReviewModel(
            user_id=customer.id,
            bakery_id=bakery12.id,
            rating=5,
            comment="The chocolate mousse is to die for! Best I've ever had."
        ),
        ReviewModel(
            user_id=customer2.id,
            bakery_id=bakery12.id,
            rating=4,
            comment="Great chocolate selection. A bit sweet for some, but I love it!"
        ),
        ReviewModel(
            user_id=customer3.id,
            bakery_id=bakery12.id,
            rating=2,
            comment="Too rich for me, but my kids loved it. Just not my style."
        ),
        
        # Bakery 13 reviews
        ReviewModel(
            user_id=customer4.id,
            bakery_id=bakery13.id,
            rating=4,
            comment="Modern bakery with quality products. Good value for money."
        ),
        ReviewModel(
            user_id=customer5.id,
            bakery_id=bakery13.id,
            rating=4,
            comment="Fresh baguettes daily. Very convenient location."
        ),
        ReviewModel(
            user_id=customer6.id,
            bakery_id=bakery13.id,
            rating=3,
            comment="Convenient but lacks the charm of traditional bakeries."
        ),
        
        # Bakery 14 reviews
        ReviewModel(
            user_id=customer.id,
            bakery_id=bakery14.id,
            rating=5,
            comment="Gourmet pastries at their finest! The fruit tart is a work of art."
        ),
        ReviewModel(
            user_id=customer2.id,
            bakery_id=bakery14.id,
            rating=5,
            comment="Incredible attention to detail. Every pastry is perfect!"
        ),
        ReviewModel(
            user_id=customer3.id,
            bakery_id=bakery14.id,
            rating=4,
            comment="Expensive but worth it for special occasions."
        ),
        ReviewModel(
            user_id=customer4.id,
            bakery_id=bakery14.id,
            rating=3,
            comment="Beautiful pastries but portions are quite small for the price."
        ),
        
        # Bakery 15 reviews
        ReviewModel(
            user_id=customer5.id,
            bakery_id=bakery15.id,
            rating=4,
            comment="Reliable bakery for daily bread. Always fresh and tasty."
        ),
        ReviewModel(
            user_id=customer6.id,
            bakery_id=bakery15.id,
            rating=5,
            comment="Best baguettes for the price! Great value."
        ),
        ReviewModel(
            user_id=customer.id,
            bakery_id=bakery15.id,
            rating=4,
            comment="Simple but good. Perfect for everyday needs."
        ),
    ]

    db.session.add_all(reviews)
    db.session.commit()

    print("Database seeded successfully!")
