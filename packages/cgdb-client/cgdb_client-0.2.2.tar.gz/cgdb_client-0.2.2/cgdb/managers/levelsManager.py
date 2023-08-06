from cgdb.resources.level import Level
from cgdb.utils.ManagerMix import ManagerMix


class LevelsManager(ManagerMix):
    def __init__(self, client):
        super().__init__(client)

    def levels(self):
        content = self.get("levels")
        time_steps = []

        for raw in content:
            time_steps.append(Level(**raw))

        return time_steps

    def level_by_id(self, id):
        content = self.get("levels/id:" + str(id))

        return Level(**content)

    def level_by_code(self, code: str):
        content = self.get("levels/" + str(code))

        return Level(**content)
