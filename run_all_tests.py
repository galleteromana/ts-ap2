from framework import (
    TestLoader,
    TestSuite,
    TestRunner,
    TestCaseTest,
    TestSuiteTest,
    TestLoaderTest
)

loader = TestLoader()


test_case_suite = loader.make_suite(TestCaseTest)
test_suite_suite = loader.make_suite(TestSuiteTest)
test_loader_suite = loader.make_suite(TestLoaderTest)


suite = TestSuite()
suite.add_test(test_case_suite)
suite.add_test(test_suite_suite)
suite.add_test(test_loader_suite)


runner = TestRunner()
runner.run(suite)