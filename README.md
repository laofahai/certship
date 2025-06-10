# certship

> 作者博客：https://laofahai.cool

一个使用 acme.sh 自动申请证书，并自动部署到对象存储的 Python 工具。

- 证书来源：Let's Encrypt（acme.sh 仅为签发工具）

## 安装依赖
```bash
poetry install
```

## 用法
```bash
python3 -m src.cli \
  --domain <你的域名> \
  --dns-provider <dns服务商, 默认ali> \
  --platform alioss \
  --oss-bucket <OSS bucket名称> \
  --oss-endpoint <OSS endpoint> \
  --ali-key <阿里云AccessKeyId> \
  --ali-secret <阿里云AccessKeySecret> \
  [--ecc] [--run] [--force] [--debug]
```

### 参数说明
- `--domain`：要申请证书的域名（必填）
- `--dns-provider`：DNS 服务商，默认 ali（可选，acme.sh 支持的 DNS 插件，详见 acme.sh 文档）
- `--platform`：目标平台，目前仅支持 alioss（必填）
- `--oss-bucket`：阿里云 OSS 的 bucket 名称（必填）
- `--oss-endpoint`：OSS 的 endpoint（必填）
- `--ali-key`：阿里云 AccessKeyId（必填）
- `--ali-secret`：阿里云 AccessKeySecret（必填）
- `--ecc`：使用 ECC 证书（可选）
- `--run`：执行证书签发和部署（可选，不加则只部署已有证书）
- `--force`：强制续签证书（可选）
- `--debug`：acme.sh 调试模式（可选）

### 依赖环境
- Python 3.8+
- poetry
- acme.sh（需提前安装并配置好，默认签发 Let's Encrypt 证书）
- ossutil64（需提前安装并配置好）

### 典型流程
1. 安装依赖：`poetry install`
2. 安装 acme.sh 并配置好 DNS API
3. 安装并配置好 ossutil64（需有 yundun-cert:CreateSSLCertificate 权限）
4. 运行上述命令自动签发并绑定证书

## 支持计划
- [x] 阿里云 AliOSS
- [ ] 腾讯云 COS
- [ ] 本地 Nginx
- [ ] 七牛云

---

欢迎 PR！
