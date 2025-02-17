from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app.forms import LoginForm, RegistrationForm
from app import db
from urllib.parse import urlparse
import traceback

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('diary.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('diary.index')
            return redirect(next_page)
        flash('아이디 또는 비밀번호가 올바르지 않습니다.')
    
    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('diary.index'))
    
    form = RegistrationForm()
    
    if request.method == 'POST':
        # POST 데이터 로깅
        current_app.logger.debug(f'폼 데이터: {request.form.to_dict()}')
        
        # CSRF 토큰 확인
        current_app.logger.debug(f'CSRF 토큰 존재: {"csrf_token" in request.form}')
        
        # 폼 검증
        is_valid = form.validate()
        current_app.logger.debug(f'폼 검증 결과: {is_valid}')
        
        if not is_valid:
            current_app.logger.error(f'폼 검증 오류: {form.errors}')
            for field, errors in form.errors.items():
                error_msg = f'{field}: {", ".join(errors)}'
                current_app.logger.error(error_msg)
                flash(error_msg)
            return render_template('auth/register.html', form=form)
    
    if form.validate_on_submit():
        try:
            current_app.logger.info('폼 검증 성공')
            
            # 사용자 객체 생성 시도
            user = User(username=form.username.data)
            user.set_password(form.password.data)
            user.gpt_api_key = form.gpt_api_key.data
            
            # 생성된 객체 정보 로깅
            user_dict = {
                'username': user.username,
                'password_hash': bool(user.password_hash),
                'gpt_api_key_encrypted': bool(user.gpt_api_key_encrypted)
            }
            current_app.logger.debug(f'생성된 user 객체: {user_dict}')
            
            # DB 저장 시도
            db.session.add(user)
            current_app.logger.debug('DB 세션에 사용자 추가됨')
            
            db.session.commit()
            current_app.logger.info('회원가입 성공')
            
            flash('회원가입이 완료되었습니다. 로그인해주세요.')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'회원가입 오류 발생: {str(e)}')
            current_app.logger.error(f'상세 오류:\n{traceback.format_exc()}')
            flash('회원가입 중 오류가 발생했습니다.')
    
    return render_template('auth/register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login')) 