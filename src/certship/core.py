import os
import subprocess
from pathlib import Path

def run_acme_issue(domain: str, dns_provider: str, ecc: bool = False):
    args = ["~/.acme.sh/acme.sh", "--issue", f"--dns", f"dns_{dns_provider}", "-d", domain]
    if ecc:
        args += ["--keylength", "ec-256", "--ecc"]
    subprocess.run(" ".join(args), shell=True, check=True)

def get_cert_paths(domain: str, ecc: bool = False):
    base = Path(f"/etc/letsencrypt/{domain}")
    return {
        "fullchain": base / "fullchain.pem",
        "key": base / "privkey.pem"
    }