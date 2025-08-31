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
    "https://drive.google.com/file/d/1kwwP0Z_TgbYJ76aTA_W-Bgy5gvWxoB5v/view?usp=drivesdk",
    "https://drive.google.com/file/d/1LO9d12BtWsCWZ5M4qTir4ICprMoM03z5/view?usp=drivesdk",
"https://drive.google.com/file/d/1OObBOuD5PxKyZTFJWAm3IiJYIBFZTSDU/view?usp=drivesdk",
"https://drive.google.com/file/d/1Qiztwvqw5iUb5-PMYlgdIv1UpzqncJIK/view?usp=drivesdk",
"https://drive.google.com/file/d/1r_gemsB1r5PsRlepWijylN4Vb6CeKowR/view?usp=drivesdk",
"https://drive.google.com/file/d/114O57wNe12UdrQaIbwztpKzoCz8Reosc/view?usp=drivesdk",
"https://drive.google.com/file/d/1JrXV_N07aDlSFzWCZ75JmamXJDRaWMjU/view?usp=drivesdk",
"https://drive.google.com/file/d/1K51vYFKquOYUcsmNgzt0ACLgTY7Q5Idb/view?usp=drivesdk",
"https://drive.google.com/file/d/1ioVdeger2uE3KdkZG5Tdljj-MHsxv3pR/view?usp=drivesdk",
"https://drive.google.com/file/d/1OzRH-WoyuTl4gsvuN6I83YTciXcFfmPv/view?usp=drivesdk",
"https://drive.google.com/file/d/1_645YAaDV977y8CS0gINEoRwUtFDhGFi/view?usp=drivesdk",
"https://drive.google.com/file/d/1cUp64NGgtAVKA5N3CbXji8ibB5UWoccb/view?usp=drivesdk",
"https://drive.google.com/file/d/1_P89nOIQFDE9-VwXLFY87CotdiKRvSjs/view?usp=drivesdk",
"https://drive.google.com/file/d/1fd7P8e101F_OdJ-bBJ65XK34oPGpD-ia/view?usp=drivesdk",
"https://drive.google.com/file/d/1frKgnfHX_yzPW9_6oCsVKzgPijs60f06/view?usp=drivesdk",
"https://drive.google.com/file/d/1s9na4zdBidXNdD7cF24WlRZ9WeCWq33n/view?usp=drivesdk",
"https://drive.google.com/file/d/1F4L5Ww4zbO7Ci7n1cT8LdYfrrEJsSsrY/view?usp=drivesdk",
"https://drive.google.com/file/d/1byOu1KBxYNBGguRGjZ-tl4Q3jhcGEjup/view?usp=drivesdk",
"https://drive.google.com/file/d/1Jk_icNWgXX_ARi4b_Rz6SH9T06hZPmo7/view?usp=drivesdk",
"https://drive.google.com/file/d/1LoM1YXYTGQbMPQPmWDhDXeQwOZby3q-n/view?usp=drivesdk",
"https://drive.google.com/file/d/1qcevmFcqWKdw5AWgRznocsXMmoPPT2xX/view?usp=drivesdk"
"https://drive.google.com/file/d/1tiLA3HYvMd5XkWPgrCCOqNt8ZBXyZYRD/view?usp=drivesdk",
"https://drive.google.com/file/d/19v2mdYsmN56_x6XH_AMHhkamyHxPRGhj/view?usp=drivesdk",
"https://drive.google.com/file/d/1tgYISds7km_k6dGlbhHHXatjob3SCRGo/view?usp=drivesdk",
"https://drive.google.com/file/d/1k7iqhOHL6uCJb6OfZZbtixAqhkOsiGzM/view?usp=drivesdk",
"https://drive.google.com/file/d/1yHgD-CkzMjrVtCG_IFIAtWd46m4A5R3b/view?usp=drivesdk",
"https://drive.google.com/file/d/1tgojAexI1WuHyKHxCzYXy8nTd9HjfZat/view?usp=drivesdk",
"https://drive.google.com/file/d/1JA2ZBVYKqVJqP21FmtlO5T0QKjZ_Dt-k/view?usp=drivesdk",
"https://drive.google.com/file/d/1NfkoSgCMB8Yt8Wgjur9KvXuPb4e6lIjp/view?usp=drivesdk",
"https://drive.google.com/file/d/1JouQDq7zADSs8pc6d9WPjQOkFMgbpriJ/view?usp=drivesdk",
"https://drive.google.com/file/d/1V0gz4AWfELqXkW27BhxEFiHUj8VJj6jQ/view?usp=drivesdk",
"https://drive.google.com/file/d/1M4f3x_63TUxePxdvwWe0nflhAsMpLZ9J/view?usp=drivesdk",
"https://drive.google.com/file/d/1qVCYiaqOICsfN-zhDwsBct1LtwLh47zG/view?usp=drivesdk",
"https://drive.google.com/file/d/1Ad62Odma1ssy1kRbmS8piTQE1ok8pyx0/view?usp=drivesdk",
"https://drive.google.com/file/d/1Jq2REltR7TL0g74j1WxfWJaVL4rJ2_oC/view?usp=drivesdk",
"https://drive.google.com/file/d/1Qq_bAM8UUwdEtKC3hHC3qReOkKJueQWh/view?usp=drivesdk",
"https://drive.google.com/file/d/1BVzTs3E-9yJSQNHUM0LoE0qX5w8qLN2U/view?usp=drivesdk",
"https://drive.google.com/file/d/1EWjLWef6_ohs0vrJLrkSJghwptw32OeW/view?usp=drivesdk",
"https://drive.google.com/file/d/1blBMf9NWT_p0FOfP9MtCajhnR3-xch31/view?usp=drivesdk"
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
