import os
import shutil
import sys
from pathlib import Path
from datetime import date
import time

import schedule

if os.getenv("PYTHON_ENV", "development") == "development":
    from dotenv import load_dotenv

    load_dotenv()

import settings
from src.utils import Utils

utils = Utils()
filters_path = sys.argv[1]


def job():
    weekly_folder = Path(settings.OUTPUT_FOLDER, f"output-{date.today().isoformat()}")
    weekly_folder.mkdir()

    prompt_filters = utils.read_filters(filters_path)
    for prompt_filter in prompt_filters:
        utils.export_json_data(prompt_filter=prompt_filter, test_export=False)
        utils.compress_output(test_export=False)

        filter_weekly_folder = Path(
            settings.OUTPUT_FOLDER, f"{prompt_filter}-{date.today().isoformat()}"
        )
        filter_weekly_folder.mkdir()

        shutil.move(settings.EXPORT_JSON_PATH, filter_weekly_folder)
        zip_list = Path(settings.OUTPUT_FOLDER).glob("*.zip")
        for zipfile in zip_list:
            shutil.move(zipfile, filter_weekly_folder)

        shutil.make_archive(
            base_name=str(filter_weekly_folder),
            format="zip",
            root_dir=filter_weekly_folder,
        )
        shutil.move(filter_weekly_folder.with_suffix(".zip"), weekly_folder)
        shutil.rmtree(filter_weekly_folder)


schedule.every().friday.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
