#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(dirname -- "$(readlink -f -- "${BASH_SOURCE[0]}")")"
cd $SCRIPT_DIR/../


# 1. Build the project
./scripts/build.sh

# 2. Symlink the binary
sudo ln -sf $(realpath ./bin/pd-node) /usr/local/bin/pd-node

# 3. Register the systemd service
sudo cp ./config/pd-node.service /lib/systemd/system/pd-node.service

# 4. Make the videos directory
sudo mkdir -p /var/lib/pd-node/videos

echo "To start the pegion defence service run:"
echo ""
echo "    systemctl start pd-node"
echo ""


