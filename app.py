from flask import Flask, render_template, url_for, request, session, redirect
from flask_socketio import SocketIO, send, emit
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET"] = "KEY"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.secret_key = "KEY"


db = SQLAlchemy(app)
io = SocketIO(app, cors_allowed_origins="*")


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


@app.route('/', methods = ["POST", "GET"])
def join_chat():

    if request.method == "POST":

        name = request.form["user_name"]
        session["user"] = name

        return redirect('/chat/')

    else:
        return render_template("join.html")

@app.route('/chat/')
def index(msg = ""):

    if "user" in session:
        messages = Message.query.order_by(Message.date_created).all()
        return render_template('index.html', messages = messages)
    else:
        return redirect("/")

@io.on("message")
def handle_message(msg) -> None:
    if msg != "CONNECTED!":
        new_msg = Message(message = msg, user = session["user"])
        db.session.add(new_msg)    
        db.session.commit()
        send({"msg":msg, "user":session["user"]}, broadcast = True)

@io.on("typing__signal")
def send_typing_signal(is_typing) -> None:
    if is_typing:
        emit("typing", True,  broadcast=True, include_self = False)
    else:
        emit("typing", False ,  broadcast=True, include_self = False)

if __name__ == '__main__':
    #app.run(host='127.0.0.1', port=8000, debug=True)
    io.run(app,debug=True)