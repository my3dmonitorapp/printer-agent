# My3DMonitor Printer Agent

Lightweight Docker agent for Klipper/Moonraker printers. It sends printer events to My3DMonitor.

## Install

1. Clone the repository:

```bash
git clone https://github.com/my3dmonitorapp/printer-agent
cd printer-agent
```

2. Open `.env`:

```bash
nano .env
```

3. Edit only these fields:
- `PRINTER_ID`
- `AGENT_TOKEN`
- `TZ`
- Optional: `MATERIAL_NAME`, `FILAMENT_DIAMETER_MM`, `FILAMENT_DENSITY_G_CM3`

Do **not** edit anything below the `DO NOT EDIT BELOW THIS LINE` section.

4. Start the agent:

```bash
docker compose up -d --build
```

5. Verify it is running:

```bash
docker compose ps
docker compose logs -f
```

## Where to get `PRINTER_ID` and `AGENT_TOKEN`

After printer onboarding in the My3DMonitor dashboard, copy the generated `PRINTER_ID` and `AGENT_TOKEN` and paste them into `.env`.

## Troubleshooting

- Agent container not running:
  - Run `docker compose ps` and `docker compose logs -f`.
- Moonraker connection errors:
  - Confirm Moonraker is reachable at `MOONRAKER_URL` (default `http://127.0.0.1:7125`).
- No events in dashboard:
  - Check `PRINTER_ID` and `AGENT_TOKEN` in `.env`.
  - Ensure `N8N_WEBHOOK_BASE` is unchanged and still under `DO NOT EDIT BELOW THIS LINE`.
- Wrong local timestamps:
  - Set a valid IANA timezone in `TZ` (for example `Asia/Jakarta` or `Europe/Rome`).
