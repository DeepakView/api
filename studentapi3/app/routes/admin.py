from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token,get_jwt
from flask_bcrypt import Bcrypt
from marshmallow import ValidationError
from app.schemas.admin_schema import AdminSchema
from app.models import Admin, RevokedToken
from app.extensions import jwt,bcrypt
from sqlalchemy.exc import IntegrityError
from app.schemas import *
from app.models import *
import traceback


class AdminController:
    admin_bp = Blueprint('admin', __name__)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        return RevokedToken.query.filter_by(jti=jti).first() is not None

    @admin_bp.route('/register', methods=['POST'])
    def admin_register():
        data = request.get_json()
        schema = AdminSchema()
        try:
            schema.load(data)  
        except ValidationError as err:
            error_response = {
                "errorCode": 422,
                "message": "Validation error",
                "stackTrace": traceback.format_exc(),
                "validationErrors": []
            }

            for field, messages in err.messages.items():
                for message in messages:
                    error_entry = {
                        "field": field,
                        "message": message
                    }
                    error_response["validationErrors"].append(error_entry)

            return jsonify(error_response), 422

        username = data['username']
        password = data['password']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            admin = Admin(username=username, password=hashed_password)
            db.session.add(admin)
            db.session.commit()
            return jsonify({'message': 'Admin registered successfully'}), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({'message': 'Username already exists'}), 400

    @admin_bp.route('/protected', methods=['GET'])
    @jwt_required()
    def admin_protected():
        current_identity = get_jwt_identity()
        is_admin = current_identity.get('is_admin', False)
        if is_admin:
            return jsonify({'message': 'This is an admin-only route'}), 200
        else:
            return jsonify({'message': 'Unauthorized'}), 403
        
    @admin_bp.route('/login', methods=['POST'])
    def admin_login():
        data = request.get_json()
        schema = AdminSchema()
        errors = schema.validate(data)
        if errors:
            return jsonify(errors), 400
        username = data['username']
        password = data['password']

        admin = Admin.query.filter_by(username=username).first()

        if admin and bcrypt.check_password_hash(admin.password, password):
            access_token = create_access_token(identity={'admin_id': admin.admin_id, 'is_admin': True})
            return jsonify({'access_token': access_token}), 200
        else:
            return jsonify({'message': 'Invalid admin credentials'}), 401

    @admin_bp.route('/logout', methods=['POST'])
    @jwt_required()
    def admin_logout():
        jti = get_jwt()['jti']
        
        # Check if the token with the same jti has already been revoked
        existing_revoked_token = RevokedToken.query.filter_by(jti=jti).first()
        
        if existing_revoked_token:
            return jsonify({'message': 'Token already revoked'}), 400
        
        # If the token is not already revoked, add it to the revoked_token table
        revoked_token = RevokedToken(jti=jti)
        db.session.add(revoked_token)
        db.session.commit()
        
        return jsonify({'message': 'Admin logged out successfully'}), 200
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        return RevokedToken.query.filter_by(jti=jti).first() is not None










    