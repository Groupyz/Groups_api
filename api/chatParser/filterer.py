from abc import ABC, abstractmethod
from chatParser.specification import GroupJsonSpecification


class ChatsJsonFilterer(ABC):

    def __init__(self) -> None:
     super().__init__()
     self.filtered_recs = []

    @abstractmethod
    def filter(self, chats: dict) -> list[dict]:
        pass


class GroupJsonFilterer(ChatsJsonFilterer):
    def __init__(self) -> None:
        super().__init__()
        self.specification = GroupJsonSpecification()

    def filter(self, chats: dict) -> list[dict]:
        for chat in chats:
            if self.specification.is_satisfied(chat):
                self.filtered_recs.append(chat)

        return self.filtered_recs