import os
from pathlib import Path
import subprocess
import tempfile

def deploy(domain: str, bucket: str, endpoint: str, cert_file, key_file):
    cert_path = Path(cert_file)
    key_path = Path(key_file)
    cert_content = cert_path.read_text()
    key_content = key_path.read_text()

    # 生成本地 XML 配置文件
    xml_content = f'''<?xml version="1.0" encoding="UTF-8"?>\n<BucketCnameConfiguration>\n  <Cname>\n    <Domain>{domain}</Domain>\n    <CertificateConfiguration>\n      <Certificate>\n{cert_content}\n      </Certificate>\n      <PrivateKey>\n{key_content}\n      </PrivateKey>\n      <Force>true</Force>\n    </CertificateConfiguration>\n  </Cname>\n</BucketCnameConfiguration>'''
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=".xml") as xml_file:
        xml_file.write(xml_content)
        xml_file_path = xml_file.name

    # 调用 ossutil 执行证书绑定
    ossutil_path = "ossutil64"  # 可根据实际情况调整
    oss_url = f"oss://{bucket}"
    cmd = f'{ossutil_path} bucket-cname --method put --item certificate {oss_url} {xml_file_path}'
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"[成功] 已为 {bucket} 的自定义域名 {domain} 绑定证书。")
    except Exception as e:
        print(f"[自动绑定] 证书绑定 OSS 失败: {e}")
    finally:
        os.remove(xml_file_path)
