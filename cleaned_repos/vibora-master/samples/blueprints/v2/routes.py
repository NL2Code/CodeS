from vibora.blueprints import Blueprint
from vibora.responses import JsonResponse

v2 = Blueprint()


@v2.route("/")
def home():
    return JsonResponse({"a": 2})


@v2.route("/exception")
def exception():
    raise IOError("oi")


@v2.handle(Exception)
def handle_exception():
    return JsonResponse({"msg": "Exception catched correctly on v2."})
