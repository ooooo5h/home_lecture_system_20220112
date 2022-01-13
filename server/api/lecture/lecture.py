from server.model import Lectures
from server import db

# 모든 강의 목록 <이름순으로> 내려오기(당장은 params 활용 x)
def get_all_lectures(params):
    
    sql = f"SELECT * FROM lectures ORDER BY name"
    
    lecture_list = db.executeAll(sql)
    
    lectures = [Lectures(row).get_data_object() for row in lecture_list]
    
    return{
        'code' : 200,
        'message' : '모든 강의 내려오기',
        'data' : {
            'lectures' : lectures,
        }
    }


# 수강 신청 기능
def apply_lecture(params):
    
    # 같은 과목에 같은 사람 신청 불가
    sql = f"SELECT * FROM lecture_user WHERE lecture_id = {params['lecture_id']} AND user_id = {params['user_id']}"
    
    already_apply = db.executeOne(sql)
    
    if already_apply:
        return {
            'code' : 400,
            'message' : '이미 수강신청 했음',
        }, 400
    
    
    # lecture_user 테이블에 한 줄 추가
    sql = f"INSERT INTO lecture_user VALUES ({params['lecture_id']},{params['user_id']})"
    
    db.insertAndCommit(sql)
    
    return {
        'code' : 200,
        'message' : '수강 신청 완료'
    }

# 수강 취소 
def cancel_apply(params):
    return{
        '임시' : '수강 취소 테스트'
    }