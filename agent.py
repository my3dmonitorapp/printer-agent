import os, time, json, requests, datetime, math, uuid, threading

# ---- Env ----
MOONRAKER    = os.getenv("MOONRAKER_URL", "http://127.0.0.1:7125").rstrip("/")
PRINTER_ID   = os.getenv("PRINTER_ID", "printer01")
WEBHOOK_BASE = os.getenv("N8N_WEBHOOK_BASE", "").rstrip("/")
TOKEN        = os.getenv("AGENT_TOKEN", "")
POLL         = int(os.getenv("POLL_SECONDS", "5"))
TZ           = os.getenv("TZ", "UTC")

# Optional per-printer filament settings
MATERIAL_NAME = os.getenv("MATERIAL_NAME", "PLA")
DIAMETER_MM   = float(os.getenv("FILAMENT_DIAMETER_MM", "1.75"))     # typical 1.75mm
DENSITY_G_CM3 = float(os.getenv("FILAMENT_DENSITY_G_CM3", "1.24"))  # PLA≈1.24; PETG≈1.27; ABS≈1.04

# ---- Derived ----
WEBHOOK_URL = f"{WEBHOOK_BASE}/{PRINTER_ID}/events"
headers = {"Content-Type": "application/json"}
if TOKEN:
    headers["X-Agent-Token"] = TOKEN

AGENT_VERSION = "0.1.0"

# ---- Helpers ----
def now_iso():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def now_local_iso():
    try:
        from zoneinfo import ZoneInfo
        return datetime.datetime.now(ZoneInfo(TZ)).replace(microsecond=0).isoformat()
    except Exception:
        return now_iso()

def mm_to_grams(length_mm: float, diameter_mm: float = DIAMETER_MM, density_g_cm3: float = DENSITY_G_CM3) -> float:
    r = diameter_mm / 2.0
    vol_mm3 = math.pi * (r * r) * length_mm
    grams = density_g_cm3 * (vol_mm3 / 1000.0)  # mm³ -> cm³
    return round(grams, 1)

def query_print_stats():
    url = f"{MOONRAKER}/printer/objects/query?print_stats&display_status&virtual_sdcard"
    r = requests.get(url, timeout=3)
    r.raise_for_status()
    return r.json().get("result", {}).get("status", {})

def new_event_id():
    return f"{PRINTER_ID}-{int(time.time()*1000)}-{uuid.uuid4().hex[:8]}"

def post_event(event, payload=None):
    data = {"event": event, "printer_id": PRINTER_ID, "timestamp": now_iso(), "event_id": new_event_id()}
    if payload:
        data.update(payload)
    rr = requests.post(WEBHOOK_URL, headers=headers, data=json.dumps(data), timeout=5)
    rr.raise_for_status()
    print(f"POST {event} -> {rr.status_code}")

def heartbeat_loop(period_s=600):
    while True:
        try:
            post_event("heartbeat", {
                "version": AGENT_VERSION,
                "material": MATERIAL_NAME,
                "tz": TZ,
            })
        except Exception as e:
            print(f"heartbeat error: {e}")
        time.sleep(period_s)

# ---- Main loop ----
def main():
    print(f"Agent starting for {PRINTER_ID} -> {WEBHOOK_URL}")
    # heartbeat in background
    threading.Thread(target=heartbeat_loop, args=(600,), daemon=True).start()

    last_state = None
    last_filename = None

    while True:
        try:
            s = query_print_stats()
            ps = s.get("print_stats", {})
            ds = s.get("display_status", {})

            state = ps.get("state")
            filename = (ps.get("filename") or "") or (ds.get("filename") or "")

            # idle -> printing
            if last_state != "printing" and state == "printing":
                post_event("print_started", {
                    "filename": filename or "",
                    "material": MATERIAL_NAME,
                    "started_at": now_local_iso(),   # local time (TZ)
                })

            # printing -> finished/cancelled/error/ready/standby
            if last_state == "printing" and state in ("complete","cancelled","error","standby","ready"):
                length_mm    = float(ps.get("filament_used") or 0.0)   # Moonraker in mm
                filament_g   = mm_to_grams(length_mm) if length_mm > 0 else None
                dur_sec      = float(ps.get("print_duration") or ps.get("total_duration") or 0.0)
                duration_min = round(dur_sec/60.0, 1) if dur_sec else None

                post_event("print_finished", {
                    "filename": filename or last_filename or "",
                    "status": state,
                    "finished_at": now_local_iso(),
                    "duration_min": duration_min,
                    "filament_g": filament_g,
                    "material": MATERIAL_NAME,
                })

            last_state = state
            if filename:
                last_filename = filename
        except Exception as e:
            print(f"poll error: {e}")
        time.sleep(POLL)

if __name__ == "__main__":
    main()

