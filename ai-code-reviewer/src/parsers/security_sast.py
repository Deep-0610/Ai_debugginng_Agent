import re
from typing import List, Dict, Any

SECURITY_RULES = [
    {
        "id": "SEC-001",
        "name": "Hardcoded API Key / Secret",
        "pattern": r"(?i)(api_key|secret|password|token)\s*=\s*['\"][A-Za-z0-9/\+=]{16,}['\"]",
        "severity": "CRITICAL",
        "cvss": 9.1,
    },
    {
        "id": "SEC-002",
        "name": "SQL Injection Vulnerability",
        "pattern": r"(?i)(select|insert|update|delete).*?\+.*?\$|\bexecute\s*\(\s*['\"].*?%s",
        "severity": "HIGH",
        "cvss": 8.5,
    },
    {
        "id": "SEC-003",
        "name": "Unsafe Execution (Command Injection)",
        "pattern": r"\b(eval|exec|os\.system|subprocess\.Popen\(.*?shell\s*=\s*True)\b",
        "severity": "HIGH",
        "cvss": 8.1,
    },
]


def run_sast_scan(code: str, language: str) -> List[Dict[str, Any]]:
    findings = []
    lines = code.splitlines()

    for idx, line in enumerate(lines, start=1):
        for rule in SECURITY_RULES:
            if re.search(rule["pattern"], line):
                findings.append(
                    {
                        "rule_id": rule["id"],
                        "line": idx,
                        "issue": rule["name"],
                        "severity": rule["severity"],
                        "cvss_score": rule["cvss"],
                        "code_snippet": line.strip(),
                    }
                )
    return findings
