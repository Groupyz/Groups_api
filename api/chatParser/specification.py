from abc import ABC, abstractmethod



class Specification(ABC):

    @abstractmethod
    def is_satisfied(self, item):
        pass


class GroupJsonSpecification(Specification):

    def is_satisfied(self, item):
        return item.get("isGroup") == True