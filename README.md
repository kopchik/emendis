# Emendis test task

## installation 

Inside *virtual environment*:
```sh
pip install -r requirements.txt
pip install -e .
```

## Running the code

```sh
# migrate database
alembic upgrade head

# load some test data
emendis load-csv tests/test_data.csv

# start webserver
uvicorn emendis.main:app --reload
```

Then navigate to http://localhost:8000/docs to see this beatiful documentation:
![api](https://github.com/kopchik/emendis/blob/master/pics/api.png)


## Other commands

See `Makefile` for some other useful commands. Also there is a cli (`emendis`).

## Output format and filtering

The export endpoint supports basic filtering by sensor id and timestamp. Output json is somewhat compatible with plotting libraries that I used to work with. Please see swagger for details (http://localhost:8000/docs).

## Some quirks

- Import endpoint accepts multiple pubsub messages at once. On a second thought it's probably not how google's pub/sub works.
- Authentication code in auth.py is incomplete: it doesn't check tokens.
- Tests are rudimentary and don't cover everything.
- Database indexes should help with range queries, but I didn't actually check the execution plans. Behaviour on large datasets wasn't tested (but "should just work" (TM)).
