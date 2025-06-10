import argparse
from certship.core import run_acme_issue, get_cert_paths
from certship.deploy.aliyun_oss import deploy

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", required=True)
    parser.add_argument("--dns-provider", default="ali")
    parser.add_argument("--platform", required=True, choices=["oss"])
    parser.add_argument("--oss-bucket")
    parser.add_argument("--oss-endpoint")
    parser.add_argument("--ecc", action="store_true")
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()

    if args.run:
        run_acme_issue(args.domain, args.dns_provider, args.ecc)

    paths = get_cert_paths(args.domain, args.ecc)

    if args.platform == "oss":
        assert args.oss_bucket and args.oss_endpoint
        deploy(args.domain, args.oss_bucket, args.oss_endpoint, paths["fullchain"], paths["key"])

if __name__ == "__main__":
    main()