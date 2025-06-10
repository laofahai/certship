import tempfile
from pathlib import Path
import subprocess

def deploy(domain: str, bucket: str, endpoint: str, cert_file, key_file, ossutil_path: str = "ossutil64"):
    cert_path = Path(cert_file)
    key_path = Path(key_file)
    cert_content = cert_path.read_text()
    key_content = key_path.read_text()

    # 生成 XML 配置（可选，部分场景用）
    xml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<BucketCnameConfiguration>
  <Cname>
    <Domain>{domain}</Domain>
    <CertificateConfiguration>
      <Force>true</Force>
      <Certificate>
{cert_content}
      </Certificate>
      <PrivateKey>
{key_content}
      </PrivateKey>
    </CertificateConfiguration>
  </Cname>
</BucketCnameConfiguration>'''
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=".xml") as xml_file:
        xml_file.write(xml_content)
        xml_file_path = xml_file.name

    # 上传证书和私钥到 OSS
    cert_obj = f"oss://{bucket}/.well-known/certs/{domain}.fullchain.pem"
    key_obj = f"oss://{bucket}/.well-known/certs/{domain}.privkey.pem"
    subprocess.run(f'{ossutil_path} cp "{cert_path}" "{cert_obj}" -e {endpoint}', shell=True, check=True)
    subprocess.run(f'{ossutil_path} cp "{key_path}" "{key_obj}" -e {endpoint}', shell=True, check=True)
    print(f"已上传证书到: {cert_obj}")
    print(f"已上传私钥到: {key_obj}")
    print(f"如需配置 CNAME，可参考生成的 XML: {xml_file_path}")
