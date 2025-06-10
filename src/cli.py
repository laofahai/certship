import argparse
from .core import run_acme_issue, get_cert_paths

def main():
    parser = argparse.ArgumentParser(description="certship: Automatically issue Let's Encrypt certificates with acme.sh and deploy to cloud platforms (AliOSS, Tencent COS, etc). Author: laofahai.cool")
    parser.add_argument("--domain", required=True, help="The domain to apply for the certificate (required)")
    parser.add_argument("--dns-provider", default="ali", help="DNS provider, default is ali (optional, any DNS plugin supported by acme.sh)")
    parser.add_argument("--platform", required=True, choices=["alioss", "tencentcos"], help="Target platform, currently only supports alioss or tencentcos (required)")
    parser.add_argument("--oss-bucket", help="Aliyun OSS bucket name (required for alioss)")
    parser.add_argument("--oss-endpoint", help="OSS endpoint (required for alioss)")
    parser.add_argument("--ecc", action="store_true", help="Use ECC certificate (optional)")
    parser.add_argument("--run", action="store_true", help="Issue and deploy certificate (optional, if not set, only deploys existing certificate)")
    parser.add_argument("--force", action="store_true", help="Force certificate renewal (optional)")
    parser.add_argument("--ali-key", help="Aliyun AccessKeyId (required for alioss)")
    parser.add_argument("--ali-secret", help="Aliyun AccessKeySecret (required for alioss)")
    parser.add_argument("--debug", action="store_true", help="acme.sh debug mode (optional)")
    args = parser.parse_args()

    if args.ali_key:
        import os
        os.environ["Ali_Key"] = args.ali_key
    if args.ali_secret:
        import os
        os.environ["Ali_Secret"] = args.ali_secret

    if args.run:
        try:
            run_acme_issue(args.domain, args.dns_provider, args.ecc, args.force, args.debug)
        except Exception as e:
            print(f"[警告] acme.sh 执行异常: {e}，将继续执行 deploy。")

    paths = get_cert_paths(args.domain, args.ecc)

    from .core import cert_is_expired
    if args.platform == "alioss":
        from .deploy.aliyun_oss import deploy
        assert args.oss_bucket and args.oss_endpoint
        # 判断证书是否过期，未过期则直接上传
        if not cert_is_expired(paths["fullchain"]):
            print("[提示] 证书未过期，直接上传到 OSS。")
            deploy(args.domain, args.oss_bucket, args.oss_endpoint, paths["fullchain"], paths["key"])
        else:
            print("[提示] 证书已过期或不存在，建议先签发新证书。")
    elif args.platform == "tencentcos":
        from .deploy.tencent_cos import deploy
        deploy()
        exit(1)
    else:
        print(f"[错误] 暂不支持的平台: {args.platform}")
        exit(1)

if __name__ == "__main__":
    main()