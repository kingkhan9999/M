import re
import requests
import json
import socket
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# List of Google Drive file links
urls = [
    "https://drive.google.com/file/d/177tniYDInRaE4XDvUvxx7TDG8n7sYdAv/view?usp=drivesdk",
    "https://drive.google.com/file/d/1xZpzgGLTCfxQ909BkZv7vwjlhujBJBPs/view?usp=drivesdk",
    "https://drive.google.com/file/d/1dg4n3Ust_VWf4iAWFfIUH8-FCXHLlKkZ/view?usp=drivesdk",
    "https://drive.google.com/file/d/1kwwP0Z_TgbYJ76aTA_W-Bgy5gvWxoB5v/view?usp=drivesdk"
]

files_data = {}

def get_local_ip():
    """Detect the VPS local IP for network access."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))  # doesn’t have to be reachable
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def load_files():
    """Load all Google Drive files once at startup."""
    global files_data
    files_data = {}
    print("📥 Loading all files...")
    for url in urls:
        try:
            file_id = url.split("/d/")[1].split("/")[0]
            download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
            response = requests.get(download_url)
            response.raise_for_status()
            files_data[file_id] = response.text
            print(f"✅ Loaded: {url}")
        except Exception as e:
            print(f"⚠️ Error loading {url} - {e}")
    print("=== All files loaded successfully ===\n")

# Load files once at startup
load_files()

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("value", "").strip()
    if not query:
        return jsonify({"error": "Missing query parameter ?value=keyword"}), 400

    # Search through loaded files
    for file_id, text in files_data.items():
        # Find all JSON-like objects
        matches = re.findall(r'\{.*?\}', text, re.DOTALL)
        for m in matches:
            try:
                fixed = m.replace("'", '"')
                fixed = re.sub(r",\s*}", "}", fixed)
                fixed = re.sub(r",\s*]", "]", fixed)
                data = json.loads(fixed)

                # Check if query exists in any value
                if any(query in str(v) for v in data.values()):
                    return jsonify(data)
            except Exception:
                continue

    return jsonify({"error": "Not found"}), 404

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "files_loaded": len(files_data)})

if __name__ == "__main__":
    host = "0.0.0.0"  # allows external access
    port = int(os.environ.get("PORT", 5000))  # Render provides $PORT
    local_ip = get_local_ip()

    print(f"\n🚀 Server running at:")
    print(f"   Local:   http://localhost:{port}")
    print(f"   Network: http://{local_ip}:{port}")

    print(f"\n🔍 Example search links:")
    print(f"   http://{local_ip}:{port}/search?value=9333688388")
    print(f"   http://{local_ip}:{port}/search?value=user1")
    print(f"   http://{local_ip}:{port}/search?value=tech_guy")

    print(f"\n🩺 Health check: http://{local_ip}:{port}/health")
    print("\n🛑 Press CTRL+C to stop\n")

    # Disable debug for production
    app.run(debug=False, host=host, port=port)
