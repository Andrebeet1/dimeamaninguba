# check_db.py
from app import app, db

def check_tables():
    with app.app_context():
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print("📋 Tables trouvées dans la base :", tables)

        # Vérifie que toutes existent
        expected = ["users", "membres", "dimes", "notifications"]
        for t in expected:
            if t in tables:
                print(f"✅ Table '{t}' OK")
            else:
                print(f"❌ Table '{t}' MANQUANTE")

if __name__ == "__main__":
    check_tables()
