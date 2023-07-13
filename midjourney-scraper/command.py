import logging
import os

import fire

if os.getenv("PYTHON_ENV", "development") == "development":
    from dotenv import load_dotenv

    load_dotenv()

from src.utils import Utils

from src.scraper import Scraper


class Command:
    def __init__(self):
        self._logger = logging.getLogger(f"scraper.{__name__}")
        Scraper.init_config()
        self._utils = Utils()

    def start_scraping(self) -> None:
        scraper = Scraper()
        scraper.start_scraping()

    def export_json_data(self) -> None:
        self._utils.export_json_data()

    def compress_output(self) -> None:
        self._utils.compress_output()


if __name__ == "__main__":
    fire.Fire(Command)