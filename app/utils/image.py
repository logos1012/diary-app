import os
from PIL import Image
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
THUMBNAIL_SIZE = (300, 300)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_thumbnail(image_path, thumbnail_path):
    with Image.open(image_path) as img:
        img.thumbnail(THUMBNAIL_SIZE)
        img.save(thumbnail_path)

def save_image(file):
    if file and allowed_file(file.filename):
        try:
            # 안전한 파일명 생성
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = f"{timestamp}{filename}"
            
            # 파일 저장 경로
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            
            # 업로드 폴더가 없으면 생성
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # 파일 저장
            file.save(file_path)
            
            return filename
        except Exception as e:
            current_app.logger.error(f'이미지 저장 중 오류 발생: {str(e)}')
            return None
    return None 