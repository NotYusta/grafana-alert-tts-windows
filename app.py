import pyttsx3
import yaml
from flask import Flask, request
import threading
import queue

# Allowed notification targets
VALID_TARGETS = ["folder"]
config = {}

def load_config():
    global config
    with open("config.yaml", "r", encoding="utf-8") as f:
        configYml: dict = yaml.safe_load(f)

    svConf = configYml.get("server", {})
    config = {
        "server_port": svConf.get("port", 8000),
        "server_path": svConf.get("path", "/notify"),
        "voice_name": configYml.get("voiceModel", "").lower(),
        "target_notification": configYml.get("targetNotification", "").lower(),
        "messages": configYml.get("messages", {}),
    }


load_config()

# Validate target notification
if config["target_notification"] not in VALID_TARGETS:
    print(f"⚠️ Invalid targetNotification: '{config['target_notification']}'")
    print(f"✅ Available options: {', '.join(VALID_TARGETS)}")
    exit()


# Create a queue for speech
speech_queue = queue.Queue()


# Background speech worker
def speech_worker():
    while True:
        message = speech_queue.get()
        try:
            # Re-initialize the engine every time
            local_engine = pyttsx3.init()
            for voice in local_engine.getProperty("voices"):
                if config["voice_name"] in voice.name.lower():
                    local_engine.setProperty("voice", voice.id)
                    break

            print(f"🔊 Speaking: {message}")
            local_engine.say(message)
            local_engine.runAndWait()
            local_engine.stop()

        except Exception as e:
            print(f"❌ Error while speaking: {e}")
        speech_queue.task_done()


# Start the speech worker thread
threading.Thread(target=speech_worker, daemon=True).start()

# Initialize Flask app
app = Flask(__name__)


@app.route(config["server_path"], methods=["POST"])
def notify():
    data = request.json
    alerts = data.get("alerts", [])
    if not alerts:
        return "", 204

    for alert in alerts:
        labels = alert.get("labels", {})
        status = alert.get("status", "").lower()
        alert_name = labels.get("alertname", "tidak diketahui")
        alert_folder = labels.get("grafana_folder", "tidak diketahui")
        template = config["messages"].get(status, config["messages"]["default"])
        # Replace status using config, fallback to raw
        status_friendly = config["messages"].get("status", {}).get(status, status)

        message = template.format(
            alert_name=alert_name, status=status_friendly, alert_folder=alert_folder
        )

        print(f"📝 Queued: {message}")
        speech_queue.put_nowait(message)

    return "", 204  # No content


if __name__ == "__main__":
    app.run(port=config["server_port"])
