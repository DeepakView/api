from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from app.routes.admin import AdminController
from app.routes.colleges import CollegeController
from app.routes.user import UserController
from app.routes.student import StudentController
from app.extensions import db
from app.models import *



app = Flask(__name__)

app.config.from_object('config')


db.init_app(app)
jwt = JWTManager(app)


app.register_blueprint(AdminController.admin_bp, url_prefix='/admin')
app.register_blueprint(UserController.user_bp, url_prefix='/user')
app.register_blueprint(CollegeController.college_bp, url_prefix='/college')
app.register_blueprint(StudentController.student_bp, url_prefix='/student')


