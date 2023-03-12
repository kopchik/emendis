#!/usr/bin/env python3
import csv

import click
import IPython
from sqlalchemy import insert, select  # noqa: F401

from . import models, schemas
from .db import get_db


@click.group()
def cli():
    pass


@cli.command()
def shell():
    # local shell context
    db = next(get_db())  # noqa: F841
    IPython.embed()


# separate function so can be used in tests
def load_csv(path, db=None):
    if not db:
        db = next(get_db())

    with open(path, "rt") as file:
        reader = csv.DictReader(file)

        rows = []
        for raw_data in reader:
            rows.append(schemas.SensorData.from_mapping(raw_data))

    db.execute(
        insert(models.SensorData).prefix_with("OR IGNORE"),
        [row.dict() for row in rows],
    )
    db.commit()


@cli.command("load-csv")
@click.argument("path", type=click.Path(exists=True))
def load_csv_command(path):
    load_csv(path)


if __name__ == "__main__":
    cli()
