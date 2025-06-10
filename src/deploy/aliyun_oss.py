def deploy(domain: str, bucket: str, endpoint: str, cert_file, key_file, ossutil_path: str = "ossutil64"):
    from os import environ
    from pathlib import Path
    import subprocess
    import tempfile

    cert_path = Path(cert_file)
    key_path = Path(key_file)
    cert_content = cert_path.read_text()
    key_content = key_path.read_text()

    # 检查 ossutil64 是否已配置 accessKeyId
    ossutil_cfg_path = str(Path.home() / ".ossutilconfig")
    need_config = False
    if not Path(ossutil_cfg_path).exists():
        need_config = True
    else:
        with open(ossutil_cfg_path, "r") as f:
            cfg = f.read()
            if not ("accessKeyID" in cfg and "accessKeySecret" in cfg and "endpoint" in cfg):
                need_config = True
    if need_config:
        ali_key = environ.get("Ali_Key")
        ali_secret = environ.get("Ali_Secret")
        if not (ali_key and ali_secret and endpoint):
            raise RuntimeError("缺少 OSS 配置信息，无法自动配置 ossutil64。请手动运行 ossutil64 config。")
        print("[提示] 自动配置 ossutil64 ...")
        subprocess.run(f'{ossutil_path} config -e {endpoint} -i {ali_key} -k {ali_secret}', shell=True, check=True)

    # 生成 XML 配置（可选，部分场景用）
    xml_content = f'''<?xml version="1.0" encoding="UTF-8"?>\n<BucketCnameConfiguration>\n  <Cname>\n    <Domain>{domain}</Domain>\n    <CertificateConfiguration>\n      <Force>true</Force>\n      <Certificate>\n{cert_content}\n      </Certificate>\n      <PrivateKey>\n{key_content}\n      </PrivateKey>\n    </CertificateConfiguration>\n  </Cname>\n</BucketCnameConfiguration>'''
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=".xml") as xml_file:
        xml_file.write(xml_content)
        xml_file_path = xml_file.name

    # 不再上传证书和私钥到 OSS，直接跳过上传逻辑
    # cert_obj = f"oss://{bucket}/{domain}.fullchain.pem"
    # key_obj = f"oss://{bucket}/{domain}.privkey.pem"
    # subprocess.run(f'{ossutil_path} cp "{cert_path}" "{cert_obj}" -e {endpoint}', shell=True, check=True)
    # subprocess.run(f'{ossutil_path} cp "{key_path}" "{key_obj}" -e {endpoint}', shell=True, check=True)
    # print(f"已上传证书到: {cert_obj}")
    # print(f"已上传私钥到: {key_obj}")
    # print(f"如需配置 CNAME，可参考生成的 XML: {xml_file_path}")

    # 自动绑定证书到 OSS 自定义域名（PutBucketCname）
    try:
        import requests
        import base64
        import time
        import hmac
        import hashlib
        from urllib.parse import quote, urlencode
        ali_key = environ.get("Ali_Key")
        ali_secret = environ.get("Ali_Secret")
        if ali_key and ali_secret:
            # 构造参数
            action = "PutBucketCname"
            version = "2015-12-15"
            method = "PUT"
            now = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            # 证书和私钥内容 base64 编码
            cert_b64 = base64.b64encode(cert_content.encode()).decode()
            key_b64 = base64.b64encode(key_content.encode()).decode()
            # 构造请求体
            xml_body = f'''<?xml version="1.0" encoding="UTF-8"?>\n<BucketCnameConfiguration>\n  <Cname>\n    <Domain>{domain}</Domain>\n    <CertificateConfiguration>\n      <Force>true</Force>\n      <Certificate>{cert_b64}</Certificate>\n      <PrivateKey>{key_b64}</PrivateKey>\n    </CertificateConfiguration>\n  </Cname>\n</BucketCnameConfiguration>'''
            # 构造签名串
            resource = f"/{bucket}/?cname"
            content_md5 = base64.b64encode(hashlib.md5(xml_body.encode()).digest()).decode()
            content_type = "application/xml"
            string_to_sign = f"PUT\n{content_md5}\n{content_type}\n{now}\n{resource}"
            signature = base64.b64encode(hmac.new(ali_secret.encode(), string_to_sign.encode(), hashlib.sha1).digest()).decode()
            headers = {
                "Date": now,
                "Authorization": f"OSS {ali_key}:{signature}",
                "Content-MD5": content_md5,
                "Content-Type": content_type,
            }
            url = f"https://{bucket}.{endpoint}/?cname"
            resp = requests.put(url, data=xml_body.encode(), headers=headers)
            if resp.status_code == 200:
                print(f"[自动绑定] 证书已自动绑定到 OSS 域名: {domain}")
            else:
                print(f"[自动绑定] 证书绑定失败: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"[自动绑定] 证书绑定 OSS 失败: {e}")
