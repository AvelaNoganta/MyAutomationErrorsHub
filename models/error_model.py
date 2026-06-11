from database import Database


class ErrorModel:
    @staticmethod
    def add_error(error_name, category_id, tool_name, error_message, root_cause, solution, image_path):
        conn = Database.get_connection()
        conn.execute("""
            INSERT INTO errors (
                error_name,
                category_id,
                tool_name,
                error_message,
                root_cause,
                solution,
                image_path
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            error_name,
            category_id,
            tool_name,
            error_message,
            root_cause,
            solution,
            image_path
        ))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_errors(page=1, per_page=5):
        offset = (page - 1) * per_page
        conn = Database.get_connection()
        errors = conn.execute("""
            SELECT errors.*, categories.name AS category_name
            FROM errors
            LEFT JOIN categories ON errors.category_id = categories.id
            ORDER BY errors.id DESC
            LIMIT ? OFFSET ?
        """, (per_page, offset)).fetchall()
        conn.close()
        return errors

    @staticmethod
    def count_all_errors():
        conn = Database.get_connection()
        count = conn.execute(
            "SELECT COUNT(*) AS total FROM errors"
        ).fetchone()["total"]
        conn.close()
        return count

    @staticmethod
    def get_error_by_id(error_id):
        conn = Database.get_connection()
        error = conn.execute("""
            SELECT errors.*, categories.name AS category_name
            FROM errors
            LEFT JOIN categories ON errors.category_id = categories.id
            WHERE errors.id = ?
        """, (error_id,)).fetchone()
        conn.close()
        return error

    @staticmethod
    def search_errors(search_text, page=1, per_page=5):
        offset = (page - 1) * per_page
        conn = Database.get_connection()
        errors = conn.execute("""
            SELECT errors.*, categories.name AS category_name
            FROM errors
            LEFT JOIN categories ON errors.category_id = categories.id
            WHERE errors.error_name LIKE ?
            ORDER BY errors.id DESC
            LIMIT ? OFFSET ?
        """, (f"%{search_text}%", per_page, offset)).fetchall()
        conn.close()
        return errors

    @staticmethod
    def count_search_errors(search_text):
        conn = Database.get_connection()
        count = conn.execute("""
            SELECT COUNT(*) AS total
            FROM errors
            WHERE error_name LIKE ?
        """, (f"%{search_text}%",)).fetchone()["total"]
        conn.close()
        return count

    @staticmethod
    def get_errors_by_category(category_id, page=1, per_page=5):
        offset = (page - 1) * per_page
        conn = Database.get_connection()
        errors = conn.execute("""
            SELECT errors.*, categories.name AS category_name
            FROM errors
            LEFT JOIN categories ON errors.category_id = categories.id
            WHERE categories.id = ?
            ORDER BY errors.id DESC
            LIMIT ? OFFSET ?
        """, (category_id, per_page, offset)).fetchall()
        conn.close()
        return errors

    @staticmethod
    def count_errors_by_category(category_id):
        conn = Database.get_connection()
        count = conn.execute("""
            SELECT COUNT(*) AS total
            FROM errors
            WHERE category_id = ?
        """, (category_id,)).fetchone()["total"]
        conn.close()
        return count

    @staticmethod
    def update_error(error_id, error_name, category_id, tool_name, error_message, root_cause, solution, image_path):
        conn = Database.get_connection()
        conn.execute("""
            UPDATE errors
            SET error_name = ?,
                category_id = ?,
                tool_name = ?,
                error_message = ?,
                root_cause = ?,
                solution = ?,
                image_path = ?
            WHERE id = ?
        """, (
            error_name,
            category_id,
            tool_name,
            error_message,
            root_cause,
            solution,
            image_path,
            error_id
        ))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_error(error_id):
        conn = Database.get_connection()
        conn.execute("DELETE FROM errors WHERE id = ?", (error_id,))
        conn.commit()
        conn.close()
