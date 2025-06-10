# certship

一个使用 acme.sh 自动申请 Let's Encrypt 证书，并部署到云平台（如阿里云 OSS）的 Python 工具。

## 安装依赖
```bash
poetry install
```

## 示例
```bash
python -m certship.cli \
  --domain static.example.com \
  --dns-provider ali \
  --platform oss \
  --oss-bucket mybucket \
  --oss-endpoint oss-cn-hangzhou.aliyuncs.com \
  --run
```

## 支持计划
- [x] 阿里云 OSS
- [ ] 腾讯云 COS
- [ ] 本地 Nginx
- [ ] 七牛云

---

欢迎 PR！
