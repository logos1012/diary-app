import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required, current_user
from app.models.diary import Diary, DiaryImage
from app.forms import DiaryForm
from app import db
from werkzeug.utils import secure_filename
from datetime import datetime, date
from calendar import monthrange
import uuid
from markdown2 import Markdown
from pillow_heif import register_heif_opener
from PIL import Image
import io
from dateutil.relativedelta import relativedelta

bp = Blueprint('diary', __name__)

markdowner = Markdown()

# HEIF/HEIC 지원 등록
register_heif_opener()

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'heic', 'heif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file):
    if file and allowed_file(file.filename):
        # 안전한 파일명 생성
        original_filename = secure_filename(file.filename)
        extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.jpg"  # HEIC는 JPG로 변환
        
        # 업로드 폴더가 없으면 생성
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        # 파일 저장 경로
        file_path = os.path.join(upload_folder, unique_filename)
        
        # HEIC/HEIF 파일 처리
        if extension in ['heic', 'heif']:
            # 파일을 메모리에서 열기
            image_data = file.read()
            image = Image.open(io.BytesIO(image_data))
            # JPG로 변환하여 저장
            image.save(file_path, 'JPEG', quality=95)
        else:
            # 다른 이미지 형식은 그대로 저장
            file.save(file_path)
        
        return unique_filename
    return None

@bp.route('/')
@login_required
def index():
    year = request.args.get('year', datetime.now().year, type=int)
    month = request.args.get('month', datetime.now().month, type=int)
    
    # 현재 연도 기준으로 ±10년 범위 설정
    current_year = datetime.now().year
    year_range = range(current_year - 10, current_year + 11)
    
    # 오늘 날짜 정보
    today = datetime.now().date()
    
    # 해당 월의 모든 일기를 가져옴
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
    
    diaries = Diary.query.filter(
        Diary.user_id == current_user.id,
        Diary.created_at >= start_date,
        Diary.created_at < end_date
    ).order_by(Diary.created_at.desc()).all()
    
    # 날짜별 일기 딕셔너리 생성 (JSON 직렬화 가능한 형태로)
    diary_dict = {}
    for diary in diaries:
        day = str(diary.created_at.day)
        if day not in diary_dict:
            diary_dict[day] = []
        diary_dict[day].append({
            'id': diary.id,
            'title': diary.title,
            'created_at': diary.created_at.strftime('%Y-%m-%d')
        })
    
    # 달력 표시를 위한 변수 계산
    first_day = date(year, month, 1)
    # weekday()는 월요일이 0, 일요일이 6이므로 조정이 필요
    first_day_weekday = (first_day.weekday() + 1) % 7  # 일요일이 0, 토요일이 6이 되도록 조정
    _, days_in_month = monthrange(year, month)
    
    # 이전 달과 다음 달 계산
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year
        
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year
    
    return render_template('diary/calendar.html',
                         year=year,
                         month=month,
                         year_range=year_range,
                         diary_dict=diary_dict,
                         first_day_weekday=first_day_weekday,
                         days_in_month=days_in_month,
                         prev_year=prev_year,
                         prev_month=prev_month,
                         next_year=next_year,
                         next_month=next_month,
                         today=today)

@bp.route('/diary/create', methods=['GET', 'POST'])
@login_required
def create():
    form = DiaryForm()
    
    if form.validate_on_submit():
        try:
            diary = Diary(
                title=form.title.data,
                content=form.content.data,
                created_at=datetime.combine(form.date.data, datetime.min.time()),
                updated_at=datetime.now(),
                user_id=current_user.id
            )
            
            db.session.add(diary)
            db.session.flush()  # diary.id를 얻기 위해 flush
            
            # 이미지 처리
            if form.images.data:
                for file in form.images.data:
                    if file and allowed_file(file.filename):
                        try:
                            filename = save_image(file)
                            if filename:
                                image = DiaryImage(
                                    filename=filename,
                                    diary_id=diary.id,
                                    is_representative=not diary.images  # 첫 번째 이미지를 대표 이미지로
                                )
                                db.session.add(image)
                        except Exception as e:
                            current_app.logger.error(f'이미지 저장 오류: {str(e)}')
                            continue
            
            db.session.commit()
            flash('일기가 저장되었습니다.')
            return redirect(url_for('diary.view', id=diary.id))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'일기 저장 오류: {str(e)}')
            flash('일기 저장 중 오류가 발생했습니다.')
            
    return render_template('diary/editor.html', form=form)

