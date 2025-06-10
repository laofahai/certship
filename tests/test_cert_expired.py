import pytest
import tempfile
from pathlib import Path
from src.core import cert_is_expired
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.x509.oid import NameOID
import datetime
from cryptography import x509

def create_cert_file(not_valid_before: datetime.datetime, not_valid_after: datetime.datetime, tmp_path: Path):
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"CN"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Beijing"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Beijing"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Test Org"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"test.example.com"),
    ])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(not_valid_before)
        .not_valid_after(not_valid_after)
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .sign(key, hashes.SHA256())
    )
    cert_pem = cert.public_bytes(serialization.Encoding.PEM)
    cert_file = tmp_path / "test_cert.pem"
    cert_file.write_bytes(cert_pem)
    return cert_file

def test_cert_is_expired_valid(tmp_path):
    now = datetime.datetime.now(datetime.UTC)
    cert_file = create_cert_file(now - datetime.timedelta(days=1), now + datetime.timedelta(days=1), tmp_path)
    assert cert_is_expired(cert_file) is False

def test_cert_is_expired_expired(tmp_path):
    now = datetime.datetime.now(datetime.UTC)
    cert_file = create_cert_file(now - datetime.timedelta(days=2), now - datetime.timedelta(days=1), tmp_path)
    assert cert_is_expired(cert_file) is True
