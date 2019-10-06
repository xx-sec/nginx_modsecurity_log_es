# coding:utf-8

import re
import os
from .settings import RuleDir


def get_rule_txt_depend_context(line_index, lines, offset=150, ):
    """
    找到 id 行， 从上往下遍历和从下往上遍历。
    :param line_index: 行所在的
    :param lines: 所有的 lines; 整个文本
    :param offset: 上下遍历寻找的偏移量
    :return:
    """
    maxIndex = len(lines) - 1
    RileTxtStartLine, RileTxtEndLine = 0, 0
    upIndexList = [line_index - i for i in range(offset)]
    for index in upIndexList:
        # todo: secrule 在单行的情况
        if re.match("SecRule .*?", lines[index]):
            RileTxtStartLine = index
            if(RileTxtStartLine == line_index):
                return lines[line_index: line_index+1]
            break
    downIndexList = [line_index + i for i in range(offset)]
    for index in downIndexList:
        if index > maxIndex or lines[index] == "\n":
            RileTxtEndLine = index-1
            break
    return lines[RileTxtStartLine:RileTxtEndLine+1]


def get_ruleparams_by_filename(filename):
    """
    通过 filename 获取该 filename 下所有的规则文本。
    :param filename:
    :return:
    """
    rule_infos = []
    with open(os.path.join(RuleDir, filename), "r+", encoding="utf-8") as f:
        lines = f.readlines()
        f.close()
    for line_index in range(len(lines)):
        if re.match("#.*?", lines[line_index]):
            continue
        matched = re.match("\s.*?id:(\d+),.*?", lines[line_index])
        if matched:
            temp = dict(
                rule_txt="".join(get_rule_txt_depend_context(line_index, lines)),
                rule_id=matched.group(1),
                rule_belong_file=filename,
            )
            rule_infos.append(temp)
    return rule_infos


def get_all_ruletxt():
    """
    获取所有的规则信息，
    :return:
    """
    results = []
    filenames = [filename for filename in os.listdir(RuleDir) if re.match(".*?conf", filename)]
    for filename in filenames:
        results.extend(get_ruleparams_by_filename(filename))
    return results


# 例如返回状态码，严重性，规则ID，Tag, 完备性。所在文件，
def parse_ruletxt_to_dict(filename):
    datas = get_ruleparams_by_filename(filename)
    rule_majus = []
    for data in datas:
        temp = data.copy()
        rule_txt = temp["rule_txt"]
        # 告警信息, 标签, 安全等级, 阶段， 版本， 完备性， 成熟性
        msg, tags, severity, phase, rev, maturity, accuracy, ver = "", [], "", "", "0", 0, 0, 'OWASP_CRS/0.0'
        tags_matched = re.findall(".*?tag:'(.*?)',.*?", rule_txt)
        for local_txt in rule_txt.split("\n"):
            msg_matched = re.match(".*?msg:'(.*?)',.*?", local_txt)
            severity_matched = re.match(".*?severity:'(.*?)',.*?", local_txt)
            phase_matched = re.match(".*?phase:(.*?),.*?", local_txt)
            rev_matched = re.match(".*?rev:'(.*?)',.*?", local_txt)
            maturity_matched = re.match(".*?maturity:'(.*?)',.*?", local_txt)
            accuracy_matched = re.match(".*?accuracy:'(.*?)',.*?", local_txt)
            ver_matched = re.match(".*?ver:'(.*?)',.*?", local_txt)
            if msg_matched:
                msg = msg_matched.group(1).replace("%", "AcTaBle").replace("{", "ZHAXIX").replace("}", "XIXAHZ")
                matched2 = re.match("(.*?)AcTaBle.*", msg)
                if matched2:
                    msg = matched2.group(1)
            if severity_matched:
                severity = severity_matched.group(1)
            if phase_matched:
                phase = phase_matched.group(1)
            if rev_matched:
                rev = rev_matched.group(1)
            if maturity_matched:
                maturity = maturity_matched.group(1)
            if accuracy_matched:
                accuracy = accuracy_matched.group(1)
            if ver_matched:
                ver = ver_matched.group(1)

        if tags_matched:
            tags = list(tags_matched)
        params = dict(
            msg=msg,
            tags=tags,
            severity=severity,
            phase=phase,
            rev=rev,
            maturity=maturity,
            accuracy=accuracy,
            ver=ver,
            filename=filename,
        )
        # temp = dict({}, **params)
        temp = dict(temp, **params)
        rule_majus.append(temp)
    return rule_majus


def get_all_rule_extracts():
    results = []
    filenames = [filename for filename in os.listdir(RuleDir) if re.match(".*?conf", filename)]
    for filename in filenames:
        results.extend(parse_ruletxt_to_dict(filename))
    return results


def rules_to_es():
    from .models import ModsecRule, client
    from elasticsearch.helpers import bulk

    inserted = get_all_rule_extracts()
    docs = []
    for x in inserted:
        _tmp = ModsecRule(meta={'id': x["rule_id"]}, **x)
        docs.append(_tmp)
    bulk(client=client, actions=[{
        "_index": ModsecRule._index._name,
        "_type": "_doc",
        "_source": x
    } for x in docs])
    print('====初始化规则OK======')
