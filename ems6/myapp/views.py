from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .models import *
from django.contrib.auth.models import User, auth
from datetime import datetime, timedelta
from django.db.models import Sum, Min, Max
from django.contrib import messages

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        title = 'Home'
        for user in User.objects.all():
            user.save()
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
                messages.warning(request, 'Vào tài khoản của bản thân để xem')
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
                messages.success(request, 'Cảm ơn bạn đã đi làm ngày hôm nay!!!')
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

            # Lấy danh sách bảng chấm công của user
            sheets = Sheet.objects.filter(user=user).order_by('-date')

            # Tính tổng giờ làm việc
            total_hour = sheets.aggregate(total_hour=Sum('work_hour'))['total_hour'] or 0

            # Lấy thông tin lương từ Profile (vì salary nằm trong Profile)
            try:
                profile = Profile.objects.get(user=user)
                total_salary = total_hour * profile.salary
            except Profile.DoesNotExist:
                total_salary = 0  # Nếu không có Profile, gán lương bằng 0

            # Đếm số lần đến muộn
            count_late = sheets.filter(status='Đến Muộn').count()

            context = {
                'title': title,
                'sheets': sheets,
                'total_hour': total_hour,
                'total_salary': total_salary,
                'count_late': count_late,
            }
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
        context = {'title': title, 'form': form, 'my_letters': my_letters}
        return render(request, 'pages/letters.html', context)
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

def request_day_off(request, username):
    try:
        title = 'Danh sách nghỉ phép'
        user = User.objects.get(username=username)
        day_off_requests = DayOffRequest.objects.filter(user=user).order_by('-start_date')
        max_end_date = day_off_requests.aggregate(max_end_date=Max('end_date'))['max_end_date']
        if max_end_date is None:
            # Nếu không có dữ liệu, đặt giá trị mặc định
            max_end_date = timezone.now().date()  # Hoặc một giá trị phù hợp
        else:
            max_end_date += timedelta(days=1)
        form = DayOffRequestForm(request.POST or None, request.FILES or None)
        if request.POST:
            if form.is_valid():
                day_off = form.save(False)
                day_off.user = request.user
                day_off.save()
                messages.success(request, 'Gửi yêu cầu nghỉ thành công')
            return redirect('request-day-off', username=username)
        context = {'title': title,'day_off_requests': day_off_requests, 'form': form, 'max_end_date': max_end_date}
        return render(request, 'pages/request_day_off.html', context)
    except User.DoesNotExist:
        return redirect('home')