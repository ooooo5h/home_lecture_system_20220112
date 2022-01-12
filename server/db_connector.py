import pymysql
from pymysql.cursors import DictCursor

class DBConnector :
    def __init__(self):
        self.db = pymysql.connect(
            host='finalproject.cbqjwimiu76h.ap-northeast-2.rds.amazonaws.com',
            port=3306,
            user='admin',
            passwd='Vmfhwprxm!123',
            db='test_202112_python',
            charset='utf8',
            cursorclass=DictCursor
        )

        # 커서도 변수로 담아두기
        self.cursor = self.db.cursor()
        
    # 쿼리 실행의 목록을 리턴하는 메쏘드 추가
    def executeAll(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def executeOne(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchone()
       
    # 하나의 데이터를 추가하고 DB에 실제 기록
    def insertAndCommit(self, sql):
        self.cursor.execute(sql)
        self.db.commit()