from flask import Markup
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SelectField, SubmitField, FloatField
from wtforms.validators import ValidationError, DataRequired, Regexp, NumberRange, Optional
from extensions import db
from . manage import *

class SignUpForm(FlaskForm):
    user_id = StringField(
        label=("Username"),
        validators=[
            DataRequired(),        
        ],
        render_kw={'type': 'text'}
    )

    user_password = StringField(
        label=("Password"),
        validators=[
            DataRequired(),
        ],
        render_kw={'type': 'password'}
    ) 

    user_confirm_password = StringField(
        label=("Confirm Password"),
        validators=[
        ],
        render_kw={'type': 'password'}
    )

    user_account_type = StringField(
        label=("Account type"),
        validators=[
        ],
        render_kw={'type': 'text'}
    )
    
    submit = SubmitField(label=('Submit'))

    def validate_user_id(form, field):
        if user_id_exists(field.data):
            raise ValidationError('User already exists. Try again.')

    def validate_user_confirm_password(form, field):
        if field.data != form.user_password.data:
            raise ValidationError('Password does not match. Try again.')

class SignInForm(FlaskForm):
    user_id = StringField(
        label=("Username"),
        validators=[
            DataRequired(),        
        ],
        render_kw={'type': 'text'}
    )

    user_password = StringField(
        label=("Password"),
        validators=[
            DataRequired(),
        ],
        render_kw={'type': 'password'}
    )

    submit = SubmitField(label=('Submit'))

    def validate_user_id(form, field):
        if not user_id_exists(field.data):
            raise ValidationError("The username you entered does not exist.")
    
    def validate_user_password(form, field):
        user = form.user_id.data
        if user_id_exists(user):
            if field.data != get_user_password(form.user_id.data):
                raise ValidationError("The password you entered is incorrect.")

class InformationForm(FlaskForm):
    user_profile_description = StringField(
        label=("Profile Description"),
        validators=[
        ],
        render_kw={'type': 'text'}
    )

    user_first_name = StringField(
        label = ("First Name"),
        validators = [       
        ],
        render_kw={'type': 'text'}
    )

    user_middle_name = StringField(
        label=("Middle Name"),
        validators=[
        ],
        render_kw={'type': 'text'}
    )

    user_last_name = StringField(
        label=("Last Name"),
        validators=[
        ],
        render_kw={'type': 'text'}
    )

    user_birthdate = DateField(
        label=("Birth Date"),
        validators=[Optional()
        ],
        render_kw={'type': 'date'}
    )

    user_sex = SelectField(
        label=('Sex'),
        choices=[
            ('', '-- Select --'),
            ('M', 'Male'),
            ('F', 'Female')
            ],
        validators=[
        ],
        render_kw={}
        )

    user_contact_number = StringField(
        label=("Contact Number"),
        validators=[
        ],
        render_kw={'type': 'text'}
    )

    user_address_street = StringField(
        label = ("Street"),
        validators=[
        ],
        render_kw={'type': 'text'}
    )

    user_address_barangay = StringField(
        label=("Barangay"),
        validators  =[
        ],
        render_kw={'type': 'text'}
    )

    user_address_city = StringField(
        label=("City / Municipality"),
        validators=[
        ],
        render_kw = {'type': 'text'}
    )

    user_address_province = StringField(
        label=("Province"),
        validators=[
        ],
        render_kw={'type': 'text'}
    )

    user_address_country = StringField(
        label=("Country"),
        validators=[
        ],
        render_kw={'type': 'text'}
    )

    user_zip_code = StringField(
        label=("Zip Code"),
        validators=[
        ],
        render_kw={'type': 'text'}
    )

    user_education = StringField(
        label=("Education"),
        validators=[
        ],
        render_kw={'type': 'text'}
    )

    user_email = StringField(
        label=("Email"),
        validators=[
        ],
        render_kw={'type': 'text'}
    )

    user_phone_number = StringField(
        label=("Phone Number"),
        validators=[
        ],
        render_kw={'type': 'text'}
    )

class ClientFillUpForm(InformationForm):
    submit = SubmitField(label=('Submit'))

class ClientEditForm(InformationForm):
    edit = SubmitField(label=('Edit'))

class ServiceProviderFillUpForm(InformationForm):
    submit = SubmitField(label=('Submit'))

class ServiceProviderEditForm(InformationForm):
    edit = SubmitField(label=('Edit'))

class RequestPostInfoForm(FlaskForm):
    request_post_title = StringField(
        label=("Title"),
        validators=[
            DataRequired(),
        ],
        render_kw={'type': 'text'}
    )

    request_post_description = StringField(
        label=("Description"),
        validators=[
            DataRequired(),
        ],
        render_kw={'type': 'text'}
    )

    request_post_service_type = SelectField(
        label=('Service Type'),
        choices=[
            ('', '-- Select --'),
            ],
        validators=[
            DataRequired(),
        ],
        render_kw={}
    )

    request_post_location = StringField(
        label=("Location"),
        validators=[
            DataRequired(),
        ],
        render_kw={'type': 'text'}
    )

    request_post_schedule = DateField(
        label=("Schedule"),
        validators=[
            DataRequired(),
        ],
        render_kw={'type': 'date'}
    )

    request_post_amount = FloatField(
        label=('Amount'),
        validators=[
            DataRequired(),
            ],
        render_kw={'type': 'number'}
    )

class RequestPostAddForm(RequestPostInfoForm):
    submit = SubmitField(label=('Submit'))

class RequestPostEditForm(RequestPostInfoForm):
    edit = SubmitField(label=('Edit'))

class ServicePostInfoForm(FlaskForm):
    service_post_title = StringField(
        label=("Title"),
        validators=[
            DataRequired(),
        ],
        render_kw={'type': 'text'}
    )

    service_post_description = StringField(
        label=("Description"),
        validators=[
            DataRequired(),
        ],
        render_kw={'type': 'text'}
    )

    service_post_service_type = SelectField(
        label=('Service Type'),
        choices=[
            ('', '-- Select --'),
            ],
        validators=[
            DataRequired(),
        ],
        render_kw={}
    )

    service_post_location = StringField(
        label=("Location"),
        validators=[
            DataRequired(),
        ],
        render_kw={'type': 'text'}
    )

    service_post_schedule = DateField(
        label=("Schedule"),
        validators=[
            DataRequired(),
        ],
        render_kw={'type': 'date'}
    )

    service_post_amount = FloatField(
        label=('Amount'),
        validators=[
            DataRequired(),
            ],
        render_kw={'type': 'number'}
    )

class ServicePostAddForm(ServicePostInfoForm):
    submit = SubmitField(label=('Submit'))

class ServicePostEditForm(ServicePostInfoForm):
    edit = SubmitField(label=('Edit'))
