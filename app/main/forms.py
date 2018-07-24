from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import request
from app.models import Tool


class SearchForm(FlaskForm):
    q = StringField('搜索工具', validators=[DataRequired()], render_kw={'placeholder': '比如说"磁力"——老司机的最爱XD'})


class UploadForm(FlaskForm):
    name = StringField('名称', validators=[DataRequired()])
    url = StringField('链接', validators=[DataRequired()])
    submit = SubmitField('提交')

    def validate(self):
        initial_validation = super(UploadForm, self).validate()
        if not initial_validation:
            return False
        
        self.tool = Tool.query.filter_by(url=self.url.data).first()

        if self.tool:
            self.url.errors.append('不要上传重复的工具！')
            return False
        return True
