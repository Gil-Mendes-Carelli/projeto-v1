import logging
from datetime import datetime, timezone


class TextFormatter(logging.Formatter):
    def format(self, record):
        timestamp = datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat()
        variable = record.msg.get("variable", "")
        value = record.msg.get("value", "")

        return f"""{'='*80}
    [{timestamp}]
    Variable: {variable}
    Value:
    {value}
    {'='*80}
    """


def setup_txt_logger(name, log_file):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent adding duplicate handlers
    if not logger.handlers:
        handler = logging.FileHandler(log_file, encoding="utf-8")
        formatter = TextFormatter()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
