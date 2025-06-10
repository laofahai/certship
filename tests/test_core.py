import pytest
from src.core import get_cert_paths, cert_is_expired
from pathlib import Path

def test_get_cert_paths_ecc():
    domain = "example.com"
    paths = get_cert_paths(domain, ecc=True)
    assert "fullchain" in paths
    assert "key" in paths
    assert str(paths["fullchain"]).endswith("_ecc/fullchain.cer")
    assert str(paths["key"]).endswith("_ecc/example.com.key")

def test_get_cert_paths_rsa():
    domain = "example.com"
    paths = get_cert_paths(domain, ecc=False)
    assert "fullchain" in paths
    assert "key" in paths
    assert str(paths["fullchain"]).endswith("example.com/fullchain.cer")
    assert str(paths["key"]).endswith("example.com/example.com.key")

def test_cert_is_expired_nonexistent():
    # Should return True if file does not exist
    assert cert_is_expired(Path("/tmp/nonexistent-cert-file.pem")) is True

