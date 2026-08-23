from src.db.database import SessionLocal, engine, Base
from src.db.models import Category, Brand, Product, SellerProduct, Comment
from src.ai.nlp import get_enbedding

db = SessionLocal()

try:
    print("⏳ در حال ساخت مجدد جداول...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # ==========================================
    # ۱. دسته‌بندی‌ها
    # ==========================================
    cat_mobile = Category(title="موبایل", slug="mobile")
    cat_laptop = Category(title="لپ‌تاپ", slug="laptop")
    cat_accessory = Category(title="لوازم جانبی", slug="accessory")
    
    db.add_all([cat_mobile, cat_laptop, cat_accessory])
    db.commit()

    # ==========================================
    # ۲. برندها
    # ==========================================
    brand_samsung = Brand(name="سامسونگ", slug="samsung")
    brand_apple = Brand(name="اپل", slug="apple")
    brand_xiaomi = Brand(name="شیائومی", slug="xiaomi")
    brand_asus = Brand(name="ایسوس", slug="asus")
    
    db.add_all([brand_samsung, brand_apple, brand_xiaomi, brand_asus])
    db.commit()

    # ==========================================
    # ۳. محصولات + تولید خودکار ایمبدینگ (title + description)
    # ==========================================
    raw_products = [
        {
            "title": "گوشی موبایل سامسونگ مدل Galaxy A55 دو سیم‌کارت ظرفیت 256 گیگابایت",
            "description": "گوشی میان‌رده سامسونگ با دوربین عالی و باتری 5000 میلی‌آمپر مناسب استفاده روزمره و عکاسی.",
            "category_id": cat_mobile.id,
            "brand_id": brand_samsung.id
        },
        {
            "title": "گوشی موبایل اپل مدل iPhone 15 Pro Max ظرفیت 256 گیگابایت",
            "description": "پرچمدار جدید اپل با بدنه تیتانیوم و پردازنده فوق‌سریع A17 Pro مناسب گیمینگ و کارهای سنگین گرافیکی.",
            "category_id": cat_mobile.id,
            "brand_id": brand_apple.id
        },
        {
            "title": "گوشی موبایل شیائومی مدل Redmi Note 13 Pro ظرفیت 256 گیگابایت",
            "description": "ارزش خرید بسیار بالا، دوربین 200 مگاپیکسلی و شارژر فوق سریع 67 واتی اقتصادی.",
            "category_id": cat_mobile.id,
            "brand_id": brand_xiaomi.id
        },
        {
            "title": "لپ تاپ 15.6 اینچی ایسوس مدل TUF Gaming F15",
            "description": "لپ‌تاپ گیمینگ قدرتمند با پردازنده Core i7 و گرافیک RTX 4060 مناسب بازی‌های سنگین، رندرینگ و مهندسی.",
            "category_id": cat_laptop.id,
            "brand_id": brand_asus.id
        }
    ]

    print("🤖 در حال تولید ایمبدینگ برای محصولات...")
    created_products = []
    for item in raw_products:
        # متن کامل برای یادگیری مدل معنایی
        full_text = f"{item['title']} {item['description']}"
        vector = get_enbedding(full_text)

        product = Product(
            title=item["title"],
            description=item["description"],
            category_id=item["category_id"],
            brand_id=item["brand_id"],
            embedding=vector
        )
        created_products.append(product)

    db.add_all(created_products)
    db.commit()

    # Refresh برای دسترسی به IDها
    for p in created_products:
        db.refresh(p)

    # ==========================================
    # ۴. فروشندگان و موجودی
    # ==========================================
    sellers = [
        SellerProduct(product_id=created_products[0].id, seller_name="دیجی‌کالا", price=18500000, stock=12, discount_percent=5),
        SellerProduct(product_id=created_products[0].id, seller_name="موبایل اکسپرس", price=18200000, stock=3, discount_percent=0),
        SellerProduct(product_id=created_products[1].id, seller_name="دیجی‌کالا", price=72500000, stock=5, discount_percent=2),
        SellerProduct(product_id=created_products[2].id, seller_name="تکنو لایف", price=14300000, stock=20, discount_percent=10),
        SellerProduct(product_id=created_products[3].id, seller_name="دیجی‌کالا", price=65000000, stock=8, discount_percent=0)
    ]
    db.add_all(sellers)
    db.commit()

    # ==========================================
    # ۵. نظرات کاربران + تولید ایمبدینگ نظرات
    # ==========================================
    raw_comments = [
        {"product_id": created_products[0].id, "title": "گوشی خیلی خوبیه", "body": "کیفیت صفحه نمایش و دوربینش تو این رنج قیمت بی‌نظیره.", "rate": 5},
        {"product_id": created_products[0].id, "title": "باتری ضعیف", "body": "گوشی خوبیه ولی باتریش اصلا دوام نداره.", "rate": 3},
        {"product_id": created_products[1].id, "title": "شاهکار اپل", "body": "سرعت فوق‌العاده و وزن کمتر نسبت به نسل قبل برای عکاسی عالی هست.", "rate": 5},
        {"product_id": created_products[2].id, "title": "ارزش خرید بالا", "body": "شارژر داخل جعبه نبود که خیلی تو ذوق میزد ولی کیفیت خوبی داره.", "rate": 3},
        {"product_id": created_products[3].id, "title": "گیمینگ عالی", "body": "صفحه نمایش با کیفیت بالایی دارد و همه بازی‌ها رو روان اجرا میکنه.", "rate": 4}
    ]

    print("🤖 در حال تولید ایمبدینگ برای نظرات...")
    created_comments = []
    for c in raw_comments:
        vector = get_enbedding(c["body"])
        comment = Comment(
            product_id=c["product_id"],
            title=c["title"],
            body=c["body"],
            rate=c["rate"],
            embedding=vector
        )
        created_comments.append(comment)

    db.add_all(created_comments)
    db.commit()

    print("🚀 دیتابیس با موفقیت پر شد و تمام بردارها ذخیره شدند!")

except Exception as e:
    db.rollback()
    print(f"❌ خطا: {e}")
finally:
    db.close()