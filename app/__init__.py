from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from werkzeug.middleware.proxy_fix import ProxyFix
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # 기본 설정
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@db:5432/flask_db'
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
    app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')  # 환경 변수에서 API 키 로드
    
    # 파일 업로드 설정 추가
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
    
    # 업로드 폴더가 없으면 생성
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # nginx나 다른 프록시 뒤에서 실행될 때 필요한 설정
    app.wsgi_app = ProxyFix(app.wsgi_app)
    
    # 확장 초기화
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    
    login_manager.login_view = 'auth.login'
    
    # 블루프린트 등록
    from app.routes.auth import auth  # auth 블루프린트 직접 import
    from app.routes.diary import bp as diary_bp  # diary 블루프린트를 diary_bp로 import
    
    app.register_blueprint(auth)  # auth 블루프린트 직접 등록
    app.register_blueprint(diary_bp)  # diary 블루프린트 등록
    
    return app
