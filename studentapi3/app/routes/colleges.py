from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity,get_jwt
from app.models import College
from app.schemas.college_schema import CustomCollegeSchema, CollegeResponseSchema
from marshmallow import ValidationError
from app.extensions import db
from sqlalchemy.exc import IntegrityError
from app.models import RevokedToken
from app.extensions import JWTManager
from functools import wraps


jwt = JWTManager()
def check_token_revocation(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        jti = get_jwt()['jti']
        if RevokedToken.query.filter_by(jti=jti).first():
            return jsonify({'message': 'Token revoked'}), 401
        return fn(*args, **kwargs)
    return wrapper

class CollegeController:
    college_bp = Blueprint('college', __name__)

    @college_bp.route('/add', methods=['POST'])
    @jwt_required()
    def create_college():
        current_user = get_jwt_identity()
        if current_user.get('is_admin'):
            data = request.get_json()
            try:
                college_data = CustomCollegeSchema().load(data)
                
                if 'college_name' in college_data:
                    college_name = college_data['college_name']

                    college = College(college_name=college_name)
                    db.session.add(college)
                    db.session.commit()

                    result = CollegeResponseSchema().dump({'message': 'College created successfully', 'college': college})

                    return jsonify(result), 201
                else:
                    raise ValidationError({
                        "Validation_errors": [
                            {
                                "college_name": {
                                    "reasons": ["College name is required"]
                                }
                            }
                        ],
                        "message": "Validation error"
                    })
            except IntegrityError:
                db.session.rollback()
                raise ValidationError({
                    "Validation_errors": [
                        {
                            "college_name": {
                                "reasons": ["College with the same name already exists"]
                            }
                        }
                    ],
                    "message": "Validation error"
                })
            except ValidationError as err:
                raise err  
        else:
            return jsonify({'message': 'Unauthorized'}), 403
