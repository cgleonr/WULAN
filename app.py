import os
from flask import Flask, request, jsonify, render_template, send_from_directory
import subprocess
import time # Import time for simulating delays

app = Flask(__name__)

# --- Configuration (Highly Recommended to use Environment Variables) ---
TARGET_MAC_ADDRESS = os.getenv("TARGET_MAC_ADDRESS", "XX:XX:XX:XX:XX:XX")
TARGET_IP_ADDRESS = os.getenv("TARGET_IP_ADDRESS", "192.168.1.XXX")
SSH_USERNAME = os.getenv("SSH_USERNAME", "your_desktop_username")
SSH_KEY_PATH = "/app/ssh_keys/id_rsa"

# --- Flask Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/wake', methods=['POST'])
def wake_desktop():
    if TARGET_MAC_ADDRESS == "XX:XX:XX:XX:XX:XX":
        # Simulate success for UI testing even if MAC is not set
        print("Simulating WoL success (MAC not configured).")
        return jsonify({"status": "success", "message": "Magic packet (simulated) sent!"})

    try:
        command = f"wakeonlan {TARGET_MAC_ADDRESS}"
        result = os.system(command)

        if result == 0:
            message = f"Magic packet sent successfully to {TARGET_MAC_ADDRESS}!"
            print(message)
            return jsonify({"status": "success", "message": message})
        else:
            message = f"Failed to send magic packet. Error code: {result}"
            print(message)
            return jsonify({"status": "error", "message": message}), 500
    except Exception as e:
        message = f"An unexpected error occurred: {str(e)}"
        print(message)
        return jsonify({"status": "error", "message": message}), 500

@app.route('/status')
def get_pc_status():
    # --- Local Testing Mocking ---
    # For local testing, let's just alternate status every few calls
    # or return a consistent "offline" since we can't ping
    # on your laptop to a truly off machine.
    # When deployed, remove this mocking.
    global _mock_is_online
    if '_mock_is_online' not in globals():
        _mock_is_online = False # Start as off

    # Simulate network delay
    time.sleep(0.5)

    if request.args.get('mock') == 'on':
        _mock_is_online = True
    elif request.args.get('mock') == 'off':
        _mock_is_online = False
    else:
        _mock_is_online = not _mock_is_online # Toggle for demonstration

    print(f"Simulating PC status: {'ON' if _mock_is_online else 'OFF'}")
    return jsonify({"status": "success", "is_online": _mock_is_online, "message": "Simulated status."})

    # --- Original Code (for deployment) ---
    # if TARGET_IP_ADDRESS == "192.168.1.XXX":
    #     return jsonify({"status": "error", "message": "TARGET_IP_ADDRESS is not configured."}), 500
    # try:
    #     ping_command = ["ping", "-c", "1", "-W", "1", TARGET_IP_ADDRESS]
    #     result = subprocess.run(
    #         ping_command,
    #         stdout=subprocess.DEVNULL,
    #         stderr=subprocess.DEVNULL
    #     )
    #     is_online = result.returncode == 0
    #     message = f"PC is {'online' if is_online else 'offline'}."
    #     print(message)
    #     return jsonify({"status": "success", "is_online": is_online, "message": message})
    # except Exception as e:
    #     message = f"Error checking PC status: {str(e)}"
    #     print(message)
    #     return jsonify({"status": "error", "message": message, "is_online": False}), 500


@app.route('/shutdown', methods=['POST'])
def shutdown_pc():
    # --- Local Testing Mocking ---
    # Simulate success for UI testing
    print("Simulating shutdown success (SSH not configured).")
    global _mock_is_online
    _mock_is_online = False # Simulate turning off
    return jsonify({"status": "success", "message": "Shutdown command (simulated) sent!"})

    # --- Original Code (for deployment) ---
    # if TARGET_IP_ADDRESS == "192.168.1.XXX" or SSH_USERNAME == "your_desktop_username":
    #     return jsonify({"status": "error", "message": "TARGET_IP_ADDRESS or SSH_USERNAME is not configured for shutdown."}), 500
    # if not os.path.exists(SSH_KEY_PATH):
    #     return jsonify({"status": "error", "message": "SSH private key not found."}), 500
    # shutdown_command_linux = f"sudo shutdown -h now"
    # ssh_command = [
    #     "ssh", "-i", SSH_KEY_PATH, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5",
    #     f"{SSH_USERNAME}@{TARGET_IP_ADDRESS}", shutdown_command_linux
    # ]
    # try:
    #     result = subprocess.run(ssh_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    #     if result.returncode == 0:
    #         message = f"Shutdown command sent successfully to {TARGET_IP_ADDRESS}."
    #         print(message)
    #         return jsonify({"status": "success", "message": message})
    #     else:
    #         error_msg = result.stderr.strip() if result.stderr else "Unknown SSH error."
    #         message = f"Failed to send shutdown command via SSH: {error_msg}"
    #         print(f"SSH command failed: {result.args}\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}")
    #         return jsonify({"status": "error", "message": message}), 500
    # except FileNotFoundError:
    #     message = "SSH client 'ssh' not found in container."
    #     print(message)
    #     return jsonify({"status": "error", "message": message}), 500
    # except Exception as e:
    #     message = f"An unexpected error occurred during shutdown: {str(e)}"
    #     print(message)
    #     return jsonify({"status": "error", "message": message}), 500

if __name__ == '__main__':
    # Flask development server reloads automatically on code changes
    app.run(host='0.0.0.0', port=8000, debug=True) # debug=True enables auto-reloading