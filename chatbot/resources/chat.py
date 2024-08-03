import json
from datetime import datetime
from flask import Response, request, url_for
from flask_restful import Resource
from jsonschema import validate, ValidationError
from werkzeug.exceptions import UnsupportedMediaType, BadRequest
from sqlalchemy.exc import IntegrityError
from chatbot.models import db, Chat
from chatbot.utils import MasonBuilder
from worker.worker import get_response

MASON = "application/vnd.mason+json"

class chatCollection(Resource):
    """
    Resource for chat collections. Methods: get, post
    """
    def get(self):
        """
        Method for getting all chat information
        """
        #initialize response body
        body = []
        res = MasonBuilder()

        for item in Chat.query.all():
            chat_item = item.serialize()
            body.append(chat_item)

        res["chat"] = body
        res.add_control("self", "/api/chat/")
        res.add_control_post("chatbot:add-chat", "Add chat", "/api/chat/", Chat.json_schema())

        return Response(json.dumps(res), 200, mimetype=MASON)

    def post(self):
        """
        Method for adding new chat logs
        """
        #check that request is json
        print("JSON", request.is_json)
        print("Request Data:", request.get_data(as_text=True))
        print(request.headers)
        print("Request Content-Type:", request.content_type)
        print(type(request))
        if not request.is_json:
            raise UnsupportedMediaType
        #check json schema
        try:
            validate(request.json, Chat.json_schema())
        except ValidationError as error:
            raise BadRequest(description=str(error)) from error

        # get response from an LLM
        request.json["generated"] = get_response(request.json.get('log'))
        #initialize new chat using deserializer
        chat = Chat()
        chat.deserialize(request.json)

        #add new chat to database
        db.session.add(chat)
        db.session.commit()

        res = MasonBuilder()
        res.add_control("self", url_for("api.chatitem", chat=chat))

        return Response(json.dumps(res), 201, mimetype=MASON)

class chatItem(Resource):
    """
    Resource for single user chats. Methods: get, delete
    """
    def get(self, chat):
        """
        Method for getting user information for a specific user
        """
        res = MasonBuilder()
        res["log"] = chat.serialize()
        res.add_control("self", url_for("api.chatitem", chat=chat))
        res.add_control_delete("Delete chat", url_for("api.chatitem", chat=chat))
        
        return Response(json.dumps(res), 200, mimetype=MASON)

    def delete(self, chat):
        """
        Method for deleting existing chat
        """
        db.session.delete(chat)
        db.session.commit()
        #204 has no response body
        return Response(status=204)
