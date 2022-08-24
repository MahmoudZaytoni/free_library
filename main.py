import imp,os
from flask import Flask, render_template
from flask import request, redirect
from flask import url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory
from database import get_db, query_table, insert_book, delete_by_id

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key

## USER View
@app.route("/")
def homePage():
    books = query_table('books')
    return render_template('index.html', books=books)

# @app.route("/<string>")
# def book():

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/sign_up")
def sign_up():
    return render_template('sign_up.html')




## Admin View To Display books and Add book and Delete 
@app.route("/admin", methods=["GET", "POST"])
def books(): # Display Books and Add
    book_data = query_table("books")
    if request.method == "GET":
        return render_template("Admin/books.html",
                    custom_css="admin",
                    book_data=book_data)
    else:
        file = request.files['cover']
        filename = secure_filename(file.filename)
        book_details = (
            filename,
            request.form['title'],
            request.form['author'],
            request.form['description']
        )
        print (book_details)
        insert_book(book_details)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "/images",filename))
        return redirect(url_for('books'))



@app.route("/Admin/update/<int:id>", methods=["GET", "POST"]) 
def update_book(id):
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
                                book_details=book_details)
    return redirect(url_for('books'))

@app.route("/Admin/delete/<int:id>")
def delete_book(id):
    delete_by_id('books', id)
    return redirect(url_for('books'))


if __name__ == "__main__":
    app.run(debug=True)
