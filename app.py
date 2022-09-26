"""

Developed and maintained by parth kabra (https://github.com/parth-kabra).

"""


from flask import Flask, render_template, url_for, request, session, redirect
from flask_socketio import SocketIO, send, emit
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from engineio.payload import Payload

app = Flask(__name__)
app.config["SECRET"] = "KEY"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.secret_key = "KEY"
Payload.max_decode_packets = 500
db = SQLAlchemy(app)
io = SocketIO(app, cors_allowed_origins="*")
online_users = 0

# MESSAGE MODEL FOR SQL
class Message(db.Model):

    def get_time() -> str:
        date = str(datetime.now())
        date = date[:date.rfind(" ")]
        time = datetime.today().strftime("%I:%M %p")
        return f'{date} {time}'

    id = db.Column(db.Integer, primary_key = True)
    message = db.Column(db.String(3000), nullable = False)
    date_created = db.Column(db.String, default = get_time())
    user = db.Column(db.String, nullable = False)

    def __repr__(self) -> str:
        return "<User %r>" % self.id   


# FLASK JOIN CHAT PAGE
@app.route('/', methods = ["POST", "GET"])
@app.route('/join', methods = ["POST", "GET"])
def join_chat():

    if request.method == "POST":

        name = request.form["user_name"]
        session["user"] = name

        return redirect('/chat/')

    else:

        if "user" in session:
            return render_template("join.html")
        
        else:
            return render_template("join.html")

@app.route("/terms")
def terms_and_conditions():
    return render_template("terms.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# FASK CHAT AREA PAGE
@app.route('/chat/')
def index():

    if "user" in session:
        messages = Message.query.order_by(Message.date_created).all()
        return render_template('index.html', messages = messages)
    else:
        return redirect("/")


# SOCKET CONNECT USER
@io.on("connect")
def add_user() -> None:
    global online_users
    online_users += 1
    emit("user_action", online_users, broadcast = True)


# SOCKET DISCONNECT USER
@io.on("disconnect")
def remove_user() -> None:
    global online_users
    online_users -= 1
    emit("user_action", online_users, broadcast = True)
    session.clear()


# SOCKET HANDLE MESSAGE
@io.on("message")
def handle_message(msg) -> None:
    if msg != "CONNECTED!":
        new_msg = Message(message = msg, user = session["user"])
        db.session.add(new_msg)    
        db.session.commit()
        sender = {
            "msg":msg,
            "user":session["user"]
        }
        send(sender, broadcast = True)


# SOCKET SEND TYPING MESSAGE 
@io.on("typing__signal")
def send_typing_signal(is_typing) -> None:

    if is_typing:
    
        typer = {
            "is_typing": True,
            "user":session["user"]
        }

        emit("typing", typer,  broadcast=True, include_self = False)
    else:
    
        typer = {
            "is_typing": False,
            "user":session["user"]
        }
    
        emit("typing", typer ,  broadcast=True, include_self = False)


if __name__ == '__main__':
    io.run(app,debug=True)