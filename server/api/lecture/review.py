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
    
    db.executeQueryAndCommit(sql)
    
    return{
        'code' : 200,
        'message' : '리뷰 작성 완료'
    }
    
# 리뷰 수정하기
def modify_review(params):
    
    # 파라미터 정리
    # field : 어느 항목을 바꿀지 알려주는 역할
    # value : 해당 항목에 실제로 넣어줄 값
    # user_id : 변경을 시도하는 사람이 누구인지 고유번호
    # review_id : 변경해줄 리뷰의 id
    
    # field라는 이름표로 어느 항목을 바꾸고 싶은지 받아오자
    column_name = params['field']
    
    
    # 변경쿼리날리기전에 검증을 하자
    # 0 : 받아온 리뷰 아이디에 해당하는 리뷰가 실존하나?
    sql = f"SELECT * FROM lecture_review WHERE id = {params['review_id']}"
    
    review_data = db.executeOne(sql)
    
    if review_data == None:
        return {
            'code' : 400,
            'message' : '해당 리뷰 존재하지 않습니다.'
        }, 400
      
    # 1 : 수정하려는 리뷰가 본인이 작성한게 맞나?
    # 파라미터에서 가져온 user_id(파라미터에서 가져온 모든 데이터는 일단 str)
    if int(review_data['user_id']) != int(params['user_id']):
        return{
            'code' : 400,
            'message' : '본인 작성 리뷰만 수정 가능'
        }, 400
      
    
    # 제목 변경?
    if column_name == 'title':
        sql = f"UPDATE lecture_review SET title='{params['value']}' WHERE id = {params['review_id']} "
        
        # DB에 변경 발생
        db.cursor.execute(sql)
        db.db.commit()
        
        return{
            'code' : 200,
            'message' : '제목 수정 완료'
        }
     
    # 내용 변경?
    if column_name == 'content':
        sql = f"UPDATE lecture_review SET content = '{params['value']}' WHERE id={params['review_id']}"
        
        db.cursor.execute(sql)
        db.db.commit()
        
        return{
            'code' : 200,
            'message' : '내용 수정 완료'
        }
           
    # 점수 변경?
    if column_name == 'score':
        
        # 2 : 파라미터로 들어온 점수가 1~5인가?
        score = float(params['value'])
        
        if not (1<= score <= 5) :
            return{
                'code' : 400,
                'message' : '리뷰 범위는 1 ~ 5 만 입력하세요.'
            }, 400
       
        
        sql = f"UPDATE lecture_review SET score = {score} WHERE id = {params['review_id']}"
        
        db.cursor.execute(sql)
        db.db.commit()
        
        return{
            'code' : 200,
            'message' : '점수 수정 완료'
        }
   
    # 여기까지 내려온거면, 수정할 수 있는 field가 아님(잘못된 값 입력했다!)     
    return{
        'code' : 400,
        'message' : 'field에 잘못된 값 입력했다',
    }, 400