# certship

> Author blog: https://laofahai.cool

A Python tool that uses acme.sh to automatically apply for certificates and deploy them to cloud platforms (such as Alibaba Cloud AliOSS).

## Install dependencies
```bash
poetry install
```

## Usage
You can run the tool via poetry:
```bash
poetry run certship --help
```
Or directly:
```bash
python3 -m src.cli --help
```

### Example
```bash
poetry run certship \
  --domain <your domain> \
  --dns-provider <dns provider, default ali> \
  --platform alioss \
  --oss-bucket <OSS bucket name> \
  --oss-endpoint <OSS endpoint> \
  --ali-key <Aliyun AccessKeyId> \
  --ali-secret <Aliyun AccessKeySecret> \
  [--ecc] [--run] [--force] [--debug]
```

### Arguments
- `--domain`: The domain to apply for the certificate (required)
- `--dns-provider`: DNS provider, default is ali (optional, any DNS plugin supported by acme.sh)
- `--platform`: Target platform, currently only supports alioss or tencentcos (required)
- `--oss-bucket`: Aliyun OSS bucket name (required for alioss)
- `--oss-endpoint`: OSS endpoint (required for alioss)
- `--ali-key`: Aliyun AccessKeyId (required for alioss)
- `--ali-secret`: Aliyun AccessKeySecret (required for alioss)
- `--ecc`: Use ECC certificate (optional)
- `--run`: Issue and deploy certificate (optional, if not set, only deploys existing certificate)
- `--force`: Force certificate renewal (optional)
- `--debug`: acme.sh debug mode (optional)

### Requirements
- Python 3.8+
- poetry
- acme.sh (must be installed and configured, defaults to Let's Encrypt)
- ossutil64 (must be installed and configured for AliOSS)

### Typical workflow
1. Install dependencies: `poetry install`
2. Install acme.sh and configure DNS API
3. Install and configure ossutil64 (requires yundun-cert:CreateSSLCertificate permission)
4. Run the above command to automatically issue and bind the certificate

## Supported platforms
- [x] Alibaba Cloud AliOSS
- [ ] Tencent Cloud COS
- [ ] Local Nginx
- [ ] Qiniu Cloud

---

PRs are welcome!

