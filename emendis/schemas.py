import base64
from datetime import datetime
from typing import TypeAlias

import orjson as json
from pydantic import BaseModel

SensorId: TypeAlias = int
AvgDwellTime: TypeAlias = float


class SensorData(BaseModel):
    sensor_id: SensorId
    dwell_time: float
    timestamp: datetime

    @classmethod
    def validate(cls, v):
        if isinstance(v, str):  # we got base64 encoded JSON
            v = cls.load_base64_json(v)

        return super().validate(v)

    @classmethod
    def load_base64_json(cls, v):
        try:
            raw_json = base64.b64decode(v)
        except Exception as e:
            raise ValueError(f"Invalid base64 data: {e}")

        try:
            raw_data = json.loads(raw_json)
        except Exception as e:
            raise ValueError(f"Invalid JSON data: {e}")

        return cls._remap(raw_data)

    @classmethod
    def _remap(cls, raw_data):
        mapping = {
            "v0": "sensor_id",
            "v18": "dwell_time",
            "Time": "timestamp",
        }
        data = {}
        for orig, dst in mapping.items():
            if orig not in raw_data:
                raise ValueError(f"Missing field: {orig} in sensor data")
            data[dst] = raw_data[orig]

        return data

    @classmethod
    def from_mapping(cls, raw_data):
        return cls(**cls._remap(raw_data))

    class Config:
        orm_mode = True


# NB duplicate attributes (e.g., message_id and messageId) are removed
class PubSubMessage(BaseModel):
    class Message(BaseModel):
        attributes: dict
        data: SensorData
        message_id: str
        publish_time: str

    message: Message
    subscription: str


class ExportSensorData(BaseModel):
    data: dict[SensorId, list[SensorData]]


class ExportAvgDwellTime(BaseModel):
    class SensorAvg(BaseModel):
        sensor_id: SensorId
        avg_dwell_time: AvgDwellTime

    data: list[SensorAvg]
