import pathlib
from pathlib import Path

base_dir: Path = pathlib.Path(__file__).resolve().parent.parent

database = 'conf/database.ini'
DATABASE_INI_PATH: Path = base_dir.joinpath(database)

work_json = 'work/w_1.json'
WORK_JSON_PATH: Path = base_dir.joinpath(work_json)