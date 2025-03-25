import json
import random 

mock_denial_snyk_scan_response = {
    "findings":
        {
            "critical_findings": {
                "count": 5,
                "types_findings": ["CVE-Random","CVE-Random2","CVE-2021-1234", "CVE-2021-1235"]
                },
            "high_findings": {
                "count": 1,
                "types_findings": ["CVE-2021-1236"]
                },
            "medium_findings": {
                "count": 0,
                "types_findings": []
                },
            }
        }

mock_approved_snyk_scan_response = {
    "findings":
        {
            "critical_findings": {
                "count": 0,
                "types_findings": []
                },
            "high_findings": {
                "count": 0,
                "types_findings": []
                },
            "medium_findings": {
                "count": 3,
                "types_findings": ["CVE-2021-1237", "CVE-2021-1238", "CVE-2021-1239"]
                },
            }
        }


responses = [ mock_denial_snyk_scan_response, mock_approved_snyk_scan_response ]
random_integer = random.randint(0,1)
result = json.dumps(responses[random_integer])
print(result)
