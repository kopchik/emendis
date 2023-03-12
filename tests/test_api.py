import base64

import orjson as json

from emendis.cli import load_csv

from .conftest import client


def dump_base64(obj: object) -> str:
    raw_json = json.dumps(obj)
    return base64.b64encode(raw_json).decode()


class Test_endpoints:
    test_message = {
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
        # perhaps needs to be split into two tests
        r = client.post(
            "/imports/sensor-data",
            json=[self.test_message],
        )
        assert r.status_code == 200, r.json()

        r = client.get("/exports/sensor-data")
        assert r.status_code == 200, r.json()
        assert r.json() == {
            "data": {
                "100013": [
                    {
                        "sensor_id": 100013,
                        "dwell_time": 2.72,
                        "timestamp": "2022-11-08T04:00:04.317801",
                    }
                ]
            }
        }

    def test_kpi(self, db):
        load_csv("tests/test_data.csv", db=db)
        r = client.get("/exports/sensor-data/kpi")
        assert r.json() == {
            "data": [
                {"avg_dwell_time": 9.206277056277052, "sensor_id": 100013},
                {"avg_dwell_time": 10.77262910798122, "sensor_id": 100022},
            ],
        }
