from marshmallow import Schema, fields, validate, validates
from marshmallow.exceptions import ValidationError
import re

class CustomCollegeSchema(Schema):
    college_name = fields.Str(
        validate=[
            validate.Length(min=1, max=255, error="College name must be between 1 and 255 characters"),
        ],
    )

    @validates('college_name')
    def validate_college_name(self, value):
        if not value or not value.strip():
            raise ValidationError("College name is required")

        if not re.match(r'^[a-zA-Z\s\-]+$', value):
            raise ValidationError("College name can only contain letters, spaces, and hyphens")

class CollegeResponseSchema(Schema):
    message = fields.Str()
    college = fields.Nested(CustomCollegeSchema)


