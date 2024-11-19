from django.shortcuts import render, get_object_or_404, redirect
from .forms import SignInForm, UserForm, ProfileForm, LetterForm
from .models import *
from django.contrib.auth.models import User, auth
from datetime import datetime
from django.db.models import Sum
from django.contrib import messages

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        title = 'Home'
        context = {'title': title}
        return render(request, 'pages/home.html', context)
    else:
        return redirect('login')

def login(request):
    title = 'Đăng nhập'
    form_li = SignInForm()
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user: 
            auth.login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Tài khoản hoặc mật khẩu không đúng')
            return redirect('login')
    context = {'title': title,
               'form_li':form_li}
    return render(request, 'pages/login.html', context)

def logout(request):
    auth.logout(request)
    return redirect('/')

def profile_detail(request, username):
    if request.user.is_authenticated:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user:
            if request.user.is_superuser or request.user.username == username:
                title = f'Hồ sơ {username}'
                departments = Department.objects.all()
                positions = Position.objects.filter(department=user.profile.position.department)
                if request.POST:
                    pos = request.POST.get('position')
                    dep = request.POST.get('department')
                    if pos and dep:
                        try: 
                            position = Position.objects.get(name=pos, department__name=dep)
                        except Position.DoesNotExist:
                            position = None
                        if not position:
                            messages.error(request, 'Không tìm thấy vị trí tại phòng đã chọn')
                            return redirect('profile-detail', username)
                    if pos and not dep:
                        position = Position.objects.get(name=pos, department=user.profile.position.department)
                    if dep and not pos:
                        position = Position.objects.get(name=user.profile.position.name, department__name=dep)
                    user.profile.position = position
                    user.profile.save()
                    messages.info(request, 'Cập nhật thành công')
                context = {'title':title,
                        'user':user,
                        'positions': positions,
                        'departments': departments}
                return render(request, 'pages/profile_detail.html', context)
            else:
                messages.warning(request, 'Vào của mày mà xem')
                return redirect('profile-detail', username=request.user.username)
        else:
            messages.error(request, 'Không tìm thấy người dùng này')
            return redirect('home')
    else:
        return redirect('home')

def update_info(request, username):
    if request.user.is_authenticated:
        if request.user.username==username:
            title = f'Sửa hồ sơ {username}'
            form_user = UserForm(instance=request.user)
            form_pr = ProfileForm(instance=request.user.profile)
            if request.POST:
                form_user = UserForm(request.POST, instance=request.user)
                form_pr = ProfileForm(request.POST, instance=request.user.profile)
                if form_user.is_valid() and form_pr.is_valid():
                    form_user.save()
                    form_pr.save()
                    return redirect('profile-detail', username = request.user.username)
            context = {'title': title,
                    'form_user':form_user,
                    'form_pr':form_pr}
            return render(request, 'pages/update_info.html', context)
        else:
            messages.warning(request, 'Mày đừng có mà táy máy')
            return redirect('profile-detail', username = request.user.username)
    else: 
        return redirect('home')

def time_keeping(request):
    if request.user.is_authenticated:
        title = 'Check In'
        date = datetime.now().date()
        if request.POST:
            check = request.POST.get('check', '')
            if check == 'in':
                Sheet.objects.create(user=request.user,date=datetime.now().date(),checkin=datetime.now().time())
                messages.success(request, 'Check-in thành công, làm việc nào!!!')
            if check == 'out':
                sheet = Sheet.objects.filter(user=request.user, date=datetime.now().date()).order_by('-id').first()
                sheet.checkout = datetime.now().time()
                sheet.save()
                messages.success(request, 'Cảm ơn bạn đã đi làm ngày hôm này!!!')
            return redirect('home')
        context = {'title': title, 'date': date}
        return render(request, 'pages/time_keeping.html', context)
    else:
        messages.error(request, 'Vui lòng đăng nhập')
        return redirect('login')
    
def sheet(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    if user and request.user.is_authenticated:
        if request.user.username == username:
            title = f'Bảng chấm công {username}'
            sheets = Sheet.objects.filter(user=user).order_by('-date')
            sheets.total_hour = sheets.aggregate(total_hour=Sum('work_hour'))['total_hour']
            sheets.total_salary = sheets.aggregate(total_salary=Sum('salary'))['total_salary']
            sheets.count_late = sheets.filter(status='Muộn').count()
            context = {'title': title,
                       'sheets': sheets}
            return render(request, 'pages/sheet.html', context)
        else:
            messages.warning(request, 'Hãy vào tài khoản của mình để xem')
            return redirect('sheet', username=request.user.username)
    else:
        messages.error(request, 'Vui lòng đăng nhập')
        return redirect('home')
    
def letters(request):
    if request.user.is_authenticated:
        title = 'Hòm thư ý kiến'
        my_letters = Letter.objects.filter(user=request.user)
        form = LetterForm(request.POST or None)
        if request.POST:
            if form.is_valid():
                letter = form.save(commit=False)
                letter.user = request.user
                letter.save()
                messages.success(request, 'Đã gửi đóng góp')
                return redirect('home')
        return render(request, 'pages/letters.html', {'title': title, 'form': form, 'my_letters': my_letters})
    else:
        return redirect('login')

def letter_detail(request, idletter):
    try:
        letter = Letter.objects.get(id=idletter)
        if request.user == letter.user or request.user.is_superuser:
            title = 'Chi tiết góp ý'
            if request.POST:
                letter.status = 'Đã xử lý'
                letter.save()
                messages.success(request, 'Đã xử lý thư góp ý')
                return redirect('main-letter')
            return render(request, 'pages/letter_detail.html', {'title': title, 'letter': letter})
        else:
            return redirect('letters')
    except Letter.DoesNotExist:
        return redirect('letters')