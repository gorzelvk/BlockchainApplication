from wtforms import Form, StringField, PasswordField, DecimalField, IntegerField, TextAreaField, validators


class RegisterForm(Form):
    name = StringField('Full Name', [validators.Length(min=1, max=50)])
    email = StringField('Email Address', [validators.Length(min=3, max=50)])
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')
