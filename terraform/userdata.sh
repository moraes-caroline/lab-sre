#!/bin/bash
set -euo pipefail

# Idempotent package installation and Docker setup
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y --no-install-recommends ca-certificates curl gnupg lsb-release
apt-get install -y --no-install-recommends docker.io git

systemctl enable --now docker || true

# Install docker-compose plugin if not present (use distro package or plugin)
if ! command -v docker-compose >/dev/null 2>&1; then
	if apt-cache policy docker-compose | grep -q docker-compose; then
		apt-get install -y --no-install-recommends docker-compose
	else
		# fallback to docker's compose plugin
		mkdir -p /usr/local/lib/docker/cli-plugins || true
	fi
fi

# Install CloudWatch agent (idempotent)
CW_DEB="amazon-cloudwatch-agent.deb"
if [ ! -f "$CW_DEB" ]; then
	wget -q https://amazoncloudwatch-agent.s3.amazonaws.com/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb -O "$CW_DEB"
fi
dpkg -i "$CW_DEB" || apt-get install -f -y
rm -f "$CW_DEB"

echo "userdata: finished" >&2