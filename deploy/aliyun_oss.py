import tempfile
from pathlib import Path
import subprocess

def deploy(domain: str, bucket: str, endpoint: str, cert_file: Path, key_file: Path, ossutil_path: str = "ossutil64"):
    xml = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=".xml")
    xml.write(f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<BucketCnameConfiguration>
  <Cname>
    <Domain>{domain}</Domain>
    <CertificateConfiguration>
      <Force>true</Force>
      <Certificate>
{cert_file.read_text()}
      </Certificate>
      <PrivateKey>
{key_file.read_text()}
      </PrivateKey>
    </CertificateConfiguration>
  </Cname>
</BucketCnameConfiguration>
""")
    xml.close()
    subprocess.run([
        ossutil_path, "bucket-cname", "--method", "put", "--item", "certificate",
        f"oss://{bucket}", xml.name, "-e", endpoint
    ], check=True)
    print(f"✅ {domain} cert uploaded to OSS {bucket}")