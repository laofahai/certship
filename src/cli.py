import argparse
from core import run_acme_issue, get_cert_paths
from deploy.aliyun_oss import deploy

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", required=True)
    parser.add_argument("--dns-provider", default="ali")
    parser.add_argument("--platform", required=True, choices=["oss"])
    parser.add_argument("--oss-bucket")
    parser.add_argument("--oss-endpoint")
    parser.add_argument("--ecc", action="store_true")
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--force", action="store_true", help="强制续签证书")
    parser.add_argument("--ali-key", help="阿里云 AccessKeyId")
    parser.add_argument("--ali-secret", help="阿里云 AccessKeySecret")
    args = parser.parse_args()

    if args.ali_key:
        import os
        os.environ["Ali_Key"] = args.ali_key
    if args.ali_secret:
        import os
        os.environ["Ali_Secret"] = args.ali_secret

    if args.run:
        try:
            run_acme_issue(args.domain, args.dns_provider, args.ecc, args.force)
        except Exception as e:
            print(f"[警告] acme.sh 执行异常: {e}，将继续执行 deploy。")

    paths = get_cert_paths(args.domain, args.ecc)

    from core import cert_is_expired
    if args.platform == "oss":
        assert args.oss_bucket and args.oss_endpoint
        # 判断证书是否过期，未过期则直接上传
        if not cert_is_expired(paths["fullchain"]):
            print("[提示] 证书未过期，直接上传到 OSS。")
            deploy(args.domain, args.oss_bucket, args.oss_endpoint, paths["fullchain"], paths["key"])
        else:
            print("[提示] 证书已过期或不存在，建议先签发新证书。")

if __name__ == "__main__":
    main()