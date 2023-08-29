from chat_parser.parser_data_classes import Summary, Chat
from DB.models import Groups
from app import db

# ERROR_PARSING = "Error while parsing: "
# CHAT_ERROR_PARSING = ERROR_PARSING + "Error while parsing specific chat."


# class ChatParser:
#     def __init__(self, chats_json, user_id: str):
#         self.summary = Summary(0, 0, None)
#         self.user_id = user_id
#         self.chats_json = chats_json

#     def parse(self) -> Summary:
#         self.chats = self.create_chats()
#         created_groups = self.create_db_records(self.chats)
#         self.summary = Summary(len(self.chats), len(self.chats_json), self.user_id)

#         return self.summary

#     def create_chats(self) -> list[Chat]:
#         self.chats = []
#         for json_chat in self.chats_json:
#             try:
#                 chat = self.create_chat(json_chat)
#                 self.chats.append(chat)
#             except KeyError:
#                 self.summary.total_records_failed += 1

#         self.summary.total_records_created = len(self.chats)

#         return self.chats

#     def create_chat(self, json_chat: dict) -> Chat:
#         try:
#             chat = Chat(
#                 group_id=json_chat.get("id").get("_serialized"),
#                 group_name=json_chat.get("name"),
#                 user_id=self.user_id,
#             )
#         except KeyError:
#             raise Exception(CHAT_ERROR_PARSING)

#         return chat

#     def create_db_records(self, chats: list[Chat]) -> list[Groups]:
#         groups = []
#         for chat in chats:
#             group = Groups(
#                 user_id=chat.user_id, group_id=chat.group_id, group_name=chat.group_name
#             )
#             groups.append(group)

#         db.session.add_all(groups)
#         db.session.commit()

#         return groups



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