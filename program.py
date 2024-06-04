import datetime as dt

from schema import factory, User, Message, Cookie
from web_data import MessageForm, UserForm
from flask import Flask, request, render_template, redirect, make_response
import random
import string


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


app = Flask(__name__)


@app.errorhandler(404)
def router_not_found(e):
    return render_template('page-not-found.html')


@app.route('/')
@app.route('/sent')
def show_all_news():
    result = session.query(Message)
    return render_template('send.html', messages=result)


@app.route('/register', methods=["GET", "POST"])
def register():
    user_form = UserForm()

    if request.method == "GET":
        return render_template('register.html', f=user_form)

    if request.method == "POST":
        user_form.process(request.form)

        if not user_form.validate():
            return render_template('register.html', f=user_form)

        new_user = User()
        new_user.first_name = user_form.first_name.data
        new_user.last_name = user_form.last_name.data
        new_user.username = user_form.username.data
        new_user.password = user_form.password.data

        if user_form.password.data != user_form.confirm_password.data:
            return render_template('register.html', f=user_form, error="Пароли не совпадают.")

        try:
            session.add(new_user)
            session.commit()
            return redirect('/login')
        except Exception as e:
            session.rollback()
            return f"Что-то пошло не так. Ошибка: {e}"


@app.route('/login', methods=["GET", "POST"])
def login():
    a = request.cookies.get("bla-bla-bla")
    user = session.query(User).join(Cookie).filter(Cookie.cookie == a).first()
    if user is None:
        user_form = UserForm()

        if request.method == "GET":
            return render_template('login.html', f=user_form)

        if request.method == "POST":
            user_form.process(request.form)
            user_username = user_form.username.data
            user_password = user_form.password.data
            user = session.query(User).filter((User.username == user_username) & (User.password == user_password)).first()
            try:
                m = user.received_messages
                response = make_response(render_template("inbox.html", messages=m))

                new_cookie = randomword(10)
                response.set_cookie("bla-bla-bla", new_cookie)
                c = Cookie(cookie=new_cookie, user_id=user.id)
                session.add(c)
                session.commit()
                return response
            except Exception as e:
                session.rollback()
                return f"Что-то пошло не так. Ошибка: {e}"
    else:
        return "Вы уже вошли"


@app.route('/logout', methods=["GET"])
def logout():
    if "bla-bla-bla" in request.cookies:
        a = request.cookies.get("bla-bla-bla")
        cookie = session.query(Cookie).filter(Cookie.cookie == a).first()
        session.delete(cookie)
        session.commit()
        return "Вы вышли"


# html
@app.route('/send', methods=["GET"])
def send():
    a = request.cookies.get("bla-bla-bla")
    user = session.query(User).join(Cookie).filter(Cookie.cookie == a).first()
    if user is not None:
        send_messages = session.query(Message).filter(Message.author_id == user.id).all()
        return render_template('send.html', user=user, messages=send_messages)
    else:
        return "Вы не вошли в систему"


# html
@app.route('/inbox', methods=["GET"])
def inbox():
    a = request.cookies.get("bla-bla-bla")
    user = session.query(User).join(Cookie).filter(Cookie.cookie == a).first()
    if user is not None:
        inbox_messages = session.query(Message).filter(Message.recipient_id == user.id).all()
        return render_template('inbox.html', user=user, messages=inbox_messages)
    else:
        return "Вы не вошли в систему"


@app.route('/new-message', methods=['GET', 'POST'])
def new_message():
    a = request.cookies.get("bla-bla-bla")
    user = session.query(User).join(Cookie).filter(Cookie.cookie == a).first()
    if user is not None:
        all_users = session.query(User)
        print(user.id)
        message_form = MessageForm()

        message_form.message_recipient.choices = [
            (u.id, f'{u.first_name} {u.last_name} ({u.username})') for u in all_users
        ]

        if request.method == "GET":
            message_form.creation_date.data = dt.datetime.now()
            return render_template('add-message-page.html', f=message_form)

        if request.method == 'POST':
            message_form.process(request.form)
            new_message1 = Message()
            new_message1.title = message_form.message_title.data
            new_message1.content = message_form.message_content.data
            new_message1.recipient_id = message_form.message_recipient.data
            new_message1.author_id = user.id
            if message_form.creation_date.data is not None:
                new_message1.created_on = message_form.creation_date.data
            try:
                session.add(new_message1)
                session.commit()
                return redirect('/send')
            except Exception as e:
                session.rollback()
                return f"Что-то пошло не так. Ошибка: {e}"
    else:
        return "Вы не вошли в систему"
#
#
#
#
#
#             recipient_id = int(request.form['recipient_id'])
#             title = request.form['title']
#             content = request.form['content']
#
#             recipient = session.query(User).filter_by(id=recipient_id).first()
#
#             if not recipient:
#                 session.close()
#                 return 'Invalid recipient.'
#
#             new_message = Message(title=title, content=content, author=user, recipient=recipient)
#             session.add(new_message)
#             session.commit()
#             session.close()
#
#             return redirect('/inbox')
#
#         users = session.query(User).all()
#         session.close()
#         return render_template('new_message.html', user=user, users=users)
#
#     return redirect('/login')


@app.route('/edit-user', methods=["GET", "POST"])
def edit_user():
    a = request.cookies.get("bla-bla-bla")
    user = session.query(User).join(Cookie).filter(Cookie.cookie == a).first()
    print(user)
    if user is not None:
        user_form = UserForm()
        if request.method == "GET":
            user_form.first_name.data = user.first_name
            user_form.username.data = user.username
            user_form.password.data = user.password

            return render_template("edit-user.html", user_id=user.id, f=user_form)

        if request.method == "POST":
            user_form.process(request.form)

            user.first_name = user_form.first_name.data
            user.username = user_form.username.data
            user_form.password.data = user.password

            try:
                session.commit()
                return redirect('/send')
            except Exception as e:
                session.rollback()
                return f"Что-то пошло не так. Ошибка: {e}"
    else:
        return "Вы не вошли в систему"


if __name__ == "__main__":
    session = factory()
    app.run(host="127.0.0.1", port=4321)