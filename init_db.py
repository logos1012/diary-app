from app import create_app, db

app = create_app()

with app.app_context():
    # 기존 테이블 삭제
    db.drop_all()
    # 새로운 테이블 생성
    db.create_all()
    print("데이터베이스 테이블이 성공적으로 생성되었습니다.") 