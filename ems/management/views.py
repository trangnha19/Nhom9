from django.shortcuts import render, redirect
from django.db.models import Count, Q,Case, When, F, Sum, ExpressionWrapper, fields
from django.contrib import messages
from datetime import datetime, timedelta
from myapp.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from decimal import Decimal
from .forms import *

# Create your views here.
def home(request):
    if request.user.is_superuser:
        # for profile in Profile.objects.all():
        #   profile.save()
        title = 'Dashboard'
        count_emp = User.objects.count()
        count_emp_male = User.objects.filter(profile__gender='Nam').count()
        count_emp_female = User.objects.filter(profile__gender='Nữ').count()
        today = timezone.now().date()
        count_late = Sheet.objects.filter(date=today, status='Đến Muộn').exclude(checkin=None).count()
        count_ontime = Sheet.objects.filter(date=today, status='Đúng Giờ').exclude(checkin=None).count()
        count_manage = User.objects.filter(profile__position__name='Trưởng phòng').count()
        count_employee = User.objects.filter(profile__position__name='Nhân viên').count()
        count_leave_today = DayOffRequest.objects.filter(start_date__lte=datetime.now().date(), end_date__gte=datetime.now().date(), status='approved').count()
        count_dpm = Department.objects.count()
        count_it = User.objects.filter(profile__position__department__name='IT').count()
        count_nhansu = User.objects.filter(profile__position__department__name='Nhân sự').count()
        count_kinhdoanh = User.objects.filter(profile__position__department__name='Kinh doanh').count()
        count_taichinh = User.objects.filter(profile__position__department__name='Tài chính').count()
        count_thietke = User.objects.filter(profile__position__department__name='Thiết kế').count()
        count_sanxuat = User.objects.filter(profile__position__department__name='Sản xuất').count()
        count_mkt = User.objects.filter(profile__position__department__name='Marketing').count()
        it_work = Sheet.objects.filter(user__profile__position__department__name='IT', date=datetime.now().date()).count()
        nhansu_work = Sheet.objects.filter(user__profile__position__department__name='Nhân sự', date=datetime.now().date()).count()
        kinhdoanh_work = Sheet.objects.filter(user__profile__position__department__name='Kinh doanh', date=datetime.now().date()).count()
        taichinh_work = Sheet.objects.filter(user__profile__position__department__name='Tài chính', date=datetime.now().date()).count()
        thietke_work = Sheet.objects.filter(user__profile__position__department__name='Thiết kế', date=datetime.now().date()).count()
        sanxuat_work = Sheet.objects.filter(user__profile__position__department__name='Sản xuất', date=datetime.now().date()).count()
        mkt_work = Sheet.objects.filter(user__profile__position__department__name='Marketing', date=datetime.now().date()).count()
        letter_pending = Letter.objects.filter(status='Đang xử lý').count()
        day_off_pending = DayOffRequest.objects.filter(status='pending').count()
        context = {'title': title,
                  'today': today,
                  'count_late': count_late,
                  'count_ontime': count_ontime,
                  'count_manage': count_manage,
                  'count_employee': count_employee,
                  'count_emp': count_emp,
                  'count_emp_male': count_emp_male,
                  'count_emp_female': count_emp_female,
                  'count_leave_today': count_leave_today,
                  'count_dpm': count_dpm,
                  'count_it': count_it,
                  'count_nhansu': count_nhansu,
                  'count_kinhdoanh': count_kinhdoanh,
                  'count_thietke': count_thietke,
                  'count_taichinh': count_taichinh,
                  'count_sanxuat': count_sanxuat,
                  'count_mkt': count_mkt,
                  'it_work': it_work,
                  'nhansu_work': nhansu_work,
                  'kinhdoanh_work': kinhdoanh_work,
                  'taichinh_work': taichinh_work,
                  'thietke_work': thietke_work,
                  'sanxuat_work': sanxuat_work,
                  'mkt_work': mkt_work,
                  'letter_pending': letter_pending,
                  'day_off_pending': day_off_pending}
        return render(request, 'pages/management.html', context)
    else:
        messages.warning(request, 'Không có quyền truy cập')
        return redirect('/')

