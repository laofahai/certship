import os
import subprocess
from pathlib import Path
import datetime
from cryptography import x509
from cryptography.hazmat.backends import default_backend

def run_acme_issue(domain: str, dns_provider: str, ecc: bool = False, force: bool = False):
    args = ["~/.acme.sh/acme.sh", "--issue", f"--dns", f"dns_{dns_provider}", "-d", domain, "--debug"]
    if ecc:
        args += ["--keylength", "ec-256", "--ecc"]
    if force:
        args.append("--force")
    subprocess.run(" ".join(args), shell=True, check=True)

def get_cert_paths(domain: str, ecc: bool = False):
    suffix = "_ecc" if ecc else ""
    base = Path.home() / f".acme.sh/{domain}{suffix}"
    return {
        "fullchain": base / "fullchain.cer",
        "key": base / f"{domain}.key"
    }

def cert_is_expired(cert_path: Path) -> bool:
    try:
        cert_data = cert_path.read_bytes()
        cert = x509.load_pem_x509_certificate(cert_data, default_backend())
        not_after = cert.not_valid_after_utc
        now = datetime.datetime.utcnow()
        return now > not_after
    except Exception as e:
        print(f"[警告] 检查证书有效期失败: {e}")
        return True
