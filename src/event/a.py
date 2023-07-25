from sanic.response import json
from sanic import Blueprint

bp = Blueprint("EXAMPLE")


@bp.route("/EXAMPLE")
async def bp_root(request):
    return json({"my": "blueprint"})
