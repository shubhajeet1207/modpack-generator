from json import JSONEncoder
from dataclasses import dataclass


class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ModInfo):
            return o.json()
        return o


@dataclass
class ModInfo:
    mod_name: str
    project_id: int
    file_id: int
    required: bool

    def json(self):
        return {
            "projectID": self.project_id,
            "fileID": self.file_id,
            "required": self.required
        }

    def __eq__(self, other):
        return isinstance(other, ModInfo) and self.project_id == other.project_id
