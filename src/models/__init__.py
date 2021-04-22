from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# initialize our db
db = SQLAlchemy()
bcrypt = Bcrypt()

from .ArticleModel import ArticleModel, ArticleSchema
from .UserModel import UserModel, UserSchema