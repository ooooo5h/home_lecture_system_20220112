# 로그인/회원가입 등, 사용자 정보 관련 기능 모아두는 모듈
# DB 연결 정보를 보관하는 변수를 import 하자
from server.db_connector import DBConnector
from server.model.users import Users

db = DBConnector()

def login(params):
    sql = f"SELECT * FROM users WHERE email='{params['email']}' AND password='{params['pw']}'"
    
    login_user = db.executeOne(sql)
    
    if login_user == None:
        return {
            'code' : 400,
            'message' : '이메일 또는 비밀번호 잘못'
        }, 400
        
    return {
        'code' : 200,
        'message' : '로그인 성공',
        'data' : {
            'user' : Users(login_user).get_data_object()
        }
    }
    
def sign_up(params):
    
    sql = f"INSERT INTO users (email, password, name) VALUES ('{params['email']}','{params['pw']}','{params['name']}')"
    
    db.insertAndCommit(sql)
    
    return {
        'code' : 200,
        'message' : '회원가입 성공'
    }