#!/usr/bin/env python3
"""Append a macOS top-CPU sample to cpu-log.json for the GitHub Pages demo."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = ROOT / "cpu-log.json"
MAX_ENTRIES = 72  # ~2.5 hours at 2-minute intervals


def ist_now() -> str:
    ist = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(tz=ist).strftime("%Y-%m-%d %H:%M:%S %Z")


def top_cpu_process() -> tuple[int, str, float]:
    out = subprocess.check_output(
        ["ps", "-Arco", "pid=,%cpu="],
        text=True,
    ).strip()
    pid_str, cpu_str = out.splitlines()[0].split(None, 1)
    pid = int(pid_str)
    cpu = float(cpu_str.strip())
    comm = subprocess.check_output(
        ["ps", "-p", str(pid), "-o", "comm="],
        text=True,
    ).strip()
    return pid, comm, cpu


def default_summary(process: str, cpu: float) -> str:
    name = process.lower()
    if cpu < 15:
        return (
            f"{process} is using modest CPU ({cpu:.1f}%). "
            "No action needed unless the machine feels sluggish."
        )
    if "cursor" in name or "code helper" in name:
        return (
            f"{process} is expected while the IDE indexes or runs agents ({cpu:.1f}%). "
            "Close unused windows or pause heavy tasks only if fans stay loud for long periods."
        )
    if "chrome" in name or "firefox" in name or "safari" in name or "discord" in name or "spotify" in name:
        return (
            f"{process} is a common foreground app spike ({cpu:.1f}%). "
            "Mute unused tabs/apps or quit the app if you are not using it; reduction is optional."
        )
    if "kernel" in name or "windowserver" in name:
        return (
            f"{process} is a system component ({cpu:.1f}%). "
            "Avoid killing it; reboot only if usage stays high with no apps open."
        )
    return (
        f"{process} is the current hotspot ({cpu:.1f}%). "
        "Inspect Activity Monitor for stuck threads; quit or update the app if usage stays high."
    )


def main() -> int:
    summary = " ".join(sys.argv[1:]).strip()
    pid, process, cpu = top_cpu_process()
    if not summary:
        summary = default_summary(process, cpu)

    if LOG_PATH.exists():
        data = json.loads(LOG_PATH.read_text(encoding="utf-8"))
    else:
        data = {"entries": []}

    data["entries"].append(
        {
            "timestamp": ist_now(),
            "pid": pid,
            "process": process,
            "cpuPercent": round(cpu, 1),
            "summary": summary,
        }
    )
    data["entries"] = data["entries"][-MAX_ENTRIES:]
    data["lastUpdated"] = ist_now()

    LOG_PATH.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"{process} ({cpu:.1f}%) pid={pid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
