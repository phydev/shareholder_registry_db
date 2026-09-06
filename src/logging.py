import logging
import re


class SecretScrubbingFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        original_message = super().format(record)
        # Regex matches the 'user:password@' chunk inside connection strings
        scrubbed_message = re.sub(r":\/\/(.*):(.*)@", r"://****:****@", original_message)
        return scrubbed_message


def setup_logger() -> None:
    console_handler = logging.StreamHandler()

    formatter = SecretScrubbingFormatter(
        fmt="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
