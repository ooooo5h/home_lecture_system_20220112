# 플라스크 자체를 로딩하자
from flask import Flask

def created_app():
    app = Flask(__name__)
    
    return app