#!/usr/bin/env bash
# Download "Amazon Top 50 Bestselling Books 2009-2019" from Kaggle (550 rows).
# Requires a Kaggle API token: https://www.kaggle.com/docs/api
set -euo pipefail
mkdir -p data
pip install --quiet kaggle
kaggle datasets download -d sootersaalu/amazon-top-50-bestselling-books-2009-2019 -p data --unzip
ls -lh data/
