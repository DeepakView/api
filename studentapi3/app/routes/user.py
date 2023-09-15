from flask import Blueprint,jsonify,request
from app.schemas.user_schema import UserSchema
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_bcrypt import Bcrypt
from marshmallow import ValidationError
from app.schemas.admin_schema import AdminSchema
from app.models import Admin, RevokedToken
from app.extensions import jwt,bcrypt
from sqlalchemy.exc import IntegrityError
from app.schemas import user_schema,StudentSchema
from app.models import *
import traceback

class UserController:
    user_bp = Blueprint('user', __name__)

    @user_bp.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        schema = UserSchema()
        errors = schema.validate(data)
        if errors:
            return jsonify(errors), 400
        username = data['username']
        password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201


    @user_bp.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        schema = UserSchema()
        errors = schema.validate(data)
        if errors:
            return jsonify(errors), 400
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            return jsonify({'access_token': access_token, 'is_admin': user.is_admin}), 200
        else:
            return jsonify({'message': 'Invalid username or password'}), 401
        


    @user_bp.route('/students', methods=['GET'])
    def get_students():
        """
        Get a list of all students.

        ---
        responses:
        200:
            description: A list of students.
            schema:
            type: array
            items:
                $ref: '#/definitions/Student'
        """
        students = Student.query.all()
        student_schema = StudentSchema(many=True)
        result = student_schema.dump(students)
        return jsonify(result), 200
    