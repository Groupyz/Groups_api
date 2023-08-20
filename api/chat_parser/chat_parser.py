from chat_parser.parser_data_classes import Summary, Chat
from DB.models import Groups
from app import db

ERROR_PARSING = "Error while parsing: "
CHAT_ERROR_PARSING = ERROR_PARSING + "Error while parsing specific chat."


class ChatParser:
    def __init__(self, chats_json, user_id: str):
        self.summary = Summary(0, 0, None)
        self.user_id = user_id

    def create_db_records(self, chats: list[Chat]) -> list[Groups]:
        groups = []
        for chat in chats:
            group = Groups(
                user_id=chat.user_id, group_id=chat.group_id, group_name=chat.group_name
            )
            groups.append(group)

        db.session.add_all(groups)
        db.session.commit()

        return groups

    def create_chat(self, json_chat: dict) -> Chat:
        try:
            chat = Chat(
                group_id=json_chat.get("id").get("_serialized"),
                group_name=json_chat.get("name"),
                user_id=self.user_id,
            )
        except Exception as e:
            raise Exception(CHAT_ERROR_PARSING)

        return chat
