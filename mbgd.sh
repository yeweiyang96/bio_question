#!/bin/bash

folder_path="data/mbgd_2018-01_proteinseq"
db_name="MBGD"

for file_path in "$folder_path"/*; do
if [ -f "$file_path" ]; then
file_name=$(basename "$file_path")
python3 api.py -db "$db_name" -n "$file_name"
fi
done