from marshmallow import Schema, fields, validate, validates
from marshmallow.exceptions import ValidationError

class AdminSchema(Schema):
    username = fields.Str(
        required=True,
        validate=[
            validate.Length(min=1, max=50, error="Username must be between 1 and 50 characters"),
            validate.Regexp(
                regex=r'^[a-zA-Z0-9_-]+$',
                error="Username can only contain letters, numbers, underscores, and hyphens",
            ),
        ],
    )
    password = fields.Str(
        required=True,
        validate=[
            validate.Length(min=8, max=100, error="Password must be between 8 and 100 characters"),
        ],
    )

    @validates('password')
    def validate_password(self, value):
        if not any(char.isnumeric() for char in value):
            raise ValidationError("Password must contain at least one numeric character")

        if not any(char.isupper() for char in value):
            raise ValidationError("Password must contain at least one uppercase letter")

        if not any(char.islower() for char in value):
            raise ValidationError("Password must contain at least one lowercase letter")
