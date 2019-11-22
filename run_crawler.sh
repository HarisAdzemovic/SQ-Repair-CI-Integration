#!/bin/bash
while IFS= read -r line; do
    ./crawler-model.py $line
done < projects_for_model_1.txt
