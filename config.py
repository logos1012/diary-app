import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://jake:dnjfcjsaksdnjs@localhost/diary_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # SQL 쿼리 로깅 활성화
    
    # 현재 파일의 디렉토리를 기준으로 uploads 폴더 경로 설정
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
