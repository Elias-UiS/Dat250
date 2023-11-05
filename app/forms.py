"""Provides all forms used in the Social Insecurity application.

This file is used to define all forms used in the application.
It is imported by the app package.

Example:
    from flask import Flask
    from app.forms import LoginForm

    app = Flask(__name__)

    # Use the form
    form = LoginForm()
    if form.validate_on_submit() and form.login.submit.data:
        username = form.username.data
    """

from datetime import datetime
from typing import cast

from flask_wtf.file import FileAllowed
from flask_wtf import FlaskForm


from wtforms import (
    BooleanField,
    DateField,
    FileField,
    FormField,
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField,
    validators,
)

# Defines all forms in the application, these will be instantiated by the template,
# and the routes.py will read the values of the fields

# : Add validation, maybe use wtforms.validators??

# TODO: There was some important security feature that wtforms provides, but I don't remember what; implement it


class LoginForm(FlaskForm):
    """Provides the login form for the application."""

    username = StringField(label="Username", render_kw={"placeholder": "Username"}, validators=[validators.Length(min=1, max=40, message="Input too long"), validators.Regexp(r'^[\w.@-]+$', message="Only alphanumeric characters are allowed.")])
    password = PasswordField(label="Password", render_kw={"placeholder": "Password"}, validators=[validators.Length(min=1, max=40, message="Input too long"), validators.Regexp(r'^[\w.@-]+$', message="Only alphanumeric characters are allowed.")])
    remember_me = BooleanField(
        label="Remember me"
    )  # : It would be nice to have this feature implemented, probably by using cookies
    submit = SubmitField(label="Sign In")


class RegisterForm(FlaskForm):
    """Provides the registration form for the application."""

    first_name = StringField(label="First Name", render_kw={"placeholder": "First Name"}, 
    validators=[validators.InputRequired("A first name is required"), validators.Length(min=2, max=30), validators.Regexp(r'^[\w.@+-]+$', message="Only alphanumeric characters are allowed.")])

    last_name = StringField(label="Last Name", render_kw={"placeholder": "Last Name"},
    validators=[validators.InputRequired("A last name is required"), validators.Length(min=2, max=30), validators.Regexp(r'^[\w.@+-]+$', message="Only alphanumeric characters are allowed.")])

    username = StringField(label="Username", render_kw={"placeholder": "Username"},
    validators=[validators.InputRequired("A username is required"), validators.Length(min=2, max=30), validators.Regexp(r'^[\w.@-]+$', message="Only alphanumeric characters are allowed.")])

    password = PasswordField(label="Password", render_kw={"placeholder": "Password"},
    validators=[validators.InputRequired(), validators.Length(min=3, max=30), validators.EqualTo('confirm_password', message='Passwords must match'), validators.Regexp(r'^[\w.@-]+$', message="Only alphanumeric characters are allowed.")])

    confirm_password = PasswordField(label="Confirm Password", render_kw={"placeholder": "Confirm Password"},
                                     validators=[validators.Length(min=2, max=40), validators.InputRequired(message = 'Can not be empty'), validators.Regexp(r'^[\w.@-]+$', message="Only alphanumeric characters are allowed.")])

    submit = SubmitField(label="Sign Up")


class IndexForm(FlaskForm):
    """Provides the composite form for the index page."""

    login = cast(LoginForm, FormField(LoginForm))
    register = cast(RegisterForm, FormField(RegisterForm))


class PostForm(FlaskForm):
    """Provides the post form for the application."""

    content = TextAreaField(label="New Post", render_kw={"placeholder": "What are you thinking about?"}, validators=[validators.InputRequired(message = 'Can not be empty'), validators.Length(min=1, max=200, message="Input too long"), validators.Regexp(r'^[\w.@+\- ]+$', message="Only alphanumeric characters are allowed.")])
    image = FileField(label="Image", validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField(label="Post")


class CommentsForm(FlaskForm):
    """Provides the comment form for the application."""

    comment = TextAreaField(label="New Comment", render_kw={"placeholder": "What do you have to say?"}, validators=[validators.InputRequired(message = 'Can not be empty'), validators.Length(min=1, max=200, message="Input too long"), validators.Regexp(r'^[\w.@+\- ]+$', message="Only alphanumeric characters are allowed.")])
    submit = SubmitField(label="Comment")


class FriendsForm(FlaskForm):
    """Provides the friend form for the application."""

    username = StringField(label="Friend's username", render_kw={"placeholder": "Username"}, validators=[validators.InputRequired(message = 'Can not be empty'), validators.Regexp(r'^[\w.@+-]+$', message="Only alphanumeric characters are allowed.")])
    submit = SubmitField(label="Add Friend")


class ProfileForm(FlaskForm):
    """Provides the profile form for the application."""

    education = StringField(label="Education", render_kw={"placeholder": "Highest education"}, validators=[validators.Regexp(r'^[\w.@+-]+$', message="Only alphanumeric characters are allowed."), validators.Length(min=1, max=200, message="Input too long")])
    employment = StringField(label="Employment", render_kw={"placeholder": "Current employment"}, validators=[validators.Regexp(r'^[\w.@+-]+$', message="Only alphanumeric characters are allowed."), validators.Length(min=1, max=200, message="Input too long")])
    music = StringField(label="Favorite song", render_kw={"placeholder": "Favorite song"}, validators=[validators.Regexp(r'^[\w.@+-]+$', message="Only alphanumeric characters are allowed."), validators.Length(min=1, max=200, message="Input too long")])
    movie = StringField(label="Favorite movie", render_kw={"placeholder": "Favorite movie"}, validators=[validators.Regexp(r'^[\w.@+-]+$', message="Only alphanumeric characters are allowed."), validators.Length(min=1, max=200, message="Input too long")])
    nationality = StringField(label="Nationality", render_kw={"placeholder": "Your nationality"}, validators=[validators.Regexp(r'^[\w.@+-]+$', message="Only alphanumeric characters are allowed."), validators.Length(min=1, max=200, message="Input too long")])
    birthday = DateField(label="Birthday", default=datetime.now())
    submit = SubmitField(label="Update Profile")
