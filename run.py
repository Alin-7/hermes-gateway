import os
import sys
import yaml
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# A very simple HTTP server to satisfy Render's port scan/health checks
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")

def start_health_check_server():
    port = int(os.getenv("PORT", 7860))
    print(f"Starting health check listener on port {port}...")
    try:
        server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
        server.serve_forever()
    except Exception as e:
        print(f"Health check server error: {e}")

# Run health check server in a background thread
threading.Thread(target=start_health_check_server, daemon=True).start()

# Determine paths
baseline_config_path = "/app/config.yaml"
hermes_home = os.getenv("HERMES_HOME")
if hermes_home:
    config_path = os.path.join(hermes_home, "config.yaml")
else:
    config_path = os.path.expanduser("~/.hermes/config.yaml")

print(f"Target config path: {config_path}")

# Load baseline config
config = {}
if os.path.exists(baseline_config_path):
    try:
        with open(baseline_config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
        print("Loaded baseline configuration.")
    except Exception as e:
        print(f"Error reading baseline config: {e}")

# Ensure model dictionary exists
if "model" not in config:
    config["model"] = {}

# Override default model if environment variable is set
model_default = os.getenv("MODEL_DEFAULT")
if model_default:
    config["model"]["default"] = model_default
    print(f"Overriding model.default to: {model_default}")

# Inject custom provider API keys from environment variables
bynara_api_key = os.getenv("BYNARA_API_KEY")
if bynara_api_key and "custom_providers" in config:
    for provider in config["custom_providers"]:
        if provider.get("name") == "Router.bynara.id":
            provider["api_key"] = bynara_api_key
            print("Injected BYNARA_API_KEY into Router.bynara.id provider configuration.")

tcloudbase_api_key = os.getenv("TCLOUDBASE_API_KEY")
if tcloudbase_api_key and "custom_providers" in config:
    for provider in config["custom_providers"]:
        if provider.get("name") == "tcloudbase":
            provider["api_key"] = tcloudbase_api_key
            print("Injected TCLOUDBASE_API_KEY into tcloudbase provider configuration.")

# Write updated config to user's home directory (.hermes/config.yaml)
os.makedirs(os.path.dirname(config_path), exist_ok=True)
try:
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(config, f)
    print(f"Successfully wrote configuration to {config_path}")
except Exception as e:
    print(f"Error writing config to home directory: {e}")

# Start the gateway using the python module path to avoid PATH resolution issues
cmd = f"{sys.executable} -m hermes_cli.main gateway run"
print(f"Starting Hermes Gateway via command: {cmd}")
os.system(cmd)
