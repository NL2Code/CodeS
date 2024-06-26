from vibora.blueprints import Blueprint
from vibora.responses import JsonResponse

v1 = Blueprint()


@v1.route("/")
def home():
    return JsonResponse({"hello": "world"})


@v1.route("/exception")
def exception():
    raise Exception("oi")


@v1.handle(IOError)
def handle_exception():
    return JsonResponse({"msg": "Exception caught correctly."})
