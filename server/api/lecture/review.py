from server import db

# 강의의 리뷰에 대한 기능만 모아두는 파일

def write_review(params):  

    # 1. 평점은 1 ~ 5 사이만 가능(파라미터)
    score = float(params['score'])   # 파라미터들은 기본적으로 str형으로 들어오기 때문에 float로 형변환   
    if not (1 <= score <= 5):
        return{
            'code' : 400,
            'message' : '평점은 1 ~ 5 사이여야 함'
        }, 400
    
    # 2. 제목의 길이는 최소 5자 이상(파라미터)    
    if len(params['title']) < 5:
        return{
            'code' : 400,
            'meesage' : '제목 5자 이상 작성해라',
        }, 400
    
    # 3. 내용의 길이는 최소 10자 이상(파라미터)   
    if len(params['content']) < 10:
        return{
        'code' : 400,
        'meesage' : '내용 10자 이상 작성해라',
    }, 400
        
    # 4. 수강신청을 해야지 리뷰 작성 가능(DB내부 조회)
    sql = f"SELECT * FROM lecture_user WHERE lecture_id = {params['lecture_id']} AND user_id = {params['user_id']}"
    
    query_result = db.executeOne(sql)
    
    if not query_result :
        return {
            'code' : 400,
            'message' : '수강신청을 안했으니 리뷰 작성 못해요.'
        }, 400
    
    # 5. 이미 리뷰를 등록했다면, 추가 등록 못하게 막자
    sql = f"SELECT * FROM lecture_review WHERE lecture_id = {params['lecture_id']} AND user_id = {params['user_id']}"
    
    already_review_data = db.executeOne(sql)
    
    if already_review_data:
        return{
            'code' : 400,
            'message' : '이미 작성했습니다.'
        }, 400
    
    # 리뷰 실제 등록
    sql = f"INSERT INTO lecture_review (lecture_id, user_id, title, content, score) VALUES ({params['lecture_id']}, {params['user_id']}, '{params['title']}', '{params['content']}',{params['score']})"
    
    db.insertAndCommit(sql)
    
    return{
        'code' : 200,
        'message' : '리뷰 작성 완료'
    }