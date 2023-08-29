from chat_parser.parser_data_classes import Chat
from DB.models import Groups
from app import db
from abc import ABC, abstractmethod
from filterer import GroupJsonFilterer


ERROR_PARSING = "Error while parsing: "
CHAT_ERROR_PARSING = ERROR_PARSING + "Error while parsing specific chat."


class ParserCoverter(ABC):


    @abstractmethod
    def convert(self, items) -> list:
        pass


class JsonChatsToGroupConverter(ParserCoverter):


    def __init__(self, user_id:str) -> None:
        super().__init__()
        self.filterer = GroupJsonFilterer()
        self.json_to_dc = JsonToGroupDCConverter(user_id)
        self.dc_to_db_recs = GroupDCToDBRecsConverter()


    def convert(self, group_chats: dict) -> list[Groups]:
        only_group = self.filterer.filter(group_chats)
        dc_groups = self.json_to_dc.convert(only_group)
        groups_db = self.dc_to_db_recs.convert(dc_groups)

        db.session.add_all(groups_db)
        db.session.commit()

        return groups_db


class JsonToGroupDCConverter(ParserCoverter):


    def __init__(self, user_id : str) -> None:
        self.user_id = user_id


    def convert(self, group_chats: dict) -> list[Chat]:
        dc_chats = []
        for json_chat in group_chats:
            dc_chat = self.create_dc_from(json_chat)
            dc_chats.append(dc_chat)

        return dc_chats


    def create_dc_from(self, json_chat: dict) -> Chat:
        try:
            dc_chat = Chat(
                group_id=json_chat.get("groupMetadata").get("_serialized"),
                group_name=json_chat.get("subject"),
                user_id= self.user_id,
            )
        except KeyError:
            raise KeyError(CHAT_ERROR_PARSING)

        return dc_chat


class GroupDCToDBRecsConverter(ParserCoverter):


    def convert(self, dc_chats: list[Chat]) -> list[Groups]:
        db_groups = []
        for dc_chat in dc_chats:
            db_group = Groups(
                user_id=dc_chat.user_id,
                group_id=dc_chat.group_id,
                group_name=dc_chat.group_name
            )
            db_groups.append(db_group)

        return db_groups