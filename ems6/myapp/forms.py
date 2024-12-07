from django.contrib.auth.models import User
from django import forms
from .models import *


class LetterForm(forms.ModelForm):
  class Meta:
    model = Letter
    exclude = ('created_at', 'user', 'status')
    widgets = {'topic': forms.Select(attrs={'class': 'form-control'}),
               'content': forms.Textarea(attrs={'class': 'form-control'})}
    labels = {'topic': 'Chủ đề', 'content': 'Nội dung', 'is_anonymous': 'Gửi thư ẩn danh?'}


class SignInForm(forms.ModelForm):
	class Meta:
		model=User
		fields = ['username', 'password']
		widgets = {'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên Đăng Nhập'}),
						'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mật Khẩu'})}
		labels = {'username': '', 'password': ''}


class DayOffRequestForm(forms.ModelForm):
    class Meta:
        model = DayOffRequest
        fields = ['start_date', 'end_date', 'reason', 'image']
        labels = {'start_date': 'Ngày bắt đầu nghỉ', 'end_date': 'Ngày kết thúc nghỉ', 'reason': 'Lý do', 'image': 'Ảnh minh chứng'}
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'image': forms.FileInput(attrs={'type': 'file', 'class': 'form-control'})}

