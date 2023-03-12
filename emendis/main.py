import itertools
from datetime import datetime

from fastapi import Depends, FastAPI
from fastapi_auth_middleware import AuthMiddleware
from fastapi_filter import FilterDepends
from fastapi_filter.contrib.sqlalchemy import Filter
from sqlalchemy import Insert, func, select
from sqlalchemy.orm import Session

from . import models, schemas
from .auth import verify_authorization_header
from .db import get_db

app = FastAPI(title="Emendis sensor API")
app.add_middleware(AuthMiddleware, verify_header=verify_authorization_header)


@app.post("/imports/sensor-data")
def import_sensor_data(
    messages: list[schemas.PubSubMessage],
    db: Session = Depends(get_db),
):
    db.execute(
        Insert(models.SensorData).prefix_with("OR IGNORE"),  # ON DUPLICATE KEY IGNORE
        [msg.message.data.dict() for msg in messages],
    )
    db.commit()
    return {"message": "ok"}


class SensorFilter(Filter):
    sensor_id__in: list[int] | None
    timestamp__gte: datetime | None
    timestamp__lte: datetime | None

    class Constants(Filter.Constants):
        model = models.SensorData


# TODO: pagination or streaming
@app.get(
    "/exports/sensor-data",
    response_model=schemas.ExportSensorData,
)
def export_sensor_data(
    db: Session = Depends(get_db),
    filter: SensorFilter = FilterDepends(SensorFilter),
):
    query = (
        select(models.SensorData)
        .order_by("sensor_id", "timestamp")
        .limit(
            1_000_000
        )  # just in case, TODO: it should raise an error if limit is reached
    )
    query = filter.filter(query)
    rows = db.scalars(query)
    grouped = {k: list(g) for k, g in itertools.groupby(rows, lambda sd: sd.sensor_id)}
    return {"data": grouped}


@app.get(
    "/exports/sensor-data/kpi",
    response_model=schemas.ExportAvgDwellTime,
)
def export_sensor_kpi(db: Session = Depends(get_db)):
    rows = db.execute(
        select(
            models.SensorData.sensor_id,
            func.avg(models.SensorData.dwell_time).label("avg_dwell_time"),
        ).group_by("sensor_id")
    )
    return {"data": [r._asdict() for r in rows]}


# TODO: auth
