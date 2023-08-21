import json
import logging


class ElasticSearchLogger(logging.Handler):
    """Custom email logger."""

    def __init__(self) -> None:
        """Initialize the logger."""
        logging.Handler.__init__(self)

    def emit(self, record):
        """
        Emit a record.

        Format the record and send it to the specified addressees.
        """
        try:
            log_record = json.loads(self.format(record))
            print(log_record)
            print('Elasticsearch logger')
        except Exception as e:
            print(f"Exception: {e}")

    def close(self):
        """Terminate the handler."""
        logging.Handler.close(self)