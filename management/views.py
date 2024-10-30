from django.shortcuts import render, redirect
from django.db.models import Sum, Q
from django.contrib import messages
from datetime import datetime
from myapp.models import Sheet, User, Profile, Position, Department
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

# Create your views here.
def home(request):
  if request.user.is_superuser:
    title = 'Dashboard'
    count_emp = User.objects.count()
    count_emp_male = User.objects.filter(profile__gender='Nam').count()
    count_emp_female = User.objects.filter(profile__gender='Nữ').count()
    today = timezone.now().date()
    count_late = Sheet.objects.filter(date=today, status='Muộn').exclude(checkin=None).count()
    count_ontime = Sheet.objects.filter(date=today, status='Đúng Giờ').exclude(checkin=None).count()
    count_manage = User.objects.filter(profile__position__name='Trưởng phòng').count()
    count_employee = User.objects.filter(profile__position__name='Nhân viên').count()
    count_it = User.objects.filter(profile__position__department__name='IT').count()
    count_nhansu = User.objects.filter(profile__position__department__name='Nhân sự').count()
    count_kinhdoanh = User.objects.filter(profile__position__department__name='Kinh doanh').count()
    count_taichinh = User.objects.filter(profile__position__department__name='Tài chính').count()
    count_thietke = User.objects.filter(profile__position__department__name='Thiết kế').count()
    count_sanxuat = User.objects.filter(profile__position__department__name='Sản xuất').count()
    count_mkt = User.objects.filter(profile__position__department__name='Marketing').count()
    count_dpm = Department.objects.count()

    context = {'title': title,
               'today': today,
               'count_late': count_late,
               'count_ontime': count_ontime,
               'count_manage': count_manage,
               'count_employee': count_employee,
               'count_emp': count_emp,
               'count_emp_male': count_emp_male,
               'count_emp_female': count_emp_female,
               'count_it': count_it,
               'count_nhansu': count_nhansu,
               'count_kinhdoanh': count_kinhdoanh,
               'count_thietke': count_thietke,
               'count_taichinh': count_taichinh,
               'count_sanxuat': count_sanxuat,
               'count_mkt': count_mkt,
               'count_dpm': count_dpm}
    return render(request, 'pages/management.html', context)
  else:
    messages.warning(request, 'Không có quyền truy cập')
    return redirect('/')

def employee(request):
  if request.user.is_superuser:
    title = 'Tất cả nhân viên'
    emps = User.objects.exclude(username='admin').order_by('-profile__start_date')
    departments = Department.objects.all()
    if request.POST:
      id = request.POST.get('leave')
      emp = Profile.objects.get(user__id=id)
      emp.end_date = datetime.now().date()
      emp.save()
      messages.success(request, 'Đã cho thằng này cút')
    keyword = request.GET.get('keyword', '')
    position = request.GET.get('position', '')
    start_date = request.GET.get('start-date', '')
    end_date = request.GET.get('end-date', '')
    department = request.GET.get('department', '')
    if keyword:
      emps = emps.filter(username__icontains=keyword)
    if position:
      emps = emps.filter(profile__position__name=position)
    if department:
      emps = emps.filter(profile__position__department__name=department)
    if start_date and end_date:
      emps = emps.filter(start_date__range=[start_date, end_date])
    elif start_date:
      emps = emps.filter(start_date__range=[start_date, datetime.now().date()])
    elif end_date:
      emps = emps.filter(start_date__range=[datetime.now().date(), end_date])
    paginator = Paginator(emps, 3)
    page_number = request.GET.get('page', '')
    try:
      page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
      page_obj = paginator.page(1)
    except EmptyPage:
      page_obj = paginator.page(paginator.num_pages)
    query_params = request.GET.copy()
    if 'page' in query_params:
      query_params.pop('page')
    context = {'title': title,
               'page_obj': page_obj,
               'departments': departments,
               'position': position,
               'department': department,
               'keyword': keyword,
               'start_date': start_date,
               'end_date': end_date,
               'query_params': query_params.urlencode()}
    return render(request, 'pages/employee.html', context)
  else:
    messages.warning(request, 'Không có quyền truy cập')
    return redirect('/')

def main_sheet(request):
  if request.user.is_superuser:
    title = 'Bảng công'
    sheets = Sheet.objects.all().order_by('-date')
    keyword = request.GET.get('keyword', '')
    status = request.GET.get('status', '')
    start_date = request.GET.get('start-date', '')
    end_date = request.GET.get('end-date', '')
    if keyword:
      sheets = sheets.filter(user__username__icontains=keyword)
    if status:
      sheets = sheets.filter(status=status)
    if start_date and end_date:
      sheets = sheets.filter(date__range=[start_date, end_date])
    elif start_date:
      sheets = sheets.filter(date__range=[start_date, datetime.now().date()])
    elif end_date:
      sheets = sheets.filter(date__range=[datetime.now().date(), end_date])
    paginator = Paginator(sheets, 1)
    page_number = request.GET.get('page', '')
    try:
      page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
      page_obj = paginator.page(1)
    except EmptyPage:
      page_obj = paginator.page(paginator.num_pages)
    query_params = request.GET.copy()
    if 'page' in query_params:
      query_params.pop('page')
    context = {'title': title, 
               'keyword': keyword,
               'start_date': start_date,
               'end_date': end_date,
               'status': status,
               'page_obj': page_obj,
               'query_params': query_params.urlencode()}
    return render(request, 'pages/main_sheet.html', context)
  else:
    messages.warning(request, 'Không có quyền truy cập')
    return redirect('/')
  
def total_salary(request):
  if request.user.is_superuser:
    title = 'Bảng lương'
    current_month = timezone.now().month
    current_year = timezone.now().year
    month_req = request.GET.get('month', current_month)
    year_req = request.GET.get('year', current_year)
    sheets = Sheet.objects.filter(
      date__month = month_req, 
      date__year = year_req).values('user__username', 'user__first_name', 'user__last_name').annotate(
        total_work_hour=Sum('work_hour'),
        total_salary=Sum('salary')).order_by('user__username')
    keyword = request.GET.get('keyword', '')
    if keyword:
      sheets = sheets.filter(user__username__icontains=keyword)
    return render(request, 'pages/total_salary.html', {'sheets': sheets, 'list_month':range(1, 13), 'list_year': range(2023,2026),
                                                       'year_req': int(year_req), 'title': title,
                                                       'month_req': int(month_req), 'keyword': keyword})
  else:
    messages.warning(request, 'Không có quyền truy cập')
    return redirect('/')