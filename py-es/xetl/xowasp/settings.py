import sys
import os


winRuleDir = "C:\\Users\\admin\Downloads\\owasp-modsecurity-crs-3.2.0\\owasp-modsecurity-crs-3.2.0"
LocalBasePath = winRuleDir if sys.platform == "win32" else "/opt/owasp-modsecurity-crs"
RuleDir = os.path.join(LocalBasePath, *["rules", ])


