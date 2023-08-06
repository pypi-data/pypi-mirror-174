from __future__ import annotations

from robot.result import TestCase as RTestResult
from robot.running import TestSuite as RTestSuite, TestCase as RTestCase, Keyword as RKeyword

from robotframework_practitest.models.practi_test.data_formatters import practi_test_duration
from robotframework_practitest.models.robot.helpers import format_kw_list


def convert(item: RTestSuite | RTestCase | RKeyword):
    return PTestSuite(item)


def get_parents_path(item: RTestSuite | RTestCase | RKeyword):
    result = []
    while item.parent:
        result.append(item.parent.name)
        item = item.parent
    result.reverse()
    return result


def extract_kw_results(results: RTestResult) -> dict:
    for kw_res in results.body:
        print(f"{kw_res}")
    return {}


def format_suite_test_description(item: PTestSuite | PTestCase):
    description = []
    if item.doc:
        description.append(f"{item.doc}")
    if item.has_setup:
        description.append("Setup:\n\t{}".format(format_kw_list([item.setup.name] + list(item.setup.args))))
    if item.has_teardown:
        teardown_kws = [item.teardown.name] + list(item.teardown.args)
        description.append("Teardown:\n\t{}".format(format_kw_list(teardown_kws)))
    return '\n'.join(description)


class PKeyword:
    def __init__(self, item: RKeyword):
        self.name = item.name
        self.tags = item.tags
        self.parent = get_parents_path(item)
        self.doc = item.doc
        self.args = item.args
        self.teardown = PKeyword(item.teardown) if item.teardown else None

    def __str__(self):
        return f"{self.name}({self.args})"

    @property
    def has_teardown(self):
        return self.teardown is not None


class PTestCase:
    def __init__(self, item: RTestCase):
        self.name = item.name
        self.tags = item.tags
        self.doc = item.doc
        self.parent = get_parents_path(item)
        self.setup = PKeyword(item.setup) if item.setup else None
        self.teardown = PKeyword(item.teardown) if item.teardown else None
        self.body = [PKeyword(k) for k in item.body]

    def __str__(self):
        return f"{self.name}({self.body})"

    @property
    def has_setup(self):
        return self.setup is not None

    @property
    def has_teardown(self):
        return self.teardown is not None

    @property
    def steps(self):
        return [{'name': k.name, 'description': k.doc} for k in self.body]


class PTestResult(PTestCase):
    def __init__(self, item: RTestResult):
        super().__init__(item)
        self.status = item.status + 'ED'
        self.starttime = item.starttime
        self.endtime = item.endtime
        self.elapsedtime = item.elapsedtime / 1000
        self.message = item.message

    @property
    def automated_execution_output(self):
        return self.message

    @property
    def duration(self):
        return practi_test_duration(self.elapsedtime)

    def steps(self, *case_steps):
        result = []
        for k in case_steps:
            k.update(**{'status': self.status})
            result.append(dict(**{"name": k.get('name'), "expected-results": self.status}))
        return result

    @property
    def exit_code(self):
        return 0 if self.status == 'PASSED' else 1


class PTestSuite:
    def __init__(self, item: RTestSuite):
        self.name = item.name
        self.doc = item.doc
        self.parent = get_parents_path(item)
        self.tests = [PTestCase(t) for t in item.tests]
        self.suites = [PTestSuite(s) for s in item.suites]
        self.setup = PKeyword(item.setup) if item.setup else None
        self.teardown = PKeyword(item.teardown) if item.teardown else None

    @property
    def tags(self) -> list:
        return []

    @property
    def has_setup(self):
        return self.setup is not None

    @property
    def has_teardown(self):
        return self.teardown is not None

    def __str__(self):
        return self.name
