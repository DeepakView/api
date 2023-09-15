
from datetime import timedelta
DEBUG = True  
JWT_SECRET_KEY = '150439867145287837725026974045353157538'  
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)  


SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost:8080/mydata'
SQLALCHEMY_TRACK_MODIFICATIONS = False

