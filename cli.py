#!/usr/bin/env python3
import click
from IPython import embed
from emendis import models, schemas
from emendis.db import get_db
from sqlalchemy import select, insert  # noqa: F401
import csv
from datetime import datetime


@click.group()
def cli():
    pass


@cli.command()
def shell():
    db = next(get_db())
    embed()


@cli.command()
@click.argument("file", type=click.File("rt"))
def load_csv(file):
    db = next(get_db())
    reader = csv.DictReader(file)

    rows = []
    for raw_data in reader:
        rows.append(schemas.SensorData.from_mapping(raw_data))

    db.execute(
        insert(models.SensorData).prefix_with("OR IGNORE"),
        [row.dict() for row in rows],
    )
    db.commit()


if __name__ == "__main__":
    cli()
