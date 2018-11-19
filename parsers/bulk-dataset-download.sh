#!/bin/bash

environment=$1
echo $environment

src_dir="/Users/ghost/src/github/jupyterlab/clean"

output_directory="$src_dir/data/ndjson"

test_folder="$output_directory/100"
prod_folder="$output_directory/1M"
echo $output_directory



test_patient_data="https://bulk-data.smarthealthit.org/eyJlcnIiOiIiLCJwYWdlIjoxMDAwMCwiZHVyIjoxMCwidGx0IjoxNSwibSI6MSwidHlwZSI6IlBhdGllbnQiLCJpZCI6ImZkNTE2OTE2MzI0OWIxNTQ4ZDYyNDhiYzUwOTM0NDJiNjJkZWM0NDlkMTc1ODBhMTZiMjY1MTIzZDBiNmQyM2UiLCJyZXF1ZXN0U3RhcnQiOjE1NDI1OTAwNzc2NzYsInNlY3VyZSI6ZmFsc2UsIm9mZnNldCI6MCwibGltaXQiOjEwMDAwfQ/fhir/bulkfiles/1.Patient.ndjson"

test_procedure_data="https://bulk-data.smarthealthit.org/eyJlcnIiOiIiLCJwYWdlIjoxMDAwMCwiZHVyIjoxMCwidGx0IjoxNSwibSI6MSwidHlwZSI6IlByb2NlZHVyZSIsImlkIjoiNDY4MzBkYTI5NjQ0OWU4ZjBkOTNjYjM3OWEzZTI0NDNlMWYwY2NlNTk1ZWU3ZDU3NGJjYjZiZmNmMDJmNDg2MiIsInJlcXVlc3RTdGFydCI6MTU0MjU4OTk5NjM2Nywic2VjdXJlIjpmYWxzZSwib2Zmc2V0IjowLCJsaW1pdCI6MTAwMDB9/fhir/bulkfiles/1.Procedure.ndjson"

test_condition_data="https://bulk-data.smarthealthit.org/eyJlcnIiOiIiLCJwYWdlIjoxMDAwMCwiZHVyIjoxMCwidGx0IjoxNSwibSI6MSwidHlwZSI6IkNvbmRpdGlvbiIsImlkIjoiMGM4NmJhYWJiYTBlZmYxOWYzN2E3MzE0Njk3N2RjZWU1NDAwZmJmYTE3YmY3MWQ5ZmE1M2FmM2ZjNDZmYzE4MCIsInJlcXVlc3RTdGFydCI6MTU0MjU5OTg1NjAxMCwic2VjdXJlIjpmYWxzZSwib2Zmc2V0IjowLCJsaW1pdCI6MTAwMDB9/fhir/bulkfiles/1.Condition.ndjson"

prod_patient_data='https://bulk-data.smarthealthit.org/eyJlcnIiOiIiLCJwYWdlIjoxMDAwMDAwLCJkdXIiOjEwLCJ0bHQiOjE1LCJtIjoxMDAwMCwidHlwZSI6IlBhdGllbnQiLCJpZCI6IjNmMWNmN2NjZjBhZGRkZTI1Y2JhNTlhZWQzNzY3YjJhNmZiMmQxNjU1ZDY1YzkyMDQ1M2ZjYWNmMDExNWRjZDEiLCJyZXF1ZXN0U3RhcnQiOjE1NDI1OTIzMDU4MzYsInNlY3VyZSI6ZmFsc2UsIm9mZnNldCI6MCwibGltaXQiOjEwMDAwMDB9/fhir/bulkfiles/1.Patient.ndjson'

prod_condition_data="https://bulk-data.smarthealthit.org/eyJlcnIiOiIiLCJwYWdlIjoxMDAwMDAwLCJkdXIiOjEwLCJ0bHQiOjE1LCJtIjoxMDAwMCwidHlwZSI6IkNvbmRpdGlvbiIsImlkIjoiYzY2OTk1NThlNmM4OWM4MDRkYTk4NjE5YThiYTNhNzhlMzM5OGQ4YTU1NGI1MmU4Nzg4YjUwMzRkMWYxYTQxZCIsInJlcXVlc3RTdGFydCI6MTU0MjU5MjQ0NTU5OCwic2VjdXJlIjpmYWxzZSwib2Zmc2V0IjowLCJsaW1pdCI6MTAwMDAwMH0/fhir/bulkfiles/1.Condition.ndjson"

prod_procedure_data="https://bulk-data.smarthealthit.org/eyJlcnIiOiIiLCJwYWdlIjoxMDAwMDAwLCJkdXIiOjEwLCJ0bHQiOjE1LCJtIjoxMDAwMCwidHlwZSI6IlByb2NlZHVyZSIsImlkIjoiZmMzNzY1YzEyZmE1YzU0ZTk1NDhiMWQxZDM4MzFkMzZkYjQ1YjE5ZGUzOGY3ZTJlNTUxMTk0MDhkNWYwNzM5YyIsInJlcXVlc3RTdGFydCI6MTU0MjU5MjUyMjkyNiwic2VjdXJlIjpmYWxzZSwib2Zmc2V0IjowLCJsaW1pdCI6MTAwMDAwMH0/fhir/bulkfiles/1.Procedure.ndjson"


## OPTIMIZE RESORUCE LOOP
if [ $environment == 'test' ] 
then
    folder=$test_folder
    patient_data=$test_patient_data
    procedure_data=$test_procedure_data
    condition_data=$test_condition_data
else
    folder=$prod_folder
    patient_data=$prod_patient_data
    procedure_data=$prod_procedure_data
    condition_data=$prod_condition_data
fi



cd $src_dir
echo `pwd`
echo $src_dir
echo '-----'

mkdir -p $folder/Patient
cd  $folder/Patient
wget $patient_data
#curl -O $patient_data 
wait

mkdir -p $folder/Condition
cd  $folder/Condition
wget $condition_data
#curl -O $condition 
wait

mkdir -p $folder/Procedure
cd  $folder/Procedure
wget $procedure_data
#curl -O $procedure_data 
wait

cd $src_dir