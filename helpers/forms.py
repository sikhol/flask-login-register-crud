from wtforms import Form, BooleanField, StringField, PasswordField, validators, TextAreaField, IntegerField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired
import email_validator

# Creating Login Form contains email and password
class LoginForm(Form):

    username = StringField("Username", validators=[validators.Length(min=7, max=50), validators.DataRequired(message="Please Fill This Field")])

    password = PasswordField("Password", validators=[validators.DataRequired(message="Please Fill This Field")])

# Creating Registration Form contains username, name, email, password and confirm password.

class RegisterForm(Form):

    name = StringField("Name", validators=[validators.Length(min=3, max=25), validators.DataRequired(message="Please Fill This Field")])

    username = StringField("Username", validators=[validators.Length(min=3, max=25), validators.DataRequired(message="Please Fill This Field")])

    email = StringField("Email", validators=[validators.Email(message="Please enter a valid email address")])
    phone = StringField("Phone", validators=[validators.Length(min=12, max=13), validators.DataRequired(message="Please Fill This Field")])
    domisili = StringField("Domisili", validators=[validators.Length(min=5, max=200), validators.DataRequired(message="Please Fill This Field")])
    industry = StringField("Industry", validators=[validators.Length(min=2, max=100), validators.DataRequired(message="Please Fill This Field")])
    password = PasswordField("Password", validators=[validators.DataRequired(message="Please Fill This Field")])


class TtsForm(Form):

    text = StringField("text", widget=TextArea(), validators=[validators.Length(min=7, max=300), validators.DataRequired(message="Please Fill This Field")])

class addBarangForm(Form):

    name = StringField("Name", validators=[validators.Length(min=1, max=25), validators.DataRequired(message="Please Fill This Field")])

    berat_barang = StringField("Berat Barang", validators=[validators.Length(min=1, max=25), validators.DataRequired(message="Please Fill This Field")])

    jenis_barang = StringField("Jenis Barang", validators=[validators.Length(min=1, max=100), validators.DataRequired(message="Please Fill This Field")])
    harga_beli = StringField("Harga Beli", validators=[validators.Length(min=1, max=13), validators.DataRequired(message="Please Fill This Field")])
    harga_jual = StringField("Harga Jual", validators=[validators.Length(min=1, max=200), validators.DataRequired(message="Please Fill This Field")])
    stok = StringField("Stok", validators=[validators.Length(min=1, max=100), validators.DataRequired(message="Please Fill This Field")])

