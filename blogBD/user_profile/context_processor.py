from matplotlib.style import context
from notification.models import Notifications

def user_notifications(request):
    context={
        
    }
    if request.user.is_authenticated:
        notifications=Notifications.objects.filter(
            user  = request.user
        ).order_by('-created_date')
        not_read = notifications.exclude(is_seen = True)
        context['notifications'] = notifications
        context['not_read'] = not_read.count()


    return context
