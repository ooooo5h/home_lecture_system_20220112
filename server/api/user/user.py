# 로그인/회원가입 등, 사용자 정보 관련 기능 모아두는 모듈
# DB 연결 정보를 보관하는 변수를 import 하자
from server.db_connector import DBConnector

db = DBConnector()

def test():
    
    # DB의 모든 users 조회 쿼리를 날려보자
    sql = "SELECT * FROM users"
    db.cursor.execute(sql)
    all_list = db.cursor.fetchall()
    
    print(all_list)
    
    return{
        '임시' : '임시'
    }