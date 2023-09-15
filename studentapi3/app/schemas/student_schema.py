from marshmallow import Schema, fields, validate, validates
from marshmallow.exceptions import ValidationError

class StudentSchema(Schema):
    student_name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=1, max=255, error="Student name must be between 1 and 255 characters"),
            validate.Regexp(
                regex=r'^[a-zA-Z\s\-]+$',
                error="Student name can only contain letters, spaces, and hyphens",
            ),
            validate.NoneOf([' '], error="Student name cannot be empty or contain only spaces"),
        ],
    )

    year = fields.Str(
        required=True,
        validate=[
            validate.OneOf(['1st Year', '2nd Year', '3rd Year'], error="Invalid year"),
        ],
    )

    department_id = fields.Int(
        required=True,
        error_messages={"required": "Department ID is required"},
    )

    department_name = fields.Str(
        required=True,
        error_messages={"required": "Department name is required"},
    )

    @validates('department_id')
    def validate_department_id(self, value):
        if value <= 0:
            raise ValidationError("Invalid department ID")
