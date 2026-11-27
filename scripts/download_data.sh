#!/usr/bin/env bash
# Download KuaiRand-Pure and the Pure rows of the supplementary category file into data/raw/.
set -euo pipefail
mkdir -p data/raw && cd data/raw

curl -L -o KuaiRand-Pure.tar.gz https://zenodo.org/records/10439422/files/KuaiRand-Pure.tar.gz
echo "0820331067a3784d9691136f772b35a7  KuaiRand-Pure.tar.gz" | md5sum -c -
tar -xzf KuaiRand-Pure.tar.gz

# The category file is 3.7 GB, but Pure videos are its first 7,583 rows: keep the header + those.
curl -sL https://zenodo.org/records/18159199/files/kuairand_video_categories.csv \
  | head -n 7584 > kuairand_video_categories_pure.csv || true   # head closes the pipe early
test "$(wc -l < kuairand_video_categories_pure.csv)" -eq 7584
