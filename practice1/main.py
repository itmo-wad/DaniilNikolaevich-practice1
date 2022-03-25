import hashlib
import os
import uuid

from flask import Flask, render_template, redirect, make_response, request, send_from_directory, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import secure_filename

from database_setup import User, Notebook, Chat

engine = create_engine('postgresql+psycopg2://wad-adm:StrongPassw0rd@127.0.0.1:55437/wad_db')
Session = sessionmaker(bind=engine)
session = Session()  # type: sqlalchemy.orm.Session

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\ewhjdlekln\xec]/'
UPLOAD_FOLDER = 'static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = ['jpg', 'png']


@app.route("/")
def root():
    """root page"""
    token = request.cookies.get('token')
    result = session.query(User).where(User.token == token).all()
    if not result:
        return redirect("/signin")
    result = result[0]
    return render_template("root_page.html", username=result.username)


@app.route("/secret_page")
def secret_page():
    """secret page"""
    token = request.cookies.get('token')
    result = session.query(User).where(User.token == token).all()
    if not result:
        return redirect("/signup")
    return render_template("secret_page.html")


@app.route("/logout")
def logout():
    """logout"""
    resp = make_response(redirect("/"))
    resp.set_cookie("token", "")
    return resp


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    """Register User"""
    if request.method == "GET":
        return render_template("signup.html")
    else:
        data = request.form
        username = data.get("username")
        password = data.get("password")
        password_hash = hashlib.md5(password.encode("utf-8")).hexdigest()
        result = session.query(User).where(User.username == username).all()
        if result:
            flash("You can't use this username, choose another one")
            return redirect("/signup")

        if not username or not password:
            flash("Data for registration is not full")
            return redirect("/signup")

        token = str(uuid.uuid4())

        new_user = User(username=username, password=password_hash, token=token)
        session.add(new_user)
        session.commit()

        resp = make_response(redirect("/secret_page"))
        resp.set_cookie("token", token)
        return resp


@app.route("/signin", methods=['GET', 'POST'])
def signin():
    """Login user"""
    if request.method == "GET":
        return render_template("signin.html")
    else:
        data = request.form
        username = data.get("username")
        password = data.get("password")
        password_hash = hashlib.md5(password.encode("utf-8")).hexdigest()
        if not username or not password:
            flash("Username or Password is absent")
            return redirect("/signin")

        result = session.query(User).where(User.username == username, User.password == password_hash).all()
        if not result:
            flash("Invalid Email or Password")
            return redirect("/signin")
        else:
            resp = make_response(redirect("/"))
            resp.set_cookie("token", result[0].token)
            return resp


@app.route("/upload", methods=['POST', 'GET'])
def upload():
    """Upload files, Get upload.html"""
    if request.method == "POST":
        if 'file' in request.files:
            file = request.files['file']
            if file:
                filename = secure_filename(file.filename)
                extension = file.filename.split('.')[1]
                if extension not in ALLOWED_EXTENSIONS:
                    flash("Not allowed extension")
                    return redirect("/upload")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                return redirect(f"/uploaded/{filename}")
            else:
                flash("You did not provide any file")
                return redirect("/upload")
        else:
            flash("You did not provide any file")
            return redirect("/upload")
    else:
        return render_template("upload.html")


@app.route("/uploaded/<filename>", methods=['GET'])
def uploaded(filename):
    """Serve downloaded files"""
    return send_from_directory('static/upload', filename)


@app.route("/notebook", methods=['GET', 'POST'])
def notebook():
    """Notebook"""
    token = request.cookies.get('token')
    result = session.query(User).where(User.token == token).all()
    if not result:
        return redirect("/signin")
    user_id = result[0].id
    if request.method == "GET":
        all_user_notes = []
        existed_notes = session.query(Notebook).where(Notebook.user_id == user_id).all()
        for note in existed_notes:
            all_user_notes.append([note.title, note.text])
        return render_template("notebook.html", existed_notes=all_user_notes)
    else:
        data = request.form
        title = data.get("title")
        text = data.get("text")

        new_note = Notebook(user_id=user_id, title=title, text=text)
        session.add(new_note)
        session.commit()

        all_user_notes = []
        existed_notes = session.query(Notebook).where(Notebook.user_id == user_id).all()
        for note in existed_notes:
            all_user_notes.append([note.title, note.text])
        return render_template("notebook.html", existed_notes=all_user_notes)


@app.route("/notebook/flush", methods=["POST"])
def notebook_flush():
    """Clear Notebook history"""
    token = request.cookies.get('token')
    result = session.query(User).where(User.token == token).all()
    if not result:
        return redirect("/signin")
    user_id = result[0].id
    session.query(Notebook).where(Notebook.user_id == user_id).delete()
    session.commit()
    return redirect("/notebook")


@app.route("/chatbot", methods=['GET', 'POST'])
def chatbot():
    """Chatbot"""
    token = request.cookies.get('token')
    result = session.query(User).where(User.token == token).all()
    if not result:
        return redirect("/signin")
    user_id = result[0].id
    if request.method == "GET":
        all_messages = []
        existed_messages = session.query(Chat).where(Chat.user_id == user_id).all()
        for message in existed_messages:
            all_messages.append([message.text, message.bot_answer])
        return render_template("chatbot.html", all_messages=all_messages)
    else:
        data = request.form
        text = data.get("text")
        if text.lower() == "hello":
            bot_answer = "Hi there!"
        elif text.lower() == "how are you?":
            bot_answer = "I am fine, and you?"
        elif text.lower() == "bye":
            bot_answer = "Hi"
        else:
            bot_answer = "I can't process this text :(("
        new_message = Chat(user_id=user_id, text=text, bot_answer=bot_answer)
        session.add(new_message)
        session.commit()

        all_messages = []
        existed_messages = session.query(Chat).where(Chat.user_id == user_id).all()
        for message in existed_messages:
            all_messages.append([message.text, message.bot_answer])
        return render_template("chatbot.html", all_messages=all_messages)


@app.route("/chatbot/flush", methods=["POST"])
def chatbot_flush():
    """Clear chat history"""
    token = request.cookies.get('token')
    result = session.query(User).where(User.token == token).all()
    if not result:
        return redirect("/signin")
    user_id = result[0].id
    session.query(Chat).where(Chat.user_id == user_id).delete()
    session.commit()
    return redirect("/chatbot")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=50000, debug=True)
