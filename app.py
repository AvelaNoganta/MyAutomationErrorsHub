import os
import uuid
import math
import sqlite3
from flask import Flask, request, render_template, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename

from database import Database
from models.category_model import CategoryModel
from models.error_model import ErrorModel

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
PER_PAGE = 5

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def delete_image_file(filename):
    if filename:
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        if os.path.exists(file_path):
            os.remove(file_path)


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/")
def home():
    search = request.args.get("search", "").strip()
    page = request.args.get("page", 1, type=int)
    categories = CategoryModel.get_all_categories()

    if search:
        errors = ErrorModel.search_errors(search, page, PER_PAGE)
        total_errors = ErrorModel.count_search_errors(search)
    else:
        errors = ErrorModel.get_all_errors(page, PER_PAGE)
        total_errors = ErrorModel.count_all_errors()

    total_pages = math.ceil(total_errors / PER_PAGE) if total_errors > 0 else 1

    return render_template(
        "home.html",
        errors=errors,
        search=search,
        categories=categories,
        page=page,
        total_pages=total_pages
    )


@app.route("/add", methods=["GET", "POST"])
def add_error():
    categories = CategoryModel.get_all_categories()

    if request.method == "POST":
        error_name = request.form.get("error_name", "").strip()
        category_id = request.form.get("category_id", "").strip()
        tool_name = request.form.get("tool_name", "").strip()
        error_message = request.form.get("error_message", "").strip()
        root_cause = request.form.get("root_cause", "").strip()
        solution = request.form.get("solution", "").strip()

        image = request.files.get("image")
        image_path = None

        if image and image.filename:
            if allowed_file(image.filename):
                filename = f"{uuid.uuid4().hex}_{secure_filename(image.filename)}"
                save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                image.save(save_path)
                image_path = filename

        ErrorModel.add_error(
            error_name=error_name,
            category_id=category_id,
            tool_name=tool_name,
            error_message=error_message,
            root_cause=root_cause,
            solution=solution,
            image_path=image_path
        )

        return redirect(url_for("home"))

    return render_template("add_error.html", categories=categories)


@app.route("/categories", methods=["GET", "POST"])
def manage_categories():
    error_message = None

    if request.method == "POST":
        category_name = request.form.get("category_name", "").strip()

        if category_name:
            try:
                CategoryModel.add_category(category_name)
                return redirect(url_for("manage_categories"))
            except sqlite3.IntegrityError:
                error_message = "Category already exists."

    categories = CategoryModel.get_all_categories()
    return render_template(
        "categories.html",
        categories=categories,
        error_message=error_message
    )


@app.route("/edit/<int:error_id>", methods=["GET", "POST"])
def edit_error(error_id):
    error = ErrorModel.get_error_by_id(error_id)
    categories = CategoryModel.get_all_categories()

    if not error:
        return "<h3>Error not found.</h3><a href='/'>Back Home</a>"

    if request.method == "POST":
        error_name = request.form.get("error_name", "").strip()
        category_id = request.form.get("category_id", "").strip()
        tool_name = request.form.get("tool_name", "").strip()
        error_message = request.form.get("error_message", "").strip()
        root_cause = request.form.get("root_cause", "").strip()
        solution = request.form.get("solution", "").strip()
        remove_image = request.form.get("remove_image")

        current_image_path = error["image_path"]
        new_image_path = current_image_path

        if remove_image == "yes" and current_image_path:
            delete_image_file(current_image_path)
            new_image_path = None

        image = request.files.get("image")
        if image and image.filename and allowed_file(image.filename):
            if current_image_path and new_image_path == current_image_path:
                delete_image_file(current_image_path)

            filename = f"{uuid.uuid4().hex}_{secure_filename(image.filename)}"
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image.save(save_path)
            new_image_path = filename

        ErrorModel.update_error(
            error_id=error_id,
            error_name=error_name,
            category_id=category_id,
            tool_name=tool_name,
            error_message=error_message,
            root_cause=root_cause,
            solution=solution,
            image_path=new_image_path
        )

        return redirect(url_for("home"))

    return render_template(
        "edit_error.html",
        error=error,
        categories=categories
    )


@app.route("/delete/<int:error_id>")
def delete_error(error_id):
    error = ErrorModel.get_error_by_id(error_id)

    if not error:
        return "<h3>Error not found.</h3><a href='/'>Back Home</a>"

    if error["image_path"]:
        delete_image_file(error["image_path"])

    ErrorModel.delete_error(error_id)
    return redirect(url_for("home"))


@app.route("/category/<int:category_id>")
def view_category(category_id):
    page = request.args.get("page", 1, type=int)
    category = CategoryModel.get_category_by_id(category_id)

    if not category:
        return "<h3>Category not found.</h3><a href='/'>Back Home</a>"

    errors = ErrorModel.get_errors_by_category(category_id, page, PER_PAGE)
    total_errors = ErrorModel.count_errors_by_category(category_id)
    total_pages = math.ceil(total_errors / PER_PAGE) if total_errors > 0 else 1

    return render_template(
        "category.html",
        category=category,
        errors=errors,
        page=page,
        total_pages=total_pages
    )


if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    Database.init_db()
    app.run(debug=True)