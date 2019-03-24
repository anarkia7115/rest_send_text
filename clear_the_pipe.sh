#!bin/bash

host="localhost"
port="5000"
for i in {1..100}
do
    curl -X POST "http://${host}:${port}/annotate/text" \
    --data '{"text": "The phosphorylation of Hdm2 by MK2 promotes the ubiquitination of p53."}'
done