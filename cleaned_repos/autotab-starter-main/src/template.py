import argparse
from typing import Optional

import utils.params as params  # noqa: F401
from selenium.webdriver.common.action_chains import ActionChains  # noqa: F401
from selenium.webdriver.common.by import By  # noqa: F401
from selenium.webdriver.common.keys import Keys  # noqa: F401
from selenium.webdriver.support import expected_conditions as EC  # noqa: F401
from selenium.webdriver.support.ui import Select  # noqa: F401
from selenium.webdriver.support.ui import WebDriverWait  # noqa: F401
from utils.auth import google_login, login  # noqa: F401
from utils.driver import get_driver


def main(params_filepath: Optional[str] = None):
    driver = get_driver()  # noqa: F841
    if params_filepath:
        params.load(filepath=params_filepath)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", help="Specify the data file path", default=None)
    args = parser.parse_args()
    main(params_filepath=args.data)
