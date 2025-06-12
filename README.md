# Desktop Wake-on-LAN & Power Control (WoL-Server)

## Overview

This project provides a convenient way to remotely power on and shut down your desktop PC from anywhere, using a Raspberry Pi and a modern, aesthetically pleasing web interface. Built with **Python Flask** and **Docker Compose**, the system leverages **Wake-on-LAN (WoL)** for waking the PC and **SSH** for remote shutdown and status checks. The user interface, built with HTML, CSS (Tailwind CSS for a glassmorphism/gold/carbon aesthetic), and JavaScript, is designed to be responsive and intuitive on both mobile devices and laptops.

Whether you're on your home network or away, this solution allows you to manage your desktop's power state with a single tap or click.

## Features

* **Wake-on-LAN (WoL) Functionality:** Send magic packets to power on your desktop remotely.
* **Remote Shutdown:** Securely shut down your PC via SSH.
* **Real-time Status Display:** Check if your PC is online or offline (via ping).
* **Modern Web UI:** A beautiful, responsive web interface inspired by glassmorphism with gold and carbon accents, accessible from any browser.
* **Dockerized Deployment:** Easy setup and management on a Raspberry Pi using Docker Compose.
* **Client-Side UI Performance:** The aesthetic UI runs efficiently in your browser, minimizing Raspberry Pi's computational load.

## Project Structure

your-project-root/
├── app.py                      # Flask application: API endpoints and UI serving
├── docker-compose.yml          # Docker Compose configuration for deployment
├── Dockerfile                  # Instructions for building the Docker image
├── requirements.txt            # Python dependencies (Flask)
├── package.json                # Node.js project configuration (for Tailwind CSS)
├── package-lock.json           # Node.js dependency lock file
├── tailwind.config.js          # Tailwind CSS configuration and custom themes
├── postcss.config.js           # PostCSS configuration (used by Tailwind)
├── templates/                  # HTML templates for the web UI
│   └── index.html              # The main web interface
├── static/                     # Static assets for the web UI
│   ├── input.css               # Tailwind CSS input file
│   ├── output.css              # Generated Tailwind CSS output file (created during Docker build)
│   ├── style.css               # (Optional) Any custom CSS not handled by Tailwind
│   ├── script.js               # JavaScript for UI interactivity
│   └── background_texture.webp # Background image/texture for the UI
└── ssh_keys/                   # Directory to hold your SSH private key (on the Pi)
└── id_rsa                  # Your SSH private key (chmod 600)


---

## Getting Started

Follow these steps to get your WoL-Server up and running.

### Prerequisites

Before you begin, ensure you have the following:

#### On Your Desktop PC (the target)

1.  **Enable Wake-on-LAN (WoL) in BIOS/UEFI:**
    * Restart your desktop and enter its BIOS/UEFI settings (usually by pressing `Del`, `F2`, `F10`, or `F12` during boot).
    * Look for settings related to "Wake-on-LAN," "PCIe Power Management," "Deep Sleep," or "Power On by PCI-E/Ethernet." **Enable this feature.**
    * Ensure your network adapter is set to listen for "magic packets" in your operating system's network driver settings (e.g., in Windows Device Manager, Network Adapters -> Properties -> Power Management tab).
2.  **Assign a Static IP Address:** Your desktop PC needs a static local IP address (e.g., `192.168.1.10`) for the Raspberry Pi to reliably ping and SSH into it. Configure this in your router's DHCP settings or directly on your desktop's network adapter settings.
3.  **Install & Configure SSH Server:**
    * **Linux Desktop:** Install `openssh-server`.
        ```bash
        sudo apt update
        sudo apt install openssh-server
        ```
    * **Windows Desktop:** You can enable the "OpenSSH Server" optional feature in Windows 10/11 settings.
