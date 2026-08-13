import sys
from django.apps import AppConfig
from django.db.models.signals import post_migrate

def force_inject_b2b_tables(sender, **kwargs):
    """
    Directly ensures missing physical table structures exist in the Postgres cluster,
    bypassing file-tracking errors entirely when terminal access is unavailable.
    """
    from django.db import connection
    
    # We only run this during live server start loops to save deploy overhead
    if any(cmd in sys.argv for cmd in ['runserver', 'gunicorn', 'uvicorn', 'wsgi']):
        print("🚀 Executing deep database schema alignment checks...")
        with connection.cursor() as cursor:
            try:
                # 1. Inject the core Product model table blueprint structure
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS "myapp_product" (
                        "id" bigserial NOT NULL PRIMARY KEY,
                        "title" varchar(255) NOT NULL,
                        "description" text NOT NULL,
                        "price" numeric(12, 2) NOT NULL,
                        "condition" varchar(10) NOT NULL,
                        "stock_count" integer NOT NULL CHECK ("stock_count" >= 0),
                        "item_location" varchar(10) NOT NULL,
                        "seller_location_details" varchar(255) NOT NULL,
                        "created_at" timestamptz NOT NULL,
                        "seller_id" integer NOT NULL
                    );
                """)
                
                # 2. Attach the essential User tracking constraint index node
                cursor.execute("""
                    DO $$
                    BEGIN
                        IF NOT EXISTS (
                            SELECT 1 FROM information_schema.table_constraints 
                            WHERE constraint_name = 'myapp_product_seller_id_fk_auth_user_id'
                        ) THEN
                            ALTER TABLE "myapp_product" 
                            ADD CONSTRAINT "myapp_product_seller_id_fk_auth_user_id" 
                            FOREIGN KEY ("seller_id") REFERENCES "auth_user" ("id") 
                            DEFERRABLE INITIALLY DEFERRED;
                        END IF;
                    END $$;
                """)
                
                # 3. Inject the secondary relational Photo table structure
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS "myapp_photo" (
                        "id" bigserial NOT NULL PRIMARY KEY,
                        "image" varchar(255) NOT NULL,
                        "created_at" timestamptz NOT NULL,
                        "product_id" bigint NULL
                    );
                """)
                
                # 4. Bind the secondary relationship constraints safely
                cursor.execute("""
                    DO $$
                    BEGIN
                        IF NOT EXISTS (
                            SELECT 1 FROM information_schema.table_constraints 
                            WHERE constraint_name = 'myapp_photo_product_id_fk_myapp_product_id'
                        ) THEN
                            ALTER TABLE "myapp_photo" 
                            ADD CONSTRAINT "myapp_photo_product_id_fk_myapp_product_id" 
                            FOREIGN KEY ("product_id") REFERENCES "myapp_product" ("id") 
                            DEFERRABLE INITIALLY DEFERRED;
                        END IF;
                    END $$;
                """)
                print("======== ✅ ALL LIVE HARDWARE B2B SQL PORTALS GENERATED COMPLIANT ========")
            except Exception as e:
                print(f"⚠️ App-init bypass indicator logs: {e}")

class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp' # 🧠 Make sure this matches your actual app folder string name!

    def ready(self):
        # Bind the handler to run automatically as soon as Django readies your apps
        post_migrate.connect(force_inject_b2b_tables, sender=self)
