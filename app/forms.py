from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, MultipleFileField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.models.user import User
from flask_wtf.file import FileAllowed
from datetime import datetime

class LoginForm(FlaskForm):
    username = StringField('사용자명', 
                         validators=[DataRequired()],
                         render_kw={"autocomplete": "username"})
    password = PasswordField('비밀번호',
                           validators=[DataRequired()],
                           render_kw={"autocomplete": "current-password"})
    submit = SubmitField('로그인')

class RegistrationForm(FlaskForm):
    username = StringField('사용자명', 
                         validators=[DataRequired(), Length(min=2, max=20)],
                         render_kw={"autocomplete": "username"})
    
    password = PasswordField('비밀번호',
                           validators=[DataRequired(), Length(min=6)],
                           render_kw={"autocomplete": "new-password"})
    
    confirm_password = PasswordField('비밀번호 확인',
                                   validators=[DataRequired(), EqualTo('password')],
                                   render_kw={"autocomplete": "new-password"})
    
    gpt_api_key = StringField('GPT API Key',
                             validators=[DataRequired()],
                             render_kw={"autocomplete": "off"})
    
    submit = SubmitField('가입하기')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('이미 사용 중인 사용자명입니다.')

class DiaryForm(FlaskForm):
    title = StringField('제목', validators=[DataRequired()])
    content = TextAreaField('내용', validators=[DataRequired()])
    date = DateField('날짜', validators=[DataRequired()], format='%Y-%m-%d')
    images = MultipleFileField('이미지')
    submit = SubmitField('저장하기')

    def __init__(self, *args, **kwargs):
        super(DiaryForm, self).__init__(*args, **kwargs)
        if not self.date.data:
            self.date.data = datetime.now().date() 