import datetime
import os
import json
from chatbot.models import Chat

def populate_database(db, app):
    """
    Dump contents of dummy_data.json to database
    """
    try:
        with open(os.path.join(os.path.dirname(__file__), "dummy_data.json"), "r",
            encoding="utf-8") as file:
            dummy_data = json.load(file)
            for chat in dummy_data.get("Chats"):
                entry = Chat(log=chat.get("log"),log_date=datetime.datetime.strptime(chat.get("date"),"%d/%m/%y %H:%M:%S"))
                db.session.add(entry)
            db.session.commit()
            return True

    except Exception:
        return False
