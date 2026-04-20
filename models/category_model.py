from database import Database


class CategoryModel:
    @staticmethod
    def get_all_categories():
        conn = Database.get_connection()
        categories = conn.execute(
            "SELECT * FROM categories ORDER BY name"
        ).fetchall()
        conn.close()
        return categories

    @staticmethod
    def get_category_by_id(category_id):
        conn = Database.get_connection()
        category = conn.execute(
            "SELECT * FROM categories WHERE id = ?",
            (category_id,)
        ).fetchone()
        conn.close()
        return category

    @staticmethod
    def add_category(name):
        conn = Database.get_connection()
        conn.execute(
            "INSERT INTO categories (name) VALUES (?)",
            (name,)
        )
        conn.commit()
        conn.close()