
# from xdsl.test import main, test3, test_redis, test_nginx_err


def test_owasp():
    from xowasp.parse import get_all_ruletxt
    rules = get_all_ruletxt()
    print(rules)
    print(len(rules))
    print(rules[0].keys())
    for x in rules:
        print(x['rule_id'])


def test2():
    from xowasp.parse import get_all_rule_extracts
    results = get_all_rule_extracts()
    for x in results:
        print(x["tags"])
        print(x["rule_txt"])
        print("-==============")


def push_rules_to_es():
    from xowasp.parse import rules_to_es
    rules_to_es()


if __name__ == '__main__':
    push_rules_to_es()


