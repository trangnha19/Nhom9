from django.contrib.auth.models import User
from django import forms
from .models import Profile, Letter


class LetterForm(forms.ModelForm):
  class Meta:
    model = Letter
    exclude = ('created_at', 'user', 'status')
    widgets = {'topic': forms.Select(attrs={'class': 'form-control'}),
               'content': forms.Textarea(attrs={'class': 'form-control'})}
    labels = {'topic': 'Chủ đề', 'content': 'Nội dung', 'is_anonymous': 'Gửi thư ẩn danh?'}


class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email']
		widgets = {'first_name': forms.TextInput(attrs={'class':'form-control'}),
				   'last_name': forms.TextInput(attrs={'class':'form-control'}),
				   'email': forms.TextInput(attrs={'class':'form-control'})}
		labels = {'first_name': 'Họ', 'last_name': 'Tên', 'email': 'Email'}


class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['dob', 'address', 'phone_number', 'image', 'cccd', 'major', 'degree']
		widgets = {'dob': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
				   'address': forms.TextInput(attrs={'class':'form-control'}),
				   'phone_number': forms.TextInput(attrs={'class':'form-control'}),
           'image': forms.FileInput(attrs={'type': 'file', 'class': 'form-control'}),
           'cccd': forms.TextInput(attrs={'class':'form-control'}),
           'major': forms.TextInput(attrs={'class':'form-control'}),
           'degree': forms.TextInput(attrs={'class':'form-control'})}
		labels = {'dob': 'Ngày sinh', 'address': 'Địa chỉ', 'phone_number': 'Số điện thoại',
            'image': 'Ảnh profile', 'cccd': 'Căn cước công dân', 'major': 'Chuyên ngành',
            'degree': 'Bằng cấp'}



class SignInForm(forms.ModelForm):
	class Meta:
		model=User
		fields = ['username', 'password']
		widgets = {'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên Đăng Nhập'}),
						'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mật Khẩu'})}
		labels = {'username': '', 'password': ''}

