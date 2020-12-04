# submit from the command line
BASE_URL=https://xray.cloud.xpand-it.com/api/v2
PROJECT=CALC
TESTPLAN=""
BROWSER=""
REPORT_FILE=$(ls target/graphwalker-reports/TEST-GraphWalker-*.xml | sort | tail -n 1)

token=$(curl -H "Content-Type: application/json" -X POST --data @"cloud_auth.json" "$BASE_URL/authenticate"| tr -d '"')
curl -H "Content-Type: application/xml" -X POST -H "Authorization: Bearer $token"  --data @"$REPORT_FILE" "$BASE_URL/import/execution/junit?projectKey=$PROJECT&testPlanKey=$TESTPLAN&testEnvironments=$BROWSER"


