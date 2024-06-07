from django.http import HttpRequest

def is_ajax(request: HttpRequest):
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"

