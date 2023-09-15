from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Student
from app.schemas.student_schema import StudentSchema
from marshmallow import ValidationError
from app.extensions import db
from sqlalchemy.exc import IntegrityError
import traceback
from app.models import *

class StudentController:
    student_bp = Blueprint('student', __name__)

    
    @student_bp.route('/student/create', methods=['GET'])
    @jwt_required()
    def get_student():
        response = {}
        return response

    @student_bp.route('/create', methods=['POST'])
    @jwt_required()
    def create_student():
        current_user = get_jwt_identity()
        if current_user.get('is_admin'):
            data = request.get_json()
            schema = StudentSchema()
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

            student_name = data['student_name']
            year = data['year']
            department_name = data['department_name']
            department_id = data['department_id']

            existing_student = Student.query.filter_by(
                student_name=student_name,
                year=year,
                department_id=department_id,
                department_name=department_name
            ).first()

            if existing_student:
                error_response = {
                    "errorCode": 400,
                    "message": "Validation error",
                    "stackTrace": "Student with similar data already exists",
                    "validationErrors": [
                        {
                            "field": "student_name",
                            "message": "Student with similar data already exists"
                        }
                    ]
                }
                return jsonify(error_response), 400

            student = Student(
                student_name=student_name,
                year=year,
                department_id=department_id,
                department_name=department_name
            )

            db.session.add(student)
            db.session.commit()
            return jsonify({'message': 'Student created successfully'}), 201
        else:
            return jsonify({'message': 'Unauthorized'}), 403
    
    @student_bp.route('/update/<int:student_id>', methods=['PUT'])
    @jwt_required()
    def update_student(student_id):
        current_user = get_jwt_identity()
        if current_user.get('is_admin'):
            student = Student.query.get(student_id)
            if not student:
                return jsonify({'message': 'Student not found'}), 404

            data = request.get_json()
            schema = StudentSchema()
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

            student.student_name = data.get('student_name', student.student_name)
            student.year = data.get('year', student.year)
            department_name = data.get('department_name', student.department_name)

            department = Department.query.filter_by(department_name=department_name).first()

            if not department:
                return jsonify({'message': 'Invalid department name'}), 400

            if department.department_id != data.get('department_id', student.department_id):
                error_message = "The provided department_id does not correspond to the department_name."
                error_response = {
                    "errorCode": 422,
                    "message": "Validation error",
                    "stackTrace": "Validation error",
                    "validationErrors": [
                        {
                            "field": "department_id",
                            "message": error_message
                        }
                    ]
                }
                return jsonify(error_response), 422

            student.department_id = department.department_id
            student.department_name = department.department_name

            db.session.commit()
            return jsonify({'message': 'Student updated successfully'}), 200
        else:
            return jsonify({'message': 'Unauthorized'}), 403

    @student_bp.route('/delete/<int:student_id>', methods=['DELETE'])

    @jwt_required()
    def delete_student(student_id):
        current_user = get_jwt_identity()
        if current_user.get('is_admin'):
            student = Student.query.get(student_id)
            if not student:
                return jsonify({'message': 'Student not found'}), 404

            db.session.delete(student)
            db.session.commit()
            return jsonify({'message': 'Student deleted successfully'}), 200
        else:
            return jsonify({'message': 'Unauthorized'}), 403

    @student_bp.route('/get', methods=['GET'])
    @jwt_required()
    def get_all_students():
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return jsonify({'message': 'Unauthorized'}), 403

        students = Student.query.all()

        student_list = []
        for student in students:
            student_info = {
                'student_id': student.student_id,
                'student_name': student.student_name,
                'year': student.year,
                'department_name': student.department_name
            }
            student_list.append(student_info)

        return jsonify({'students': student_list}), 200


    