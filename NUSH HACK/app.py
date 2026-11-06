import os
import json
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from supabase import create_client, Client

# Load .env from next to this file, regardless of the working directory
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

app = Flask(__name__)

# --- CONFIGURATION ---
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
LOCAL_DB_FILE = "server_database.json"

# --- INITIALIZE SUPABASE CLIENT ---
try:
    # Ensure missing or placeholder values aren't triggering invalid initialization crashes
    if not SUPABASE_URL or not SUPABASE_KEY or "your-supabase" in SUPABASE_URL:
        raise ValueError("Supabase credentials missing or still placeholders.")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("[INIT] Connected securely to Supabase Cloud Client.")
except Exception as e:
    supabase = None
    print(f"[WARNING] Supabase client offline or unconfigured ({e}). Falling back to local file DB.")

# --- LOCAL DATABASE FALLBACK CONTROLLERS ---
def save_to_local_db(text):
    with open(LOCAL_DB_FILE, "w") as f:
        json.dump({"content": text}, f)

def read_from_local_db():
    if not os.path.exists(LOCAL_DB_FILE):
        return ""
    try:
        with open(LOCAL_DB_FILE, "r") as f:
            data = json.load(f)
            return data.get("content", "")
    except Exception:
        return ""

# --- ROUTE 1: INITIAL HTML LAYOUT DELIVERY (GET) ---
@app.route('/', methods=['GET'])
def home():
    current_text = ""
    
    if supabase:
        try:
            # Query row ID 1 from your documents table
            result = supabase.table("documents").select("content").eq("id", 1).execute()
            if result.data and len(result.data) > 0:
                current_text = result.data[0].get("content", "")
            print(f"[DATABASE READ] Retrieved state from Supabase.")
        except Exception as e:
            print(f"[DATABASE ERROR] Supabase read failed, trying local fallback: {e}")
            current_text = read_from_local_db()
    else:
        current_text = read_from_local_db()
            
    # Inject workspace content directly into templates/index.html
    return render_template('index.html', initial_text=current_text)

# --- ROUTE 2: LIVE BACKGROUND SYNC ENGINE (POST) ---
@app.route('/sync', methods=['POST'])
def sync_data():
    try:
        data = request.get_json(force=True)
        text_content = data.get("text", "")
        
        print(f"[SYNC ENGINE] Processing workspace buffer update...")
        
        # Save to local server file immediately for systemic redundancy
        save_to_local_db(text_content)
        
        # Attempt to upsert state to Supabase table
        if supabase:
            try:
                supabase.table("documents").upsert({
                    "id": 1, 
                    "content": text_content, 
                    "updated_at": "now()"
                }).execute()
                print("[SUPABASE CLOUD] Workspace state safely upserted.")
            except Exception as cloud_err:
                print(f"[SUPABASE ERROR] Write failed mid-transit: {cloud_err}")
                return jsonify({"status": "partial_success", "message": "Saved to local server file only."}), 200
            
        return jsonify({"status": "success", "text": text_content}), 200
    except Exception as e:
        print(f"[FATAL SYNC CRASH] Endpoint structural failure: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# --- ROUTE 3: LATEST STATE FOR DEVICE-TO-DEVICE SYNC (GET) ---
@app.route('/state', methods=['GET'])
def get_state():
    if not supabase:
        return jsonify({"text": read_from_local_db()}), 200

    try:
        result = supabase.table("documents").select("content").eq("id", 1).execute()
        text = result.data[0].get("content", "") if result.data else ""
        return jsonify({"text": text or ""}), 200
    except Exception as e:
        # Don't fall back to the local file here: it can be older than what this
        # device is showing, and browsers would overwrite newer text with it.
        print(f"[DATABASE ERROR] Supabase state read failed: {e}")
        return jsonify({"status": "error", "message": "Cloud database unavailable."}), 503

if __name__ == '__main__':
    # Locks port 5001 to bypass AirPlay port 5000 bottlenecks
    app.run(host='127.0.0.1', port=5001, debug=True)
