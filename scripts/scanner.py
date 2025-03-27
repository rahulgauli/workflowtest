import json
import random 
import csv
import io


mock_snyk_scan_response_a = {
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


mock_snyk_scan_response_b = {
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


responses = [ mock_snyk_scan_response_a, mock_snyk_scan_response_b ]
random_integer = random.randint(0,1)
result = json.dumps(responses[random_integer])


def generate_github_summary(json_data):
    summary = []
    for severity, details in json_data["findings"].items():
        if details["count"] > 0:
            summary.append(f"{severity.capitalize()}: {details['count']} ({', '.join(details['types_findings'])})")
    return " | ".join(summary)


github_summary = generate_github_summary(json.loads(result))
print(github_summary)
