# **My3DMonitor – Printer Agent**

This repository contains the My3DMonitor Printer Agent, a lightweight Docker-based service that connects to Klipper / Moonraker and reports printer activity (prints, usage, heartbeat) to the My3DMonitor platform.

The agent is printer-agnostic and works with any Klipper-based printer (Voron, Anycubic, etc.).



Requirements

Before installing the agent, make sure your printer host has:

&nbsp;   • Linux (Raspberry Pi OS, Armbian, etc.)

&nbsp;   • Klipper + Moonraker running and connected

&nbsp;   • Docker + Docker Compose plugin

&nbsp;   • Internet access

⚠️ Important

This agent assumes Moonraker is reachable and stable before installation.



##### 1\. Verify Klipper \& Moonraker

SSH into your printer host and run:



**systemctl is-active klipper**

**systemctl is-active moonraker**



Both must return active.

Test Moonraker API:

curl http://127.0.0.1:7125/printer/info

If you get JSON output, Moonraker is ready.



##### 2\. Install Docker (if not already installed)

**sudo apt update**

**sudo apt install -y ca-certificates curl git**

**curl -fsSL https://get.docker.com | sudo sh**

**sudo usermod -aG docker $USER**

**newgrp docker**

**sudo apt install -y docker-compose-plugin**

Verify:

**docker --version**

**docker compose version**



##### 3\. Clone the Printer Agent

**cd ~**

**git clone https://github.com/<YOUR\_GITHUB\_ORG>/printer-agent.git**

**cd printer-agent**



##### 4\. Configure the Agent

Create your local environment file:



nano .env

Required fields to edit

\# Moonraker API (usually local)

MOONRAKER\_URL=http://127.0.0.1:7125



\# Unique printer identifier

PRINTER\_ID= **" this part you need to write your printer ID "**



\# Webhook URL provided by My3DMonitor

N8N\_WEBHOOK\_BASE=https://app.my3dmonitor.com/webhook/XXXX/printers



\# Agent authentication token

AGENT\_TOKEN= **" write you long token code "**



\# Timezone (**important for daily stats, set it correctly**) 

TZ=Europe/Rome

Save and exit.

❗ Do NOT commit .env

It contains secrets and is ignored by Git.



##### 5\. Start the Agent

**docker compose up -d --build**

Check status:

**docker ps**

View logs:

**docker logs -f printer-agent**

You should see:

&nbsp;   • Agent startup

&nbsp;   • One heartbeat event

&nbsp;   • Print events when you start/finish a print



##### 6\. Test the Installation

&nbsp;   **1. Start a print from Mainsail / Fluidd**

    **2. Verify:**

        **◦ print\_started is sent once**

        **◦ print\_finished is sent once**

    **3. Confirm data appears in your My3DMonitor dashboard**

**DONE**



Updating the Agent

To update to a new version:

**cd ~/printer-agent**

**git pull**

**docker compose up -d --build**



Uninstalling the Agent

**cd ~/printer-agent**

**docker compose down**



Notes About \[mcu host]

Some Klipper configurations include:

\[mcu host]

serial: /tmp/klipper\_host\_mcu

⚠️ This is optional and advanced.

&nbsp;   • Only required if you use pin: host:gpioXX

&nbsp;   • Not required for standard printers

&nbsp;   • If enabled without proper setup, Klipper will fail to start

For most users, this section should be commented out or removed.



Troubleshooting

Moonraker 503 errors

If logs show 503 Klippy Host not connected:

&nbsp;   • Klipper is not ready

&nbsp;   • Restart Klipper and Moonraker

&nbsp;   • Fix printer connection before running the agent

Duplicate events

&nbsp;   • Ensure only one agent container is running

&nbsp;   • Reboot the printer host if Klipper was unstable earlier



License

MIT License

