import json
import os


RESULT_FILE = "edupath_results.json"


def save_results(results):
    """
    Save EduPath results to a JSON file.
    """

    with open(
        RESULT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=2,
            ensure_ascii=False
        )

    return True


def load_results():
    """
    Load previously saved EduPath results.

    Returns None if the file does not exist
    or cannot be read.
    """

    if not os.path.exists(RESULT_FILE):
        return None

    try:

        with open(
            RESULT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (
        json.JSONDecodeError,
        OSError
    ):

        return None


def results_exist():
    """
    Check whether saved results exist.
    """

    return os.path.exists(RESULT_FILE)


def delete_results():
    """
    Delete saved EduPath results.
    """

    if os.path.exists(RESULT_FILE):

        os.remove(RESULT_FILE)

        return True

    return False