#!/bin/bash

REPORT_FILE=output_allinone.xml
curl -H "Content-Type: multipart/form-data" -u admin:admin -F "file=@$REPORT_FILE" http://192.168.56.102/rest/raven/1.0/import/execution/junit?projectKey=CALC
