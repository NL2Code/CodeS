from vibora import Request, Vibora
from vibora.responses import JsonResponse
from vibora.schemas import Schema, fields


class SimpleSchema(Schema):
    name: str


app = Vibora()


@app.route("/", methods=["POST"])
async def home(request: Request):
    return JsonResponse({"name": (await request.json())["name"]})


if __name__ == "__main__":
    app.run(debug=False, port=8000, host="0.0.0.0", workers=8)