4.  **Set up SSH Key-Based Authentication:** For secure and unattended access, you'll use SSH keys.
    * Generate an SSH key pair (if you don't have one): Open a terminal (Git Bash, WSL, PowerShell) and run `ssh-keygen -t rsa -b 4096`. Press Enter for default location and no passphrase (unless you want to enter it every time, which defeats automation).
    * **Copy the Public Key** (`~/.ssh/id_rsa.pub`) to your desktop PC.
        * **Linux Desktop:** Use `ssh-copy-id <your-desktop-username>@<your-desktop-ip>` or manually append the content of `id_rsa.pub` to `~/.ssh/authorized_keys` on your desktop.
        * **Windows Desktop:** Append the content of `id_rsa.pub` to `C:\Users\<YourUsername>\.ssh\authorized_keys` (create `.ssh` and `authorized_keys` if they don't exist). Ensure correct file permissions (only owner write/read).
5.  **Configure `sudo` for Shutdown (Linux Desktop Only):** To allow the Pi to shut down your Linux desktop via SSH without a password, you need to grant `NOPASSWD` sudo access for the `shutdown` command.
    * On your desktop, open the sudoers file: `sudo visudo`
    * Add the following line, replacing `your_desktop_username` with the actual username you'll SSH as:
        ```
        your_desktop_username ALL=(ALL) NOPASSWD: /sbin/shutdown
        ```
    * Save and exit (`Ctrl+X`, `Y`, `Enter` for Nano).

#### On Your Development Machine (where you're preparing the code in VS Code)

1.  **Git:** Installed and configured.
2.  **VS Code:** With the Docker extension (optional, but helpful).
3.  **Python 3.11+:** Installed.
4.  **`pip`:** Python package installer.
5.  **Node.js & npm:** Download and install the LTS version from [nodejs.org](https://nodejs.org/). This is crucial for building the Tailwind CSS UI. Remember to restart your terminal after installation.
6.  **Docker Desktop (Optional):** If you wish to test the Docker image locally before deploying to the Pi.

#### On Your Raspberry Pi (the server)

1.  **Raspberry Pi OS:** Installed on an SD card.
2.  **SSH Enabled:** Ensure SSH is enabled on your Pi for remote access.
3.  **Docker & Docker Compose:** Install Docker and Docker Compose on your Raspberry Pi.
    ```bash
    curl -sSL [https://get.docker.com](https://get.docker.com) | sh
    sudo apt-get install -y libffi-dev libssl-dev python3 python3-pip
    sudo pip3 install docker-compose
    sudo usermod -aG docker $USER # Add your user to the docker group
    # You will need to log out and log back in for the group change to take effect.
    ```

---

### Local Development Setup (on your Dev Machine)

Follow these steps to set up the project locally for development and UI testing.

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd <your-project-root>
    ```

2.  **Create Python Virtual Environment:**
    ```bash
    python3.11 -m venv venv
    source venv/bin/activate # On Windows: venv\Scripts\activate
    ```

3.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize Node.js Project & Tailwind CSS:**
    ```bash
    npm init -y
    npm install -D tailwindcss postcss autoprefixer tailwindcss-filters
    npx tailwindcss init -p
    ```
    *This creates `package.json`, `package-lock.json`, `tailwind.config.js`, `postcss.config.js`, and the `node_modules` directory.*

5.  **Configure Tailwind CSS:**
    Open `tailwind.config.js` and ensure the `content` array points to your HTML, JS, and Python files correctly (as specified in the project structure above). This is where you'll define custom colors, shadows, and other design tokens to match your desired aesthetic.

6.  **Create Tailwind Input CSS:**
    Create `static/input.css` with the following content:
    ```css
    @tailwind base;
    @tailwind components;
    @tailwind utilities;
    ```

7.  **Create `ssh_keys` directory:**
    ```bash
    mkdir ssh_keys
    ```
    This folder will remain empty for local testing but is crucial for deployment.

8.  **Update `app.py` for Local Testing:**
    * For local UI development, the WoL, ping, and SSH commands will fail.
    * Temporarily **uncomment the "Local Testing Mocking" sections** and **comment out the "Original Code (for deployment)" sections** within the `wake_desktop`, `get_pc_status`, and `shutdown_pc` functions in `app.py`. This will allow your UI to simulate success/failure and status changes.
    * Remember to revert these changes before deploying!

9.  **Generate Tailwind CSS Output:**
    You need to run this command **every time you make changes to your HTML, JavaScript, `tailwind.config.js`, or `static/input.css`** to update `static/output.css`.
    ```bash
    npx tailwindcss -i ./static/input.css -o ./static/output.css --minify
    ```

10. **Run the Flask Development Server:**
    ```bash
    python app.py
    ```
    The server will start on `http://localhost:8000`.

11. **Test the UI:**
    Open your web browser and navigate to `http://localhost:8000`. You should see your beautifully styled UI. Interact with the buttons and observe the simulated status changes.

---

## Deployment to Raspberry Pi

Once you're satisfied with the local setup and UI, deploy it to your Raspberry Pi.

1.  **Update `app.py` for Production:**
    * **Crucially, revert the temporary changes made for local testing in `app.py`.**
    * **Uncomment the "Original Code (for deployment)" sections** and **comment out the "Local Testing Mocking" sections** within `wake_desktop`, `get_pc_status`, and `shutdown_pc`.
2.  **Configure Environment Variables in `docker-compose.yml`:**
    Open `docker-compose.yml` and **replace the placeholder values** for `TARGET_MAC_ADDRESS`, `TARGET_IP_ADDRESS`, and `SSH_USERNAME` with your desktop's actual details.
    ```yaml
    environment:
      - TARGET_MAC_ADDRESS=XX:XX:XX:XX:XX:XX  # <--- YOUR DESKTOP'S MAC
      - TARGET_IP_ADDRESS=192.168.1.XXX      # <--- YOUR DESKTOP'S STATIC IP
      - SSH_USERNAME=your_desktop_username   # <--- YOUR DESKTOP'S SSH USERNAME
    ```
3.  **Place SSH Private Key on Pi:**
    * Copy your **SSH private key file** (e.g., `id_rsa` from `~/.ssh/`) to the `ssh_keys/` directory within your project folder on the Raspberry Pi.
    * **Important:** Set correct permissions for your private key on the Pi:
        ```bash
        chmod 600 ./ssh_keys/id_rsa
        ```
        (If you put it elsewhere, adjust the path in `docker-compose.yml` and `app.py` accordingly.)
4.  **Transfer Project Files to Raspberry Pi:**
    Copy the entire `your-project-root` directory (containing `app.py`, `docker-compose.yml`, `Dockerfile`, `templates/`, `static/`, `ssh_keys/` with your key, etc.) to a suitable location on your Raspberry Pi (e.g., `/home/pi/wol-server/`).
5.  **Navigate to Project Directory on Pi:**
    ```bash
    cd /home/pi/wol-server/
    ```
6.  **Build and Run with Docker Compose:**
    This command will build the Docker image (installing Node.js and running the Tailwind build inside the container) and then start your WoL-Server.
    ```bash
    docker-compose up -d --build
    ```
    * `up`: Creates and starts containers.
    * `-d`: Runs containers in detached mode (in the background).
    * `--build`: Forces Docker Compose to rebuild the image, ensuring all changes are picked up and Tailwind CSS is re-generated.

7.  **Verify Container Status:**
    ```bash
    docker-compose ps
    ```
    You should see `wol_server_container` listed with a `Up` status.

---

## Usage

### On Your Local Network

1.  Find your Raspberry Pi's local IP address (e.g., using `ifconfig` or `ip a` on the Pi, or checking your router's connected devices).
2.  Open a web browser on your phone or laptop and navigate to:
    `http://<Raspberry_Pi_IP_Address>:8000`

### Away From Home (Remote Access)

To access your WoL-Server when you're away from home, you'll need a remote access solution. Here are some popular options:

1.  **VPN (Virtual Private Network):** Set up a VPN server on your home router or directly on your Raspberry Pi (e.g., using PiVPN or OpenVPN). When away, connect your device to your home VPN, and then access the Pi's local IP address as if you were on your home network.
2.  **Cloudflare Tunnel:** A secure, zero-trust solution that exposes your local service to the internet without opening any ports on your router. You install `cloudflared` on your Pi, and it creates an outbound connection to Cloudflare.
3.  **Tailscale:** Creates a secure mesh network between your devices, allowing them to connect directly without port forwarding. Install Tailscale on your Pi and your phone/laptop, and they'll be able to communicate securely.
4.  **ngrok:** A quick and easy way to expose a local web server to the internet for testing or temporary access.

Once your chosen remote access solution is configured, you'll use the public URL or VPN-assigned IP address to access your WoL-Server's web interface.

---

## Contributing

Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, please open an issue or submit a pull request.

---

## License

[Choose and insert your license here, e.g., MIT License]