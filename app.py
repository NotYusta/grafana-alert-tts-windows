import pyttsx3
import yaml
from flask import Flask, request
import threading
import time

# Allowed notification targets
VALID_TARGETS = ["folder"]
config = {}

# Message queue for rotation
loop_messages = []  # List of dicts: {message, max, interval, count}
loop_lock = threading.Lock()


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
        "loop": configYml.get("loop", {}),
    }


load_config()

# Validate target notification
if config["target_notification"] not in VALID_TARGETS:
    print(f"⚠️ Invalid targetNotification: '{config['target_notification']}'")
    print(f"✅ Available options: {', '.join(VALID_TARGETS)}")
    exit()

# Flask app
app = Flask(__name__)


def rotating_speaker():
    local_engine = pyttsx3.init()
    matched = False
    for voice in local_engine.getProperty("voices"):
        if config["voice_name"] in voice.name.lower():
            local_engine.setProperty("voice", voice.id)
            matched = True
            break
    if not matched:
        print("⚠️ Voice not found, using default voice.")

    idx = 0
    while True:
        with loop_lock:
            if not loop_messages:
                time.sleep(1)
                continue

            item = loop_messages[idx % len(loop_messages)]
            message = item["message"]
            max_count = item["max"]
            interval = item["interval"]
            count = item["count"]

        print(f"🔊 Speaking: {message} ({count + 1}/{max_count if max_count else '∞'})")
        try:
            local_engine.say(message)
            local_engine.runAndWait()
        except Exception as e:
            print(f"❌ Error while speaking: {e}")

        time.sleep(interval)

        with loop_lock:
            item["count"] += 1
            if max_count != 0 and item["count"] >= max_count:
                print(f"✅ Finished: {message}")
                loop_messages.remove(item)
            else:
                idx += 1


# Start speaker thread
threading.Thread(target=rotating_speaker, daemon=True).start()


@app.route(config["server_path"], methods=["POST"])
def notify():
    data = request.json
    print(data)
    alerts = data.get("alerts", [])
    if not alerts:
        return "", 204

    for alert in alerts:


        labels = alert.get("labels", {})
        status = alert.get("status", "").lower()
        alert_description = alert.get("annotations", {}).get("description", "")
        alert_summary = alert.get("annotations", {}).get("summary", "")
        alert_name = labels.get("alertname", "tidak diketahui")
        alert_folder = labels.get("grafana_folder", "tidak diketahui")
        ignored_alerts = config["messages"].get("ignore", [])
        
        if alert_name in ignored_alerts:
            print(f"Ignoring {alert_name} from {alert_folder}..")
            continue
        # Format message
        template = config["messages"].get(status) or config["messages"].get("default", "{alert_name} - {status}")
        status_friendly = config["messages"].get("status", {}).get(status, status)

        message = template.format(
            alert_name=alert_name,
            status=status_friendly,
            alert_folder=alert_folder,
            alert_description=alert_description,
            alert_summary=alert_summary,
        )

        # Get loop settings
        loop_data = config["loop"].get(status, config["loop"].get("default", {}))
        max_loops = loop_data.get("max", 1)
        interval = loop_data.get("interval", 5)

        with loop_lock:
            exists = any(msg["message"] == message for msg in loop_messages)

            if status == "resolved":
                loop_messages[:] = [m for m in loop_messages if m["message"] != message]
                print(f"➖ Removed from loop_messages: {message}")
            elif not exists:
                loop_messages.append({
                    "message": message,
                    "max": max_loops,
                    "interval": interval,
                    "count": 0,
                })
                print(f"➕ Added to loop_messages: {message} (max: {max_loops}, interval: {interval}s)")
            else:
                print(f"ℹ️ Already in loop_messages, skipping: {message}")

    return "", 204


if __name__ == "__main__":
    app.run(port=config["server_port"])
