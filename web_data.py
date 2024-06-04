from wtforms import Form
from wtforms import StringField, IntegerField, BooleanField, TextAreaField, RadioField, \
    SelectField, SelectMultipleField, DateField

from wtforms.validators import InputRequired, NumberRange
from wtforms.widgets import ListWidget, CheckboxInput


class MessageForm(Form):
    message_title = StringField(
        label="Название сообщения:",
        name="message-title",
        validators=[InputRequired(message="Вы не указали заголовок сообщения.")]
    )

    message_content = TextAreaField(label="Содержание сообщения:", name="message-content")

    message_author = SelectField(label="Автор сообщения:", name="message-author", coerce=int)
    message_recipient = SelectField(label="Получатель сообщения:", name="message-recipient", coerce=int)

    creation_date = DateField(label="Дата отправления сообщения:", name="creation-date", format="%Y-%m-%d")



class UserForm(Form):
    first_name = StringField(
        label="Имя:",
        validators=[InputRequired(message="Введите имя пользователя.")]
    )

    last_name = StringField(
        label="Фамилия:",
        validators=[InputRequired(message="Введите фамилию пользователя.")]
    )

    username = StringField(
        label="Логин:",
        validators=[InputRequired(message="Введите логин пользователя.")]
    )

    password = StringField(
        label="Пароль:",
        validators=[InputRequired(message="Введите пароль пользователя.")]
    )

    confirm_password = StringField(
        label="Подтверждение пароля:",
        validators=[InputRequired(message="Подтвердите пароль пользователя.")]
    )