@bp.route('/diary/<int:id>', methods=['GET'])
@login_required
def view(id):
    diary = Diary.query.get_or_404(id)
    if diary.user_id != current_user.id:
        flash('접근 권한이 없습니다.')
        return redirect(url_for('diary.index'))
    
    # 마크다운을 HTML로 변환
    diary.content_html = markdowner.convert(diary.content)
    return render_template('diary/view.html', diary=diary)

@bp.route('/diary/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    diary = Diary.query.get_or_404(id)
    if diary.user_id != current_user.id:
        flash('접근 권한이 없습니다.')
        return redirect(url_for('diary.index'))
    
    form = DiaryForm(obj=diary)
    if form.validate_on_submit():
        try:
            diary.title = form.title.data
            diary.content = form.content.data
            
            # 이미지 처리
            if form.images.data:
                for file in form.images.data:
                    if file:
                        filename = save_image(file)
                        if filename:
                            image = DiaryImage(
                                filename=filename,
                                diary_id=diary.id
                            )
                            db.session.add(image)
            
            db.session.commit()
            flash('일기가 수정되었습니다.')
            return redirect(url_for('diary.view', id=diary.id))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'일기 수정 오류: {str(e)}')
            flash('일기 수정 중 오류가 발생했습니다.')
    
    return render_template('diary/editor.html', form=form, diary=diary)

@bp.route('/diary/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    diary = Diary.query.get_or_404(id)
    
    if diary.user_id != current_user.id:
        flash('삭제 권한이 없습니다.')
        return redirect(url_for('diary.list_all'))
    
    try:
        # 연결된 이미지 파일들 삭제
        for image in diary.images:
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image.filename)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        db.session.delete(diary)
        db.session.commit()
        
        flash('일기가 삭제되었습니다.')
        return redirect(url_for('diary.list_all'))
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'일기 삭제 오류: {str(e)}')
        flash('일기 삭제 중 오류가 발생했습니다.')
        return redirect(url_for('diary.list_all'))

@bp.route('/diary/upload-image', methods=['POST'])
@login_required
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': '파일이 없습니다.'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '선택된 파일이 없습니다.'}), 400
    
    if file and allowed_file(file.filename):
        filename = save_image(file)
        if filename:
            return jsonify({
                'url': url_for('static', filename=f'uploads/{filename}'),
                'filename': filename
            })
        return jsonify({'error': '파일 저장에 실패했습니다.'}), 400
    
    return jsonify({'error': '허용되지 않는 파일 형식입니다.'}), 400

@bp.route('/diary/image/<int:image_id>', methods=['DELETE'])
@login_required
def delete_image(image_id):
    image = DiaryImage.query.get_or_404(image_id)
    diary = Diary.query.get(image.diary_id)
    
    if diary.user_id != current_user.id:
        return jsonify({'error': '권한이 없습니다.'}), 403
    
    try:
        # 파일 시스템에서 이미지 삭제
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image.filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        db.session.delete(image)
        db.session.commit()
        return jsonify({'message': '이미지가 삭제되었습니다.'}), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'이미지 삭제 오류: {str(e)}')
        return jsonify({'error': '이미지 삭제 중 오류가 발생했습니다.'}), 500

@bp.route('/diary/new', methods=['GET', 'POST'])
@bp.route('/diary/edit/<int:diary_id>', methods=['GET', 'POST'])
def edit_diary(diary_id=None):
    form = DiaryForm()
    if form.validate_on_submit():
        # 일기 저장 로직 추가
        diary = Diary(title=form.title.data, content=form.content.data, date=form.date.data)
        # 이미지 처리 로직 추가 (필요한 경우)
        
        # 데이터베이스에 저장
        db.session.add(diary)
        db.session.commit()
        
        flash('일기가 저장되었습니다.', 'success')
        return redirect(url_for('diary.index'))
    
    # 기존 일기 로드 (편집 모드일 경우)
    if diary_id:
        diary = Diary.query.get(diary_id)
        form.title.data = diary.title
        form.content.data = diary.content
        form.date.data = diary.date

    return render_template('diary/editor.html', form=form)

@bp.route('/diary/list')
@login_required
def list_all():
    # 모든 일기를 날짜 내림차순으로 가져옴
    diaries = Diary.query.filter_by(user_id=current_user.id)\
        .order_by(Diary.created_at.desc())\
        .all()
    
    return render_template('diary/list.html', diaries=diaries)

