import os
import sys
import yaml

# Determine paths
baseline_config_path = "/app/config.yaml"
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
