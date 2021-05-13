import os,unittest

def run_test():
    '''
    运行单元测试
    :return:
    '''
    project_path = os.path.dirname(__file__)
    test_suite = unittest.TestLoader().discover(start_dir=project_path, pattern="*test.py")
    unittest.TextTestRunner().run(test_suite)

if __name__ == '__main__':
    run_test()