@bp.route('/diary/photo')
@login_required
def photo_calendar():
    year = request.args.get('year', datetime.now().year, type=int)
    month = request.args.get('month', datetime.now().month, type=int)
    
    # 현재 연도 기준으로 ±10년 범위 설정
    current_year = datetime.now().year
    year_range = range(current_year - 10, current_year + 11)
    
    # 오늘 날짜 정보
    today = datetime.now().date()
    
    # 해당 월의 모든 일기를 가져옴
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
    
    # 이미지가 있는 일기만 가져오기
    diaries = Diary.query.join(DiaryImage).filter(
        Diary.user_id == current_user.id,
        Diary.created_at >= start_date,
        Diary.created_at < end_date
    ).order_by(Diary.created_at.desc()).all()
    
    # 날짜별 이미지 딕셔너리 생성
    photo_dict = {}
    for diary in diaries:
        if diary.images:
            day = str(diary.created_at.day)
            if day not in photo_dict:
                photo_dict[day] = []
            # 대표 사진 또는 첫 번째 사진만 추가
            rep_image = diary.representative_image
            if rep_image:
                photo_dict[day].append({
                    'diary_id': diary.id,
                    'image_filename': rep_image.filename
                })
    
    # 달력 표시를 위한 변수 계산
    first_day = date(year, month, 1)
    first_day_weekday = (first_day.weekday() + 1) % 7
    _, days_in_month = monthrange(year, month)
    
    # 이전 달과 다음 달 계산
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year
        
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year
    
    return render_template('diary/photo_calendar.html',
                         year=year,
                         month=month,
                         year_range=year_range,
                         photo_dict=photo_dict,
                         first_day_weekday=first_day_weekday,
                         days_in_month=days_in_month,
                         prev_year=prev_year,
                         prev_month=prev_month,
                         next_year=next_year,
                         next_month=next_month,
                         today=today)

@bp.route('/diary/image/<int:image_id>/set-representative', methods=['POST'])
@login_required
def set_representative_image(image_id):
    image = DiaryImage.query.get_or_404(image_id)
    diary = Diary.query.get(image.diary_id)
    
    if diary.user_id != current_user.id:
        return jsonify({'error': '권한이 없습니다.'}), 403
    
    try:
        # 해당 일기의 모든 이미지의 대표 상태를 해제
        DiaryImage.query.filter_by(diary_id=diary.id).update(
            {'is_representative': False},
            synchronize_session=False
        )
        # 선택한 이미지를 대표로 설정
        image.is_representative = True
        db.session.commit()
        return jsonify({'message': '대표 사진이 설정되었습니다.'}), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'대표 사진 설정 오류: {str(e)}')
        return jsonify({'error': '대표 사진 설정 중 오류가 발생했습니다.'}), 500

@bp.route('/home')
@login_required
def home():
    current_date = datetime.now()
    monthly_images = []
    
    for i in range(12):
        # 각 월의 시작일과 종료일 계산
        target_date = current_date.replace(day=1) - relativedelta(months=i)
        start_date = target_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # 다음 달의 첫 날을 계산하여 종료일로 사용
        end_date = (start_date + relativedelta(months=1))
        
        # 해당 월의 대표 이미지들 조회
        monthly_diaries = Diary.query.join(DiaryImage).filter(
            Diary.user_id == current_user.id,
            Diary.created_at >= start_date,
            Diary.created_at < end_date,
            DiaryImage.is_representative == True
        ).order_by(Diary.created_at.desc()).all()
        
        if monthly_diaries:
            monthly_images.append({
                'year': target_date.year,
                'month': target_date.month,
                'diaries': [{
                    'id': diary.id,
                    'title': diary.title,
                    'created_at': diary.created_at,
                    'image': diary.representative_image
                } for diary in monthly_diaries if diary.representative_image]
            })
    
    return render_template('diary/home.html', monthly_images=monthly_images)

@bp.route('/save', methods=['POST'])
@login_required
def save():
    form = DiaryForm()
    
    # 폼 데이터 로깅
    current_app.logger.debug(f'폼 데이터: {request.form.to_dict()}')
    current_app.logger.debug(f'CSRF 토큰 존재: {"csrf_token" in request.form}')
    
    if not form.validate():
        current_app.logger.error(f'폼 검증 오류: {form.errors}')
        for field, errors in form.errors.items():
            error_msg = f'{field}: {", ".join(errors)}'
            current_app.logger.error(error_msg)
            flash(error_msg)
        return redirect(url_for('diary.editor'))
    
    try:
        diary = Diary(
            user_id=current_user.id,
            title=form.title.data,
            content=form.content.data
        )
        db.session.add(diary)
        db.session.commit()
        
        # 이미지 처리
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                
                image = DiaryImage(
                    diary_id=diary.id,
                    filename=filename
                )
                db.session.add(image)
                db.session.commit()

        flash('일기가 저장되었습니다.')
        return redirect(url_for('diary.view', diary_id=diary.id))
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'일기 저장 오류: {str(e)}')
        flash('일기 저장 중 오류가 발생했습니다.')
        return redirect(url_for('diary.editor'))