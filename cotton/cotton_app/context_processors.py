from .models import Notification, UserRegistration

def notification_count(request):
    if request.session.get('username'):
        try:
            user = UserRegistration.objects.get(email=request.session['username'])
            count = Notification.objects.filter(user=user, is_read=False).count()
            return {'notifications_unread_count': count}
        except UserRegistration.DoesNotExist:
            return {}
    return {}
