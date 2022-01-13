from server.model import Lectures, Reviews
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
    
    # 1. 수강신청 안 한 과목은 취소 불가 400
    sql = f"SELECT * FROM lecture_user WHERE user_id = {params['user_id']} AND lecture_id = {params['lecture_id']} "
    
    already_apply = db.executeOne(sql)
    
    if not already_apply :
        return {
            'code' : 400,
            'message' : '수강 신청 안한 과목은 취소 불가',
        }, 400
    
    
    # 향후에는 토큰을 받아내서, 내가 신청한 과목만 취소 가능하도록 처리
    
    # 2. 실제 신청 내역 삭제(쿼리 매우 유의!!)
    sql = f"DELETE FROM lecture_user WHERE user_id = {params['user_id']} AND lecture_id = {params['lecture_id']}"
    
    # DELETE문도 쿼리 실행/DB변경 확정 절차로, INSERT INTO와 동일하게 동작한다
    db.cursor.execute(sql)
    db.db.commit()
    
    return{
        'code' : 200,
        'message' : '수강 취소 완료'
    }
    
# 특정 강의 상세보기
def view_lecture_detail(id, params):
    
    # 1 : 강의 자체에 대한 정보 조회
    
    sql = f"SELECT * FROM lectures WHERE id = {id}"
    
    lecture_data = db.executeOne(sql)
    
    lecture = Lectures(lecture_data)
    
    # 2 : 모든 리뷰 내역을 추가로 첨부   
    sql = f"SELECT * FROM lecture_review WHERE lecture_id = {id}"
    
    review_data_list = db.executeAll(sql)
    
    reviews = [Reviews(row).get_data_object() for row in review_data_list]
    
    
    # 3 : 해당 강의의 모든 리뷰 평균 점수를 추가로 조회

    
    
    return{
        'code' : 200,
        'message' : '강의 상세 보기',
        'data' : {
            'lecture' : lecture.get_data_object(),
            'reviews' : reviews,
        }
    }