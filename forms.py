from wtforms import Form, StringField, PasswordField, DecimalField, IntegerField, TextAreaField, validators


class RegisterForm(Form):
    name = StringField('Full Name', [validators.Length(min=1, max=50)])
    email = StringField('Email Address', [validators.Length(min=5, max=50)])
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')


class SendMoneyForm(Form):
    email = StringField('Email', [validators.Length(min=4, max=30)])
    amount = StringField('Amount', [validators.Length(min=1, max=30)])


class BuyForm(Form):
    amount = StringField('Amount', [validators.Length(min=1, max=30)])
