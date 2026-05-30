#!/usr/bin/env python3
"""
Auto-commit watcher: monitors the project directory and pushes changes to GitHub.
Usage: python3 scripts/watcher.py
       python3 scripts/watcher.py --path /custom/path --delay 5
"""

import argparse
import logging
import os
import subprocess
import threading
import time
from datetime import datetime
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

LOG_DIR = Path.home() / "antigravity_logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "watcher.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)

IGNORE = {".git", "node_modules", ".next", ".turbo", "dist", "__pycache__", ".DS_Store"}


def is_ignored(path: str) -> bool:
    return any(part in IGNORE for part in Path(path).parts)


def run(cmd: list[str], cwd: str) -> tuple[int, str]:
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    output = (result.stdout + result.stderr).strip()
    return result.returncode, output


def commit_and_push(repo_path: str) -> None:
    code, out = run(["git", "status", "--porcelain"], repo_path)
    if not out:
        log.info("No changes to commit.")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"Auto-sync: {timestamp}"

    steps = [
        (["git", "add", "-A"], "Stage"),
        (["git", "commit", "-m", msg], "Commit"),
        (["git", "push", "origin", "main"], "Push"),
    ]

    for cmd, label in steps:
        code, out = run(cmd, repo_path)
        if code != 0:
            log.error("%s failed: %s", label, out)
            # Retry once
            code, out = run(cmd, repo_path)
            if code != 0:
                log.error("%s retry failed — halting. %s", label, out)
                return
        else:
            log.info("%s: %s", label, out or "ok")

    log.info("Pushed to GitHub.")


class ChangeHandler(FileSystemEventHandler):
    def __init__(self, repo_path: str, delay: float):
        self.repo_path = repo_path
        self.delay = delay
        self._timer: threading.Timer | None = None
        self._lock = threading.Lock()

    def _schedule(self) -> None:
        with self._lock:
            if self._timer:
                self._timer.cancel()
            self._timer = threading.Timer(self.delay, commit_and_push, args=[self.repo_path])
            self._timer.start()

    def on_modified(self, event):
        if not event.is_directory and not is_ignored(event.src_path):
            log.debug("Changed: %s", event.src_path)
            self._schedule()

    def on_created(self, event):
        if not is_ignored(event.src_path):
            self._schedule()

    def on_deleted(self, event):
        if not is_ignored(event.src_path):
            self._schedule()


def main():
    parser = argparse.ArgumentParser(description="Auto-commit file watcher")
    parser.add_argument("--path", default=str(Path(__file__).parent.parent), help="Repo path to watch")
    parser.add_argument("--delay", type=float, default=3.0, help="Debounce delay in seconds (default: 3)")
    args = parser.parse_args()

    repo_path = os.path.abspath(args.path)
    log.info("Watching: %s  (debounce: %ss)", repo_path, args.delay)
    log.info("Logs: %s/watcher.log", LOG_DIR)

    handler = ChangeHandler(repo_path, args.delay)
    observer = Observer()
    observer.schedule(handler, repo_path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log.info("Stopping watcher.")
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
