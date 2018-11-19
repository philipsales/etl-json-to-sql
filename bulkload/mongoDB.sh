#!/bin/bash

database_name="ycsb"
collection_name="memory_used"

src_dir="/Users/ghost/src/github/jupyterlab/clean"

input_path="$src_dir/output/fhir-json/100/Condition"
input_filename="1.Condition.json"

input_dir="$input_path/$input_filename"

echo --db $database_name --collection $collection_name --type json --file $input_dir --jsonArray

for filename in $input_path/*.json; do
    echo $filename
    mongoimport --db $database_name --collection $collection_name --type json --file $filename 
done