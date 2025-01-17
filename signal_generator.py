import random
import time

def generate_signal():
    """Generates random signals."""
    signals = [
        "Code Blue: Safe",
        "Code Orange: Possible Incident",
        "Code Red: Signal loss or Health issue"
    ]
    while True:
        yield random.choice(signals)

if __name__ == "__main__":
    generator = generate_signal()
    while True:
        print(next(generator))
        time.sleep(random.randint(5, 10))  # Generate a signal every 5–10 seconds
