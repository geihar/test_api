# from django.utils.timezone import now
from .models import User

#
#
# class SetLastVisitMiddleware(object):
#     def process_response(self, request, response):
#         if request.user.is_authenticated():
#             # Update last visit time after request finished processing.
#             User.objects.filter(pk=request.user.pk).update(last_visit=now())
#         return response

from datetime import timedelta as td
from django.utils import timezone
from django.conf import settings
from django.db.models.expressions import F

# from <user profile path> import UserProfile


class LastUserActivityMiddleware(object):
    KEY = "last-activity"

    def process_request(self, request):
        if request.user.is_authenticated():
            last_activity = request.session.get(self.KEY)

            # If key is old enough, update database.
            too_old_time = timezone.now() - td(
                seconds=settings.LAST_ACTIVITY_INTERVAL_SECS
            )
            if not last_activity or last_activity < too_old_time:
                User.objects.filter(user=request.user.pk).update(
                    last_login=timezone.now()
                )
                # login_count=F('login_count') + 1)

            request.session[self.KEY] = timezone.now()

        return None
