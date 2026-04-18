class TestCase:

    def __init__(self, test_method_name):
        self.test_method_name = test_method_name

    def run(self):
        self.set_up() 

        test_method = getattr(self, self.test_method_name)
        test_method() 
        self.tear_down() 

    def set_up(self):
        pass

    def tear_down(self):
        pass


class TestResult:
    def __init__(self):
        self.run_count = 0
        self.failures = []
        self.errors = []

    def test_started(self):
        pass

    def add_failure(self, test):
        pass

    def add_error(self, test):
        pass

    def summary(self):
        pass


class TestSuite:
    def __init__(self):
        self.tests = []

    def add_test(self, test):
        pass

    def run(self, result):
        pass


class TestLoader:
    def get_test_case_names(self, test_case_class):
        pass

    def make_suite(self, test_case_class):
        pass


class TestRunner:
    def __init__(self):
        self.result = TestResult()

    def run(self, test):
        pass


#------------------------------------------------------------------------------------------------
from framework import TestCase


class MyTest(TestCase):

    def set_up(self):
        print("set_up")

    def tear_down(self):
        print("tear_down")

    def test_a(self):
        print("test_a")


test = MyTest("test_a")
test.run()
