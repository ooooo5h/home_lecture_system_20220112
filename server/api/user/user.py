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
    
    # 목록 for문을 돌면서, 한 줄을 row로 추출하고, 추출된 row를 모델클래스로 가공해서 dict로 재가공해라를 한줄로 작성
    # comprehension
    all_users = [ Users(row).get_data_object()  for row in all_list]
        
    return{
        'users' : all_users
    }