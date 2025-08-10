from logging import Logger
import yaml  # type: ignore


def ask_for_input(attempt_number: int) -> str:
    """
    Prompts user for his credentials.yaml filepath.

    Returns:
        str: absolute filepath to user's .yaml credentials file
    """
    if attempt_number == 1:
        return input("\nAbsolute filepath for credentials (stop is Ctrl+C): ").strip()
    else:
        return input("\ntry again (stop is Ctrl+C): ").strip()


def parse_yaml_file(file_path: str, logger: Logger) -> dict:
    if not file_path:
        logger.info("Please provide a file path.")
        return {}
    elif not file_path.endswith(".yaml"):
        logger.info("Only .yaml files.")
        return {}
    try:
        with open(file_path, "r") as file:
            credentials = yaml.safe_load(file)
            if not isinstance(credentials, dict):
                logger.info("Invalid credentials format, check your .yaml format.")
                return {}
            return credentials
    except FileNotFoundError:
        logger.info(f"File not found: {file_path}")
        return {}
    except KeyError:
        logger.info("Please check your .yaml variables names")
        return {}
