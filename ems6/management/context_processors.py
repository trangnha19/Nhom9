from myapp.models import DayOffRequest

def pending_dayoff(request):
  count_pending = DayOffRequest.objects.filter(status='pending').count()
  return {'count_pending': count_pending}