def employee(request):
    if request.user.is_superuser:
        title = 'Tất cả nhân viên'
        emps = User.objects.exclude(username='admin').order_by('-profile__start_date')
        departments = Department.objects.all()

        # Xử lý khi thay đổi trạng thái
        if request.POST:
            id = request.POST.get('change_status')
            status = request.POST.get('status')
            emp = Profile.objects.get(user__id=id)
            emp.status = status
            emp.save()
            messages.success(request, f"Trạng thái của nhân viên đã được cập nhật thành {dict(Profile.STATUS_CHOICES).get(status)}")
            # Redirect lại trang hiện tại
            return redirect('employee')  # Đảm bảo tên route 'employee' là đúng

        # Bộ lọc và phân trang
        keyword = request.GET.get('keyword', '')
        position = request.GET.get('position', '')
        start_date = request.GET.get('start-date', '')
        end_date = request.GET.get('end-date', '')
        department = request.GET.get('department', '')
        if keyword:
            emps = emps.filter(Q(first_name__icontains=keyword)|Q(last_name__icontains=keyword))
        if position:
            emps = emps.filter(profile__position__name=position)
        if department:
            emps = emps.filter(profile__position__department__name=department)
        if start_date and end_date:
            emps = emps.filter(profile__start_date__range=[start_date, end_date])
        elif start_date:
            emps = emps.filter(profile__start_date__gte=start_date)
        elif end_date:
            emps = emps.filter(profile__start_date__lte=end_date)

        # Thêm thông báo nếu không tìm thấy nhân viên
        if not emps.exists():
            messages.error(request, 'Không tìm thấy người dùng nào.')

        paginator = Paginator(emps, 10)
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

        context = {
            'title': title,
            'page_obj': page_obj,
            'departments': departments,
            'position': position,
            'department': department,
            'keyword': keyword,
            'start_date': start_date,
            'end_date': end_date,
            'query_params': query_params.urlencode(),
        }
        return render(request, 'pages/employee.html', context)
    else:
        messages.warning(request, 'Không có quyền truy cập')
        return redirect('/')

def create_employee(request):
   if request.user.is_authenticated:
       title = 'Thêm nhân viên'
       form_e = EmployeeCreateForm(request.POST or None)
       form_p = ProfileForm(request.POST or None, request.FILES or None)


       if request.POST:
           # Kiểm tra nếu form không hợp lệ
           if not form_e.is_valid() or not form_p.is_valid():
               messages.error(request, 'Thông tin nhập không hợp lệ. Vui lòng kiểm tra lại.')


           # Kiểm tra trùng lặp email
           elif User.objects.filter(email=form_e.cleaned_data.get('email')).exists():
               messages.error(request, 'Email đã tồn tại trong hệ thống.')
           else:
               # Lưu thông tin nhân viên và profile
               emp = form_e.save()
               profile = form_p.save(commit=False)
               profile.user = emp
               profile.save()
               messages.success(request, 'Thêm nhân viên thành công')
               return redirect('employee')


       context = {
           'title': title,
           'form_e': form_e,
           'form_p': form_p
       }
       return render(request, 'pages/create_employee.html', context)
   else:
       return redirect('/')

def update_employee(request, username):
    if request.user.is_superuser:
        try:
            user = User.objects.get(username=username)
            title = f'Sửa hồ sơ {user.username}'
            form_e = EmployeeUpdateForm(request.POST or None, instance=user)
            form_p = ProfileForm(request.POST or None, request.FILES or None, instance=user.profile)
            if request.POST:
                if form_e.is_valid() and form_p.is_valid():
                    form_e.save()
                    form_p.save()
                    messages.success(request, 'Chỉnh sửa hồ thành công')
                    return redirect('profile-detail', username=user.username)
            context = {'title': title,
                       'user': user,
                       'form_e':form_e,
                       'form_p':form_p}
            return render(request, 'pages/update_employee.html', context)
        except User.DoesNotExist:
            return redirect('home')
    else:
        return redirect('home')

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
    paginator = Paginator(sheets, 6)
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
        sheets = Sheet.objects.all()

        # Filter by keyword (username)
        keyword = request.GET.get('keyword', '')
        if keyword:
            sheets = sheets.filter(user__username__icontains=keyword)

        # Filter by department
        dpm_req = request.GET.get('dpm', '')
        if dpm_req and dpm_req != "Tất cả":
            sheets = sheets.filter(user__profile__position__department__name=dpm_req)

        # Get current month and year
        current_month = timezone.now().month
        current_year = timezone.now().year
        month_req = request.GET.get('month', current_month)
        year_req = request.GET.get('year', current_year)

        # Define constants
        num_days_in_month = 26

        # Fetch approved day-off requests
        approved_dayoff_requests = DayOffRequest.objects.filter(
            status='approved',
            start_date__year=year_req
        ).annotate(
            days_off=ExpressionWrapper(
                (F('end_date') - F('start_date')) + 1,
                output_field=fields.IntegerField()
            )
        )

        # Query the sheets with aggregation
        sheets = sheets.filter(
            date__month=month_req,
            date__year=year_req
        ).values(
            'user__id', 'user__username', 'user__first_name', 'user__last_name'
        ).annotate(
            total_work_hour=Sum('work_hour'),
            total_salary=F('user__profile__salary'),
            # late_count=Count(Case(When(status='Đến Muộn', then=1))),
            # total_late_count=F('late_count'),
            ot_sum=Sum('ot'),
            late_time=Sum('late_time'),
            days_worked=Count('date', distinct=True)
        ).order_by('user__id')

        # Calculate additional data for each sheet
        for sheet in sheets:
            # Fetch approved day-off requests
            previous_approved_days_off = approved_dayoff_requests.filter(
                user__username=sheet['user__username'],
                start_date__month__lt=month_req
            ).aggregate(total_requests=Count('id'))['total_requests'] or 0

            current_month_requests = approved_dayoff_requests.filter(
                user__username=sheet['user__username'],
                start_date__month=month_req
            )
            approved_days_off_current_month = current_month_requests.aggregate(
                total_requests=Count('id')
            )['total_requests'] or 0

            # Adjust approved days off if yearly limit exceeds 12
            if previous_approved_days_off + approved_days_off_current_month > 12:
                approved_days_off_current_month = max(0, 12 - previous_approved_days_off)

            # Calculate attendance days and missing days
            sheet['prev_approved_days_off'] = previous_approved_days_off
            sheet['approved_days_off'] = approved_days_off_current_month
            # sheet['missing_days'] = max(0, num_days_in_month - sheet['days_worked'])
            sheet['att_day'] = sheet['days_worked'] + approved_days_off_current_month

            # Calculate bonuses, penalties, and salary
            sheet['ot_sal'] = Decimal(100000) * Decimal(sheet['ot_sum'])
            sheet['awrd'] = Decimal(1000000) if sheet['ot_sum'] > 15 else Decimal(2000000) if sheet['ot_sum'] > 20 else 0
            sheet['neg_sal'] = Decimal(100000) * Decimal(sheet['late_time'])
            sheet['real_salary'] = int(sheet['total_salary'] / Decimal(26) * sheet['att_day'])

            # Calculate deductions for BHXH and TNCN
            bhxh = 0
            tncn = 0
            if sheet['days_worked'] > 12:
                bhxh = int(sheet['total_salary'] * Decimal(10.5) / Decimal(100))
                tncn = int(sheet['total_salary'] * Decimal(5) / Decimal(100))

            sheet['bhxh'] = bhxh
            sheet['tncn'] = tncn

            # Calculate final salary
            real_sal = sheet['real_salary'] - sheet['neg_sal'] - bhxh - tncn + sheet['awrd'] + sheet['ot_sal']
            sheet['real_sal'] = real_sal

        return render(request, 'pages/total_salary.html', {
            'sheets': sheets,
            'list_month': range(1, 13),
            'list_year': range(2023, 2026),
            'year_req': int(year_req),
            'title': title,
            'month_req': int(month_req),
            'keyword': keyword,
            'dpm_req': dpm_req,
            'dpms': Department.objects.all(),
        })

    else:
        messages.warning(request, 'Không có quyền truy cập')
        return redirect('/')


