from peewee import *
from BaseModel import *
from misc_functions import *

class ItemTypeData(BaseModel):
    name = CharField()

    def to_string(self):
        return str(self.name)