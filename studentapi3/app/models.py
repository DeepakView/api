from app.extensions import db


class College(db.Model):
    __tablename__ = 'College'

    college_id = db.Column(db.Integer, primary_key=True)
    college_name = db.Column(db.String(255), nullable=False)


class Department(db.Model):
    __tablename__ = 'Department'

    department_id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(255), nullable=False)
    college_id = db.Column(db.Integer, db.ForeignKey('College.college_id'))


    college = db.relationship('College', backref='departments')


class Student(db.Model):
    __tablename__ = 'Student'

    student_id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Enum('1st Year', '2nd Year', '3rd Year'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('Department.department_id'))
    department_name = db.Column(db.String(255))

    department = db.relationship('Department', backref='students')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Admin(db.Model):
    __tablename__ = 'Admin'

    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class RevokedToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), unique=True, nullable=False)