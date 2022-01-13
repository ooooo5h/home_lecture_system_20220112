# 로그인/회원가입 등, 사용자 정보 관련 기능 모아두는 모듈
# DB 연결 정보를 보관하는 변수를 import 하자
from server.model.users import Users
from server import db

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
    
    # 이메일이 중복이면 가입 불허
    sql = f"SELECT * FROM users WHERE email = '{params['email']}'"
    
    email_check_result = db.executeOne(sql)
    
    if email_check_result:
        return {
            'code' : 400,
            'message' : '중복된 이메일입니다.'
        }, 400
    
    
    sql = f"INSERT INTO users (email, password, name) VALUES ('{params['email']}','{params['pw']}','{params['name']}')"
    
    db.insertAndCommit(sql)
    
    return {
        'code' : 200,
        'message' : '회원가입 성공'
    }
    
# 이메일 받아서 사용자 정보 조회
def find_user_by_email(params):
    
    sql = f"SELECT * FROM users WHERE email = '{params['email']}'"
    
    find_user_data = db.executeOne(sql)
    
    if find_user_data :
        find_user = Users(find_user_data)
        return {
            'code' : 200,
            'message' : '사용자를 찾았다',
            'data' : {
                'user' : find_user.get_data_object()
            }
        }
    else :
        return {
            'code' : 400,
            'messsage' : '해당 이메일의 사용자 없음',            
        }, 400