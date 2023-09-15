from marshmallow import Schema, fields, validate, validates
from marshmallow.exceptions import ValidationError
class UserSchema(Schema):
    
    username = fields.String(required=True, validate=validate.Length(min=1, max=50))
    password = fields.String(required=True, validate=validate.Length(min=1, max=100))
    is_admin = fields.Boolean()