def letter(request):
  if request.user.is_authenticated:
    title = 'Danh sách đóng góp ý kiến'
    letters = Letter.objects.all().order_by('-created_at')
    topics = TopicLetter.objects.all()
    topic_rq = request.GET.get('topic', '')
    status = request.GET.get('status', '')
    time = request.GET.get('time', '')
    if topic_rq:
      letters = letters.filter(topic__name=topic_rq)
    if status:
      letters = letters.filter(status=status)
    if time:
      now = timezone.now()
      if time == 'Hôm nay':
        letters=letters.filter(created_at__date=now.date())
      elif 'ngày qua' in time:
        time_days_ago = now - timedelta(days=int(time[0]))
        letters = letters.filter(created_at__gte=time_days_ago)
    paginator = Paginator(letters, 10)
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
               'topics': topics,
               'time': time,
               'topic_rq': topic_rq,
               'status': status,
               'page_obj': page_obj,
               'query_params': query_params.urlencode()}
    return render(request, 'pages/main_letter.html', context)
  else:
    messages.warning(request, 'Không có quyền truy cập')
    return redirect('/')

def admin_review_requests(request):
    title = 'Đơn nghỉ phép'
    requests = DayOffRequest.objects.order_by('-start_date')
    status = request.GET.get('status', '')
    start_date = request.GET.get('start-date', '')
    end_date = request.GET.get('end-date', '')
    if status:
      if status == 'Đang chờ':
        requests = requests.filter(status='pending')
      elif status == 'Đã duyệt':
        requests = requests.filter(status='approved')
      else:
        requests = requests.filter(status='rejected')
    if start_date and end_date:
      requests = requests.filter(start_date__range=[start_date, end_date])
    elif start_date:
      requests = requests.filter(start_date__range=[start_date, datetime.now().date()])
    elif end_date:
      requests = requests.filter(start_date__range=[datetime.now().date(), end_date])

    paginator = Paginator(requests, 10)
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
    if request.POST:
        accept = request.POST.get('accept', '')
        refuse = request.POST.get('refuse', '')
        day_off_request = DayOffRequest.objects.get(id=accept if accept else refuse)
        day_off_request.status = 'approved' if accept else 'rejected'
        day_off_request.save()
        messages.success(request, 'Đã duyệt yêu cầu' if accept else 'Đã từ chối yêu cầu')
        return redirect('dayoff')
    context = {'title': title,
               'start_date': start_date,
               'end_date': end_date,
               'status': status,
               'page_obj': page_obj,
               'query_params': query_params.urlencode()}
    return render(request, 'pages/admin_review_requests.html', context)