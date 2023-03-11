import base64

import orjson as json
from fastapi.testclient import TestClient

from emendis.main import app

client = TestClient(app)


def dump_base64(obj: object) -> str:
    raw_json = json.dumps(obj)
    return base64.b64encode(raw_json).decode()


class Test_endpoints:
    one_data_entry = {
        "message": {
            "attributes": {"key": "value"},
            "data": dump_base64(
                {"v0": 100013, "v18": 2.72, "Time": "2022-11-08T04:00:04.317801"}
            ),
            "messageId": "2070443601311540",
            "message_id": "2070443601311540",
            "publishTime": "2021-02-26T19:13:55.749Z",
            "publish_time": "2021-02-26T19:13:55.749Z",
        },
        "subscription": "projects/myproject/subscriptions/mysubscription",
    }

    def test_import_and_export_of_data(self):
        # TODO: test with multiple messages
        r = client.post(
            "/imports/sensor-data",
            json=[self.one_data_entry],
        )
        assert r.status_code == 200, r.json()

        r = client.get("/exports/sensor-data")
        assert r.status_code == 200, r.json()
        assert r.json() == [
            {
                "dwell_time": 2.72,
                "sensor_id": 100013,
                "timestamp": "2022-11-08T04:00:04.317801",
            }
        ]
