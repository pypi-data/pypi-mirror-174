from jsonpath import jsonpath
import pytest
import ast
import time
import os
import json
import requests
import traceback
requests.packages.urllib3.disable_warnings()


test_result = {
    "title": "",
    "desc": "",
    "tester": "",
    "project": "",
    "start_time": "",
    "end_time": "",
    "failed": 0,
    "passed": 0,
    "skipped": 0,
    "error": 0,
    "cases": [],
    "file_sub": None
}



class PytestQuery:
    def __init__(self, host=''):
        self.HOST = host

    def query(self, kwargs, check=None):
        if not kwargs['url'].startswith('http'):
            kwargs['url'] = self.HOST + kwargs['url']
        if 'files' in kwargs.keys():
            kwargs_copy = kwargs.copy()
            kwargs_copy['files'] = str(kwargs_copy['files']).replace('<', "\"<").replace('>', ">\"")
            kwargs_copy['files'] = ast.literal_eval(kwargs_copy['files'])
            info = {"请求内容": kwargs_copy}
        else:
            info = {"请求内容": kwargs}
        try:
            r = requests.request(**kwargs)
            try:
                response = r.json()
            except Exception:
                response = r.text
            # 一个完整的信息
            info.update({"响应头": dict(r.headers), "响应Cookies": r.cookies.get_dict(), "响应体": response})
            # 没有断言时的返回
            if not check:
                if r.status_code == 200:
                    return info
                else:
                    raise Exception(info)
                # return info
            # 断言验证
            else:
                if not isinstance(check, (dict, list)):
                    return {"错误信息": f"断言异常，参数必须为json类型\n{check}"}
                if isinstance(check, dict):
                    check = [check]
                for n, ass in enumerate(check):
                    if ass['type'].upper() == 'JSON':
                        if not isinstance(response, (dict, list)):
                            raise Exception({"响应体": response, "错误信息": f"响应体不是JSON类型"})
                            # return {"status": False, "响应体": response, "错误信息": f"响应体不是JSON类型"}
                        else:
                            jsonpath_results = jsonpath(response, ass.get('exp'))
                            json_result = jsonpath_results[0] if len(jsonpath_results) == 1 else jsonpath_results
                            if ass['value'] != json_result:
                                info.update({"失败详情": f"*** 断言匹配失败\n条数：{n + 1}\n匹配详情:{ass}"})
                                raise Exception(info)
                                # return info
                    elif ass['type'].upper() == 'TEXT':
                        if not isinstance(ass['value'], str):
                            ass['value'] = str(ass['value'])
                        if ass['value'] not in r.text:
                            info.update({"失败详情": f"*** 断言匹配失败\n条数：{n + 1}\n匹配详情:{ass}"})
                            raise Exception(info)
                            # return info
            info.update(dict(status=True))
            return info
        except Exception:
            info.update({"错误信息": f"{traceback.format_exc()}"})
            raise Exception(info)
            # return info


def node_handle(node, item, call):
    file_path = node.location[0].replace('.py', '')
    if test_result['file_sub']:
        file_path = '\\'.join(file_path.split('\\')[int(test_result['file_sub']):])
    class_fun_path = node.location[2].split('.')
    if len(class_fun_path) == 1:
        class_path = None
        method_path = class_fun_path[0]
    else:
        class_path = class_fun_path[-2]
        method_path = class_fun_path[-1]
    sections = node.sections[0][-1] if node.sections else None
    excinfo = None
    if call.excinfo:
        try:
            excinfo = ast.literal_eval(str(call.excinfo.value))
        except Exception:
            excinfo = {"详情": f" {call.excinfo.typename} {call.excinfo.value}"}
    doc = item.function.__doc__
    return {"model": test_result['project'] + file_path, "classed": class_path, "method": method_path, "doc": doc,
            "duration": str(node.duration)[0:4], "status": node.outcome, "sections": sections, "excinfo": excinfo}


def pytest_sessionstart(session):
    """在整个测试运行开始"""
    test_result['title'] = session.config.getoption('--title') or ''
    test_result['tester'] = session.config.getoption('--tester') or ''
    test_result['desc'] = session.config.getoption('--desc') or ''
    test_result['project'] = session.config.getoption('--project') or ''
    test_result['file_sub'] = session.config.getoption('--file_sub') or ''
    test_result['start_time'] = time.strftime("%Y-%m-%d %H:%M:%S")

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """测试中报告的运行日志输出"""
    out = yield
    report = out.get_result()
    if report.when == 'call':
        test_result[report.outcome] += 1
        info = node_handle(report, item, call)
        test_result["cases"].append(info)
    elif report.outcome == 'failed':
        report.outcome = 'error'
        test_result['error'] += 1
        info = node_handle(report, item, call)
        test_result["cases"].append(info)
    elif report.outcome == 'skipped':
        test_result[report.outcome] += 1
        info = node_handle(report, item, call)
        test_result["cases"].append(info)


def pytest_sessionfinish(session):
    """在整个测试运行完成之后调用的钩子函数,可以在此处生成测试报告"""
    test_result['end_time'] = time.strftime("%Y-%m-%d %H:%M:%S")
    report = session.config.getoption('--report')
    if report:
        report_file_name = time.strftime("%Y-%m-%d_%H%M%S") + " " + (f"{report}.html" if not report.endswith('.html') else report)
        report_path = session.config.getoption('--path') or 'reports'
        if not os.path.isdir(report_path):
            os.makedirs(report_path)
        # 读取测试报告文件
        template_path = os.path.join(os.path.dirname(__file__), './template')
        with open(f'{template_path}/index.html', 'r', encoding='utf-8')as f:
            template = f.read()
        report_template = template.replace('templateData', json.dumps(test_result))
        with open(os.path.join(report_path, report_file_name), 'w', encoding='utf-8') as f:
            f.write(report_template)


def pytest_addoption(parser):
    """添加main的可调用参数"""
    group = parser.getgroup("testreport")
    group.addoption(
        "--report",
        action="store",
        default=None,
        help="测试报告标识",
    )
    group.addoption(
        "--title",
        action="store",
        default=None,
        help="测试报告最顶部标题",
    )
    group.addoption(
        "--desc",
        action="store",
        default=None,
        help="当前测试报告的说明",
    )
    group.addoption(
        "--tester",
        action="store",
        default=None,
        help="测试人员",
    )
    group.addoption(
        "--project",
        action="store",
        default=None,
        help="项目名称",
    )
    group.addoption(
        "--path",
        action="store",
        default=None,
        help="报告保存的路径",
    )
    group.addoption(
        "--file_sub",
        action="store",
        default=None,
        help="测试模块显示的范围",
    )



@pytest.fixture(scope='session')
def Api():
    return PytestQuery()
