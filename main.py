from src.cli.cli import *
from src.db.database import *
from src.exceptions.exception import *
from pathlib import Path


db_location = Path('./data/tasks.db')
db_handler = DataBaseHandler(db_location)
c  = Cli(db_handler)
c.app()
