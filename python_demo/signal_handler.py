import random
import time
from event_logger import log_event
from geopy.geocoders import Nominatim
import smtplib
from email.message import EmailMessage

# Global variables
system_state = "idle"
geolocation_log = []  # 2D array to store geolocation with timestamps
email_dict = {
    1: "email1@example.com",
    2: "email2@example.com",
    3: "email3@example.com",
    4: "email4@example.com"
}

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "your_email@example.com"  # Replace with your email
EMAIL_PASSWORD = "your_password"  # Replace with your email password

def bold_text(text):
    """Returns bolded text using ANSI escape codes."""
    return f"\033[1m{text}\033[0m"  # Bold text

def send_alert_emails(subject, body):
    """Sends email alerts to predefined addresses with a subject and body."""
    log_event("Sending email alerts.")
    try:
        for email in email_dict.values():
            msg = EmailMessage()
            msg["From"] = EMAIL_SENDER
            msg["To"] = email
            msg["Subject"] = subject
            msg.set_content(body)
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.send_message(msg)
        log_event("Email alerts sent successfully.")
    except Exception as e:
        log_event(f"Failed to send email alerts: {e}")

def get_geolocation():
    """Fetches the current geolocation."""
    try:
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode("Your City Name")  # Replace with a specific location or logic
        return location.address
    except Exception as e:
        log_event(f"Failed to fetch geolocation: {e}")
        return "Unknown Location"

def log_event_to_file(timestamp, location, event_log):
    """Logs event details (timestamp, location, and event log) into a file."""
    with open("event_logs.txt", "a") as file:
        file.write(f"Timestamp: {timestamp}\n")
        file.write(f"Location: {location}\n")
        file.write(f"Event Log: {event_log}\n")
        file.write("-" * 50 + "\n")

def handle_code_red():
    """Handles a Code Red incident."""
    global system_state
    system_state = "handling an alarm"
    log_event(bold_text("ALARM! Immediate action required."))

    # Get geolocation and log it
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    location = get_geolocation()
    log_event(f"Geolocation of Code Red: {location}")
    geolocation_log.append([timestamp, location])

    # Send initial email alerts for Code Red
    send_alert_emails(
        "Code Red Alert!",
        f"Code Red triggered at location: {location}, Time: {timestamp}."
    )

    # Allow the user to interactively resolve the issue
    resolve_alarm(timestamp, location)

def resolve_alarm(timestamp, location):
    """Allows the user to redirect alarms to the authorities with an event log."""
    while True:
        print(bold_text("\n--- Code Red Alarm ---"))
        print("Enter an event log to redirect alarms to the authorities:")
        event_log = input("Event Log: ").strip()
        if event_log:
            log_event(f"Event entered: {event_log}")
            log_event("Alarms redirected to valid authorities. System returning to idle state.")
            print(bold_text("Alarms have been redirected to the valid authorities."))

            # Email the event log to stakeholders
            send_alert_emails(
                "Code Red Event Log",
                f"Event log: {event_log}\nLocation: {location}\nTime: {timestamp}"
            )

            # Store the event log in the file
            log_event_to_file(timestamp, location, event_log)

            global system_state
            system_state = "idle"
            break
        else:
            print("Please enter a valid event log.")

def handle_code_orange():
    """Handles the 15-minute countdown and user confirmation for Code Orange."""
    global system_state
    system_state = "waiting for confirmation"
    log_event(bold_text("Code Orange received. Starting 15-minute countdown."))
    print(bold_text("\n--- Code Orange: Possible Incident ---"))
    print("You have 15 minutes to confirm your state. Enter 'clear' to confirm or 'failure' to escalate.")

    start_time = time.time()
    duration = 15 * 60  # 15 minutes in seconds

    while time.time() - start_time < duration:
        remaining_time = int(duration - (time.time() - start_time))
        minutes, seconds = divmod(remaining_time, 60)
        print(f"Time remaining: {minutes:02}:{seconds:02}", end="\r")
        try:
            user_input = input("\nEnter 'clear' or 'failure': ").strip().lower()
            if user_input == "clear":
                log_event("User confirmed state is clear. Timer stopped.")
                print(bold_text("Thank you for confirming. Resuming normal operations."))
                system_state = "idle"
                return
            elif user_input == "failure":
                log_event("User indicated failure. Triggering alarm and Code Red.")
                handle_code_red()
                return
            else:
                print("Invalid input. Please enter 'clear' or 'failure'.")
        except EOFError: # end of the file without data received
            pass

    log_event("No confirmation received within 15 minutes. Escalating.")
    handle_code_red()

def handle_signal(signal):
    """Handles the received signal."""
    global system_state
    log_event(f"Received signal: {signal}")
    if signal == "Code Blue: Safe":
        log_event("Status is safe. No action needed.")
    elif signal == "Code Orange: Possible Incident":
        if system_state == "idle":  # Only handle if no higher-priority action is ongoing
            handle_code_orange()
        else:
            log_event(f"Ignored Code Orange because system is in state: {system_state}.")
    elif signal == "Code Red: Signal loss or Health issue":
        log_event(bold_text("Code Red received. Sounding alarm."))
        handle_code_red()
    else:
        log_event(f"Unknown signal: {signal}")

def simulate_signal():
    """Simulates random signal generation and handles them."""
    signals = [
        "Code Blue: Safe",
        "Code Orange: Possible Incident",
        "Code Red: Signal loss or Health issue"
    ]
    while True:
        signal = random.choice(signals)
        handle_signal(signal)
        if system_state == "idle":  # Only continue signal generation if idle
            time.sleep(random.randint(5, 15))  # Wait for a random interval between signals

if __name__ == "__main__":
    log_event("Signal handling program started.")
    try:
        simulate_signal()
    except KeyboardInterrupt:
        log_event("Program interrupted by user.")
