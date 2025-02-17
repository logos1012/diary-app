from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from cryptography.fernet import Fernet
import os
from base64 import b64encode, b64decode
from flask import current_app

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    gpt_api_key_encrypted = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.text('CURRENT_TIMESTAMP'))
    
    # 암호화 키 생성 또는 가져오기
    @staticmethod
    def get_encryption_key():
        key = os.environ.get('ENCRYPTION_KEY')
        if not key:
            # 새로운 키 생성
            key = Fernet.generate_key()
            os.environ['ENCRYPTION_KEY'] = key.decode()
            return key
        else:
            try:
                # 기존 키가 유효한지 확인
                key_bytes = key.encode() if isinstance(key, str) else key
                Fernet(key_bytes)
                return key_bytes
            except Exception:
                # 유효하지 않은 키면 새로 생성
                key = Fernet.generate_key()
                os.environ['ENCRYPTION_KEY'] = key.decode()
                return key

    @property
    def gpt_api_key(self):
        if not self.gpt_api_key_encrypted:
            return None
        try:
            f = Fernet(self.get_encryption_key())
            return f.decrypt(b64decode(self.gpt_api_key_encrypted)).decode()
        except Exception as e:
            current_app.logger.error(f"GPT API 키 복호화 오류: {str(e)}")
            return None

    @gpt_api_key.setter
    def gpt_api_key(self, api_key):
        if api_key:
            try:
                f = Fernet(self.get_encryption_key())
                self.gpt_api_key_encrypted = b64encode(f.encrypt(api_key.encode())).decode()
            except Exception as e:
                current_app.logger.error(f"GPT API 키 암호화 오류: {str(e)}")
                self.gpt_api_key_encrypted = None
        else:
            self.gpt_api_key_encrypted = None

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id)) 