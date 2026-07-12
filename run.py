import os
import yaml

config_path = "/root/.hermes/config.yaml"

# Load config if it exists
if os.path.exists(config_path):
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
    except Exception as e:
        print(f"Error reading config: {e}")
        config = {}
else:
    config = {}

# Ensure model dictionary exists
if "model" not in config:
    config["model"] = {}

# Override default model if environment variable is set
model_default = os.getenv("MODEL_DEFAULT")
if model_default:
    config["model"]["default"] = model_default
    print(f"Overriding model.default to: {model_default}")

# Write updated config back
os.makedirs(os.path.dirname(config_path), exist_ok=True)
try:
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(config, f)
except Exception as e:
    print(f"Error writing config: {e}")

# Start the gateway
print("Starting Hermes Gateway...")
os.system("gateway run")
