from test.test_loads import IntLoadTest, IntLoadWithIndexTest, LoadReferenceFromArrayTest


def test_classes():
    for test_class in [
        IntLoadTest,
        IntLoadWithIndexTest,
        LoadReferenceFromArrayTest
    ]:
        test_class().run_test()
