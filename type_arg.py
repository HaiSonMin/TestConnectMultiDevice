from typing import TypedDict
from datetime import datetime
from bson import ObjectId


class TypeDevice(TypedDict):
    deviceId: str
    deviceName: str
    deviceIndex: str

