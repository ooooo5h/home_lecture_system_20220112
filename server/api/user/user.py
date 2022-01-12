# 로그인/회원가입 등, 사용자 정보 관련 기능 모아두는 모듈
# DB 연결 정보를 보관하는 변수를 import 하자
from server.db_connector import DBConnector
from server.model.users import Users

db = DBConnector()

def test():
    
    # DB의 모든 users 조회 쿼리를 날려보자
    sql = "SELECT * FROM users"
    db.cursor.execute(sql)
    all_list = db.cursor.fetchall()
    
    all_users = []
    
    for row in all_list :
        # Users(row) : Users형태의 인스턴스 생성 => 함수들도 내장하고 있다
        # 인스턴스에게 곧바로 get_data_object() 실행 명령
        # 해당 유저의 정보를 활용한 dict가 리턴됨
        # 곧바로 목록의 append의 재료로 활용
        all_users.append(Users(row).get_data_object())
    
    return{
        'users' : all_users
    }