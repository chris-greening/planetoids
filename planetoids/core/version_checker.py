import urllib.request
import threading

GITHUB_VERSION_URL = "https://raw.githubusercontent.com/chris-greening/planetoids/refs/heads/main/planetoids/core/version.txt"

def check_for_update(current_version, callback):
    """Checks GitHub for latest version and triggers callback if newer version exists."""
    def _check():
        try:
            with urllib.request.urlopen(GITHUB_VERSION_URL, timeout=2) as response:
                latest = response.read().decode("utf-8").strip()
                if _is_newer_version(latest, current_version):
                    callback(latest)
        except Exception:
            pass  # Fail silently, especially if offline

    threading.Thread(target=_check, daemon=True).start()

def _is_newer_version(remote, local):
    """Compare semantic versions like '0.2.1' and '0.3.0'."""
    def parse(v): return [int(x) for x in v.strip().split(".")]
    return parse(remote) > parse(local)
