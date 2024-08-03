import os
import json
from datetime import datetime
import click
from flask.cli import with_appcontext
from chatbot import db


class Chat(db.Model):
    """
    Database model for chat information
    """
    id = db.Column(db.Integer, primary_key=True)
    log = db.Column(db.String(64), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    generated = db.Column(db.String(64), nullable=False)


    def serialize(self):
        """
        Function for serializing chat data item
        """
        return{
            "log": self.log,
            "date": datetime.isoformat(self.date),
            "generated": self.generated,
            "id": self.id
        }
    def deserialize(self, doc):
        """
        Function for deserializing chat data item
        """
        self.log = doc["log"]
        self.date = datetime.fromisoformat(str(doc["date"]))
        self.generated = doc["generated"]

    @staticmethod
    def json_schema():
        """
        JSON schema for chat
        """
        schema = {
            "type": "object",
            "required": ["log", "date"]
        }
        props = schema["properties"] = {}
        props["log"] = {
            "description": "",
            "type": "string"
        }
        props["date"] = {
            "description": "Datetime of the chat as a string",
            "type": "string"
        }
        props["generated"] = {
            "description": "generated answer",
            "type": "string"
        }
        return schema

@click.command("init-db")
@with_appcontext
def init_db_command():
    """
    Command for creating database
    """
    db.create_all()

@click.command("fill-db")
@with_appcontext
def fill_db_command():
    """
    Command for putting dummy data to database
    """
    with open(os.path.join(os.path.dirname(__file__), "tools", "dummy_data.json"), "r",
        encoding="utf-8") as file:
        dummy_data = json.load(file)
        for chat in dummy_data.get("Chats"):
            entry = Chat(log=chat.get("log"), date=datetime.strptime(chat.get("date"),
                        "%d/%m/%y %H:%M:%S"), generated=chat.get("generated"))
            db.session.add(entry)
        db.session.commit()
