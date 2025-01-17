import logging

# Configure the logging module to write logs to a file
logging.basicConfig(
    filename="signal_events.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log_event(message):
    """Logs an event with a timestamp."""
    logging.info(message)
