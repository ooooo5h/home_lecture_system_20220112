# 플라스크 자체를 로딩하자
from flask import Flask

from server.db_connector import DBConnector

# DB연결 정보를 관리하는 클래스 생성해서 그 객체를 변수에 담자
db = DBConnector()

def created_app():
    app = Flask(__name__)
    
    return app