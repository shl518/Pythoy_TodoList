from django.utils.deprecation import MiddlewareMixin
import datetime
from todo.models import Todo
import datetime


class update_expired(MiddlewareMixin):
    def process_request(self, request):
        widget = ['/login/', '/logout/', '/signup/', '/']
        if request.path_info in widget:
            return
        now = datetime.datetime.now()
        today = datetime.date.today()
        Todo.objects.filter(user=request.user, expiration_date__lt=now, datecompleted__isnull=True,
                            status__lt=3).update(status=3)

    def process_response(self, request, response):
        return response
