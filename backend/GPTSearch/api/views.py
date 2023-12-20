import json

from django.http import HttpResponse, HttpResponseServerError, JsonResponse


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the api index.")


def echo(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)  # request.raw_post_data w/ Django < 1.4
        try:
            data = json_data['data']
        except KeyError:
            HttpResponseServerError("Malformed data!")
        return JsonResponse(data, status=200)
