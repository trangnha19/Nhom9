from myapp.models import DayOffRequest, Letter

def pending_dayoff(request):
  count_pending = DayOffRequest.objects.filter(status='pending').count()
  return {'count_pending': count_pending}

def pending_letter(request):
    # Số lượng thư góp ý ở trạng thái 'Đang chờ duyệt'
    count_letter_pending = Letter.objects.filter(status='Đang xử lý').count()
    return {'count_letter_pending': count_letter_pending}