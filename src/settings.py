from pathlib import Path
from loguru import logger
from pydantic import BaseModel
from datetime import datetime


class Settings(BaseModel):
    basedir: Path = Path.cwd()
    logdir: Path = basedir / "logs"
    loglevel: str = "DEBUG"
    logfile: Path = logdir / f'{datetime.now().strftime("%Y-%m-%d")}.log'
    data_dir: Path = Path("data//raw")
    outputdir: Path = Path("data//processed")

    schiphol_lat: int = 52.3080392
    schiphol_lon: int = 4.7621975

    temp_start_date: str = "2010-01-01"
    temp_end_date: str = "2020-12-01"


settings = Settings()
logger.add(settings.logfile, level=settings.loglevel)
