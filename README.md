# My3DMonitor Printer Agent

A lightweight Docker agent for Klipper/Moonraker printers that sends printer events to My3DMonitor.

## Requirements

Before you start, make sure you have:

- A Linux-based printer device with **Klipper + Moonraker already running**
- **SSH access enabled** on that device
- A working **internet connection**
- **Docker** installed (we will check/install it below)

## Step 1 — Connect to the printer with SSH

SSH is a way to open a terminal on your printer device from your computer.

You need:

- Your printer device IP address (example: `192.168.1.120`)
- Your Linux username on the printer device
- Your password

Common usernames are:

- `pi`
- `biqu`
- `orangepi`

Example SSH commands:

```bash
ssh pi@192.168.1.120
ssh biqu@192.168.1.120
```

If this is your first SSH login, type `yes` and press Enter, then enter your password.

## Step 2 — Install Docker

First, check if Docker is already installed:

```bash
docker --version
```

If you see a version number, Docker is installed. Continue to Step 3.

If Docker is not installed, run:

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin
sudo usermod -aG docker $USER
```

What these commands do:

- `apt update`: refreshes package lists
- `apt install`: installs Docker and Docker Compose plugin
- `usermod -aG docker $USER`: allows your user to run Docker without `sudo`

Important: after running these commands, disconnect SSH and connect again so group changes take effect.

## Step 3 — Download the agent

```bash
git clone https://github.com/my3dmonitorapp/printer-agent
cd printer-agent
```

This downloads the project and moves you into the project folder.

## Step 4 — Edit the `.env` file

Open the config file:

```bash
nano .env
```

Edit **ONLY** these required fields:

- `PRINTER_ID`
- `AGENT_TOKEN`
- `TZ`

Optional fields you may also edit:

- `MATERIAL_NAME`
- `FILAMENT_DIAMETER_MM`
- `FILAMENT_DENSITY_G_CM3`

Use values like this example:

```env
PRINTER_ID=voron01
AGENT_TOKEN=abc123xyz
TZ=Asia/Jakarta
```

Do not edit anything below the **`DO NOT EDIT BELOW THIS LINE`** section.

In `nano`, save with `Ctrl+O`, press Enter, then exit with `Ctrl+X`.

## Step 5 — Start the agent

```bash
docker compose up -d --build
```

This builds and starts the container in the background.

The first start can take 1-2 minutes.

## Step 6 — Verify the agent is running

Check container status:

```bash
docker compose ps
```

View live logs:

```bash
docker compose logs -f
```

Success looks like:

- The `printer-agent` container is running
- Logs show startup and heartbeat messages

Press `Ctrl+C` to stop viewing logs.

## Step 7 — Confirm success in My3DMonitor dashboard

Open your My3DMonitor dashboard.

Your printer should appear and start reporting within 1-2 minutes.

## Where to get `PRINTER_ID` and `AGENT_TOKEN`

These values are provided in the My3DMonitor dashboard after you onboard/add your printer.

Copy them from the dashboard and paste them into `.env`.

## Troubleshooting

### 1) Docker not installed

If `docker --version` fails, run the install commands from Step 2, then disconnect and reconnect SSH.

### 2) Moonraker connection failed

Verify Moonraker is reachable on the printer device:

```bash
curl http://127.0.0.1:7125/printer/info
```

If this does not return JSON, Moonraker is not ready or not reachable.

### 3) Wrong `AGENT_TOKEN`

If logs show authentication/authorization errors, re-check `AGENT_TOKEN` in `.env` and paste it again from My3DMonitor dashboard.

### 4) Printer not appearing in dashboard

Check:

- `PRINTER_ID` is correct
- `AGENT_TOKEN` is correct
- Container is running (`docker compose ps`)
- Logs for errors (`docker compose logs -f`)
- You did not edit anything below `DO NOT EDIT BELOW THIS LINE`

### 5) Wrong timezone / invalid `TZ`

Use a valid IANA timezone, for example:

- `UTC`
- `Europe/Rome`
- `Asia/Jakarta`
- `America/New_York`

If `TZ` is invalid, local time values may be wrong.

## Updating the agent

To update to the latest version:

```bash
cd printer-agent
git pull
docker compose up -d --build
```

## notes: 
The agent seems sensitive to power disruptions, especially if the Pi board is powered or restarted in different times from the printer board, i rare cases we noticed double inputs on My3dmonitor dashboard. make sure the 2 boards are powered at same time, and especially after the first installation a reboot of printer is suggested. 
