from app import db
from datetime import datetime

class Diary(db.Model):
    __tablename__ = 'diaries'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # 이미지 정보를 저장하기 위한 관계 설정
    images = db.relationship('DiaryImage', backref='diary', lazy=True, cascade='all, delete-orphan')

    @property
    def representative_image(self):
        """대표 이미지를 반환. 없으면 가장 오래된 이미지 반환"""
        rep_image = DiaryImage.query.filter_by(
            diary_id=self.id, 
            is_representative=True
        ).first()
        if not rep_image and self.images:
            rep_image = self.images[0]  # 가장 오래된 이미지
        return rep_image

class DiaryImage(db.Model):
    __tablename__ = 'diary_images'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    diary_id = db.Column(db.Integer, db.ForeignKey('diaries.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_representative = db.Column(db.Boolean, nullable=False, default=False) 