import json
import random 

##user story for data schemas for these will be needed 


##user story for policy will need to be defined with this format
def policy1(scan_findings):
    if scan_findings["findings"]["critical_findings"]["count"] > 0 or scan_findings["findings"]["high_findings"]["count"] > 0:
        return "fail"
    return "pass"


def policy2(scan_findings):
    if scan_findings["findings"]["high_findings"]["count"] > 0 and scan_findings["findings"]["medium_findings"]["count"] > 0:
        return "fail"
    return "pass"


mock_policy_data = {
    "repositories": [
        {
            "name": "repo1",
            "policy": policy1
        },
        {
            "name": "repo2",
            "policy": policy2
        },
        {
            "name": "repo3",
            "policy": policy1
        }
    ]
}

##snyk scripting user story will be based off the result with this format
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

mock_snyk_scan_response_c = {
    "findings":
        {
            "critical_findings": {
                "count": 2,
                "types_findings": ["CVE-2022-0001", "CVE-2022-0002"]
                },
            "high_findings": {
                "count": 4,
                "types_findings": ["CVE-2022-0003", "CVE-2022-0004", "CVE-2022-0005", "CVE-2022-0006"]
                },
            "medium_findings": {
                "count": 1,
                "types_findings": ["CVE-2022-0007"]
                },
            }
        }

mock_snyk_scan_response_d = {
    "findings":
        {
            "critical_findings": {
                "count": 0,
                "types_findings": []
                },
            "high_findings": {
                "count": 2,
                "types_findings": ["CVE-2023-1234", "CVE-2023-1235"]
                },
            "medium_findings": {
                "count": 5,
                "types_findings": ["CVE-2023-1236", "CVE-2023-1237", "CVE-2023-1238", "CVE-2023-1239", "CVE-2023-1240"]
                },
            }
        }

mock_snyk_scan_response_e = {
    "findings":
        {
            "critical_findings": {
                "count": 3,
                "types_findings": ["CVE-2024-0001", "CVE-2024-0002", "CVE-2024-0003"]
                },
            "high_findings": {
                "count": 0,
                "types_findings": []
                },
            "medium_findings": {
                "count": 0,
                "types_findings": []
                },
            }
        }


responses = [ mock_snyk_scan_response_a, mock_snyk_scan_response_b, mock_snyk_scan_response_c, mock_snyk_scan_response_d, mock_snyk_scan_response_e]
random_integer = random.randint(0,4)
result = json.dumps(responses[random_integer])
policy_result = policy1(json.loads(result))


## messaging user story will be based off the result with this format
def generate_github_summary(json_data):
    summary = []
    for severity, details in json_data["findings"].items():
        if details["count"] > 0:
            summary.append(f"{severity.capitalize()}: {details['count']} ({', '.join(details['types_findings'])})")
    return " | ".join(summary)


github_summary = generate_github_summary(json.loads(result))
final_result = {
    "policy_result": policy_result,
    "github_summary": github_summary
}


print(final_result)
