# coding:utf-8
import os

res_pratean = """
REQUEST-903.9001-DRUPAL-EXCLUSION-RULES.conf（DRUPAL应用规则补丁）
REQUEST-903.9002-WORDPRESS-EXCLUSION-RULES.conf（WORDPRESS应用规则补丁）
REQUEST-903.9003-NEXTCLOUD-EXCLUSION-RULES.conf（NEXTCLOUD应用规则补丁）
REQUEST-903.9004-DOKUWIKI-EXCLUSION-RULES.conf（DOKUWIKI应用规则补丁）
REQUEST-903.9005-CPANEL-EXCLUSION-RULES.conf（CPANEL应用规则补丁）
REQUEST-903.9006-XENFORO-EXCLUSION-RULES.conf（XENFORO应用规则补丁）
REQUEST-910-IP-REPUTATION.conf（可疑IP匹配）
REQUEST-911-METHOD-ENFORCEMENT.conf（强制方法）
REQUEST-912-DOS-PROTECTION.conf（DOS攻击）
REQUEST-913-SCANNER-DETECTION.conf（扫描器检测）
REQUEST-920-PROTOCOL-ENFORCEMENT.conf（HTTP协议规范相关规则）
REQUEST-921-PROTOCOL-ATTACK.conf（协议攻击）
- 举例：HTTP Header Injection Attack、HTTP参数污染
REQUEST-930-APPLICATION-ATTACK-LFI.conf（应用攻击-路径遍历）
REQUEST-931-APPLICATION-ATTACK-RFI.conf（远程文件包含）
REQUEST-932-APPLICATION-ATTACK-RCE.conf（远程命令执行）
REQUEST-933-APPLICATION-ATTACK-PHP.conf（PHP应用防护规则）
REQUEST-934-APPLICATION-ATTACK-NODEJS.conf（NodeJs应用防护规则）
REQUEST-941-APPLICATION-ATTACK-XSS.conf（XSS注入攻击）
REQUEST-942-APPLICATION-ATTACK-SQLI.conf（SQL注入攻击）
REQUEST-943-APPLICATION-ATTACK-SESSION-FIXATION.conf（会话固定）
REQUEST-944-APPLICATION-ATTACK-JAVA.conf（Java应用防护规则）
REQUEST-949-BLOCKING-EVALUATION.conf（引擎上下文联合评估）
RESPONSE-950-DATA-LEAKAGES.conf（信息泄露）
RESPONSE-951-DATA-LEAKAGES-SQL.conf（SQL信息泄露）
RESPONSE-952-DATA-LEAKAGES-JAVA.conf（JAVA源代码泄露）
RESPONSE-953-DATA-LEAKAGES-PHP.conf（PHP信息泄露）
RESPONSE-954-DATA-LEAKAGES-IIS.conf（IIS信息泄露）
REQUEST-905-COMMON-EXCEPTIONS.conf（常见示例）
REQUEST-901-INITIALIZATION.conf（引擎初始化）
RESPONSE-980-CORRELATION.conf（内置关联规则）
REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf.example（引擎规则解释器）
RESPONSE-959-BLOCKING-EVALUATION.conf（引擎上下文联合评估）"""

import re


def get_kv_of_rukes():
    regexp = []
    for x in res_pratean.split("\n"):
        matched=re.match("(R.*?\.conf)（(.*?)）", x)
        if matched:
            temp = {}
            temp["category"] = re.match(".*?\d+\-(.*?)\.conf", matched.group(1)).group(1)
            temp["cn_category"] = matched.group(2)
            temp["filename"] = matched.group(1)
            regexp.append(temp)
    return regexp


def add_not_added_rulecates():
    sources = [x["filename"] for x in get_kv_of_rukes()]

    from .settings import RuleDir
    for x in os.listdir(RuleDir):
        if x not in sources:
            print(x)
        else:
            print('OK=======')