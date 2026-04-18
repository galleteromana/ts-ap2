class TestCase:

    def __init__(self, test_method_name):
        self.test_method_name = test_method_name

    def run(self, result):
        result.test_started()
        self.set_up()

        try:
            test_method = getattr(self, self.test_method_name)
            test_method()
        except AssertionError:
            result.add_failure(self.test_method_name)
        except Exception:
            result.add_error(self.test_method_name)

        self.tear_down()

    def set_up(self):
        pass

    def tear_down(self):
        pass

    def assert_equal(self, first, second):
        if first != second:
            raise AssertionError(f'{first} != {second}')

    def assert_true(self, expr):
        if not expr:
            raise AssertionError(f'{expr} is not true')

    def assert_false(self, expr):
        if expr:
            raise AssertionError(f'{expr} is not false')

    def assert_in(self, member, container):
        if member not in container:
            raise AssertionError(f'{member} not found in {container}')


class TestResult:

    RUN_MSG = 'run'
    FAILURE_MSG = 'failed'
    ERROR_MSG = 'error'

    def __init__(self, suite_name=None):
        self.run_count = 0
        self.failures = []
        self.errors = []

    def test_started(self):
        self.run_count += 1

    def add_failure(self, test):
        self.failures.append(test)

    def add_error(self, test):
        self.errors.append(test)

    def summary(self):
        return f'{self.run_count} {self.RUN_MSG}, ' \
               f'{len(self.failures)} {self.FAILURE_MSG}, ' \
               f'{len(self.errors)} {self.ERROR_MSG}'


class TestSuite:

    def __init__(self):
        self.tests = []

    def add_test(self, test):
        self.tests.append(test)

    def run(self, result):
        for test in self.tests:
            test.run(result)


class TestLoader:

    TEST_METHOD_PREFIX = 'test'

    def get_test_case_names(self, test_case_class):
        methods = dir(test_case_class)
        return list(filter(lambda m: m.startswith(self.TEST_METHOD_PREFIX), methods))

    def make_suite(self, test_case_class):
        suite = TestSuite()
        for name in self.get_test_case_names(test_case_class):
            suite.add_test(test_case_class(name))
        return suite


class TestRunner:

    def __init__(self):
        self.result = TestResult()

    def run(self, test):
        test.run(self.result)
        print(self.result.summary())
        return self.result


class TestStub(TestCase):

    def test_success(self):
        assert True

    def test_failure(self):
        assert False

    def test_error(self):
        raise Exception()


class TestCaseTest(TestCase):

    def test_assert_true(self):
        self.assert_true(True)

    def test_assert_false(self):
        self.assert_false(False)

    def test_assert_equal(self):
        self.assert_equal("", "")
        self.assert_equal("foo", "foo")
        self.assert_equal([], [])
        self.assert_equal(['foo'], ['foo'])
        self.assert_equal((), ())
        self.assert_equal(('foo',), ('foo',))
        self.assert_equal({}, {})
        self.assert_equal({'foo'}, {'foo'})

    def test_assert_in(self):
        animals = {'monkey': 'banana', 'cow': 'grass', 'seal': 'fish'}

        self.assert_in('a', 'abc')
        self.assert_in('foo', ['foo'])
        self.assert_in(1, [1, 2, 3])
        self.assert_in('monkey', animals)


class TestSuiteTest(TestCase):

    def test_suite_size(self):
        suite = TestSuite()

        suite.add_test(TestStub('test_success'))
        suite.add_test(TestStub('test_failure'))
        suite.add_test(TestStub('test_error'))

        assert len(suite.tests) == 3

    def test_suite_success_run(self):
        result = TestResult()
        suite = TestSuite()

        suite.add_test(TestStub('test_success'))
        suite.run(result)

        assert result.summary() == '1 run, 0 failed, 0 error'

    def test_suite_multiple_run(self):
        result = TestResult()
        suite = TestSuite()

        suite.add_test(TestStub('test_success'))
        suite.add_test(TestStub('test_failure'))
        suite.add_test(TestStub('test_error'))

        suite.run(result)

        assert result.summary() == '3 run, 1 failed, 1 error'

#------------------------------------------------------------------------------------------------
class MyTest(TestCase):

    def test_ok(self):
        assert True

    def test_fail(self):
        assert False

    def test_error(self):
        raise Exception()


class TestLoaderTest(TestCase):

    def test_create_suite(self):
        loader = TestLoader()
        suite = loader.make_suite(TestStub)
        assert len(suite.tests) == 3

    def test_create_suite_of_suites(self):
        loader = TestLoader()
        stub_suite = loader.make_suite(TestStub)
        spy_suite = loader.make_suite(TestSpy)

        suite = TestSuite()
        suite.add_test(stub_suite)
        suite.add_test(spy_suite)

        assert len(suite.tests) == 2

    def test_get_multiple_test_case_names(self):
        loader = TestLoader()
        names = loader.get_test_case_names(TestStub)
        assert names == ['test_error', 'test_failure', 'test_success']

    def test_get_no_test_case_names(self):

        class Test(TestCase):
            def foobar(self):
                pass

        loader = TestLoader()
        names = loader.get_test_case_names(Test)
        assert names == []


loader = TestLoader()
suite = loader.make_suite(TestLoaderTest)

runner = TestRunner()
runner.run(suite)
