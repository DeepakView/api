from flask import Blueprint

admin_bp = Blueprint('admin', __name__, template_folder='templates', static_folder='static')
user_bp = Blueprint('user', __name__, template_folder='templates', static_folder='static')
college_bp = Blueprint('college', __name__, template_folder='templates', static_folder='static')
student_bp = Blueprint('student', __name__, template_folder='templates', static_folder='static')

