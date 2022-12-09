from wtforms import Form, StringField, DecimalField, IntegerField, TextAreaField, PasswordField, validators


class RegisterForm(Form):
    name = StringField('Full Name', [validators.length(min=5, max=30)])
    username = StringField('Username', [validators.length(min=5, max=30)])
    email = StringField('Email', [validators.length(min=5, max=30)])
    password = PasswordField('Password', [
        validators.data_required(),
        validators.length(min=5, max=30),
        validators.EqualTo('confirm_password', message='Passwords do not match')
        ])
    confirm_password = PasswordField('Confirm password')