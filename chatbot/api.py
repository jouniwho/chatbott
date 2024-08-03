from flask import Blueprint
from flask_restful import Api

from chatbot.resources.chat import chatCollection, chatItem


api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

api.add_resource(chatCollection, "/chat/")
api.add_resource(chatItem, "/chat/<chat:chat>/")
