import imp,os
from flask import Blueprint, render_template, request, redirect,flash
from .database import query_table, get_db, delete_by_id,insert_book
from werkzeug.utils import secure_filename
from flask import url_for
from flask_login import  login_required, current_user
views = Blueprint('view', __name__)

UPLOAD_FOLDER = "website/static/uploads"

@views.route("/")
@login_required
def homePage():
    books = query_table('books')
    return render_template('index.html', books=books, user=current_user)


@views.route("/book/<int:id>", methods=["GET", "POST"])
def book(id):
    conn = get_db()
    if request.method == "GET":
        conn = conn.cursor().execute(f"SELECT * FROM books WHERE id={id}")
        book_data = conn.fetchone()
        return render_template('book.html', book=book_data ,user=current_user)

@views.route("/admin", methods=["GET", "POST"])
def books(): # Display Books and Add
    if current_user.email == "admin@gmail.com":
        book_data = query_table("books")
        if request.method == "GET":
            return render_template("Admin/books.html",
                        custom_css="admin",
                        book_data=book_data,
                        user=current_user)
        else:
            file = request.files['cover']
            filename = secure_filename(file.filename)
            book_details = (
                filename,
                request.form['title'],
                request.form['author'],
                request.form['description']
            )
            insert_book(book_details)
            file.save(os.path.join(UPLOAD_FOLDER + "/images",filename))
            return redirect(url_for('view.books'))
    else:
        flash("Invalid Url ", category='error')
        return redirect(url_for('view.homePage'))

@views.route("/Admin/update/<int:id>", methods=["GET", "POST"]) 
def update_book(id):
    if current_user.email == "admin@gmail.com":
        conn = get_db()
        if request.method == "POST":
            cover = request.form['cover']
            title = request.form['title']
            author = request.form['author']
            description = request.form['description']
            conn.execute(f"""UPDATE books
                            SET cover='{cover}', title='{title}',author='{author}', description_book='{description}'
                            WHERE id={id}""")
            conn.commit()
            conn.close()
        elif request.method == "GET":
            conn = conn.cursor().execute(f"SELECT * FROM books WHERE id={id}")
            book_details = conn.fetchone()
            conn.close()
            return render_template('Admin/update.html',
                                    custom_css="admin",
                                    book_details=book_details,
                                    user=current_user)
        return redirect(url_for('view.books'))
    else:
        flash("Invalid Url ", category='error')
        return redirect(url_for('view.homePage'))


@views.route("/Admin/delete/<int:id>")
def delete_book(id):
    if current_user.email == "admin@gmail.com":
        delete_by_id('books', id)
    else:
        flash("Invalid Url ", category='error')
    return redirect(url_for('view.homePage'))



