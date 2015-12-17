from django.db.models import F

from api.models import Endpoint


class TrackEndpointsHitMiddleware(object):
    # Check if client IP is allowed
    def process_view(self, request, view_func, view_args, view_kwargs):
        Endpoint.objects.filter(name=view_func.func_name).update(hits=F('hits')+1)
        return None