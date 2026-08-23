from src.db.database import SessionLocal, engine, Base
from src.db.models import Category, Brand, Product, SellerProduct, Comment

db = SessionLocal()

try:
    print("⏳ در حال پاکسازی و ساخت مجدد جداول...")
    # این دو خط برای این است که اگر دیتای خرابی از قبل مانده پاک شود و از نو ساخته شود
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    print("✅ جداول آماده شد. در حال تزریق اطلاعات دیجی‌کالا...")

    # =========================
    # ۱. ایجاد دسته‌بندی‌ها
    # =========================
    cat_mobile = Category(title="موبایل", slug="mobile")
    cat_laptop = Category(title="لپ‌تاپ", slug="laptop")
    cat_accessory = Category(title="لوازم جانبی", slug="accessory")
    
    db.add_all([cat_mobile, cat_laptop, cat_accessory])
    db.commit()

    # =========================
    # ۲. ایجاد برندها
    # =========================
    brand_samsung = Brand(name="سامسونگ", slug="samsung")
    brand_apple = Brand(name="اپل", slug="apple")
    brand_xiaomi = Brand(name="شیائومی", slug="xiaomi")
    brand_asus = Brand(name="ایسوس", slug="asus")
    
    db.add_all([brand_samsung, brand_apple, brand_xiaomi, brand_asus])
    db.commit()

    # =========================
    # ۳. ایجاد محصولات (مرتبط با دسته و برند)
    # =========================
    products = [
        Product(
            title="گوشی موبایل سامسونگ مدل Galaxy A55 دو سیم‌کارت ظرفیت 256 گیگابایت",
            description="گوشی میان‌رده سامسونگ با دوربین عالی و باتری 5000 میلی‌آمپر.",
            category_id=cat_mobile.id,
            brand_id=brand_samsung.id
        ),
        Product(
            title="گوشی موبایل اپل مدل iPhone 15 Pro Max ظرفیت 256 گیگابایت",
            description="پرچمدار جدید اپل با بدنه تیتانیوم و پردازنده فوق‌سریع A17 Pro.",
            category_id=cat_mobile.id,
            brand_id=brand_apple.id
        ),
        Product(
            title="گوشی موبایل شیائومی مدل Redmi Note 13 Pro ظرفیت 256 گیگابایت",
            description="ارزش خرید بسیار بالا، دوربین 200 مگاپیکسلی و شارژر 67 واتی.",
            category_id=cat_mobile.id,
            brand_id=brand_xiaomi.id
        ),
        Product(
            title="لپ تاپ 15.6 اینچی ایسوس مدل TUF Gaming F15",
            description="لپ‌تاپ گیمینگ قدرتمند با گرافیک RTX 4060 مناسب برای بازی و رندرینگ.",
            category_id=cat_laptop.id,
            brand_id=brand_asus.id
        )
    ]
    
    db.add_all(products)
    db.commit()

    # =========================
    # ۴. ایجاد فروشندگان و قیمت‌ها (Buy Box)
    # =========================
    sellers = [
        SellerProduct(product_id=products[0].id, seller_name="دیجی‌کالا", price=18500000, stock=12, discount_percent=5),
        SellerProduct(product_id=products[0].id, seller_name="موبایل اکسپرس", price=18200000, stock=3, discount_percent=0),
        
        SellerProduct(product_id=products[1].id, seller_name="دیجی‌کالا", price=72500000, stock=5, discount_percent=2),
        
        SellerProduct(product_id=products[2].id, seller_name="تکنو لایف", price=14300000, stock=20, discount_percent=10),
        
        SellerProduct(product_id=products[3].id, seller_name="دیجی‌کالا", price=65000000, stock=8, discount_percent=0)
    ]
    
    db.add_all(sellers)
    db.commit()

    # =========================
    # ۵. ایجاد نظرات کاربران
    # =========================
    comments = [
        Comment(product_id=products[0].id, title="گوشی خیلی خوبیه", body="کیفیت صفحه نمایش و دوربینش تو این رنج قیمت بی‌نظیره.", rate=5),
        Comment(product_id=products[0].id, title="باتری ضعیف", body="گوشی خوبیه ولی باتریش با استفاده سنگین زود تموم میشه.", rate=3),
        
        Comment(product_id=products[1].id, title="شاهکار اپل", body="سرعت فوق‌العاده و وزن کمتر نسبت به نسل قبل.", rate=5),
        
        Comment(product_id=products[2].id, title="ارزش خرید بالا", body="بهترین میان‌رده بازار از نظر من. شارژر داخل جعبه هم داره.", rate=5),
        
        Comment(product_id=products[3].id, title="گیمینگ عالی", body="همه بازی‌های روز رو با بالاترین گرافیک اجرا میکنه، فقط یکم داغ میکنه.", rate=4)
    ]

    db.add_all(comments)
    db.commit()

    print("🚀 دیتابیس با موفقیت با اطلاعات استاندارد دیجی‌کالا پر شد!")

except Exception as e:
    db.rollback()
    print(f"❌ خطا در تزریق اطلاعات: {e}")

finally:
    db.close()
    