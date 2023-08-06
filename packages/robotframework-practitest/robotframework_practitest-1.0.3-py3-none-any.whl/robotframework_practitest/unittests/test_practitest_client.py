import logging, os.path
import json
import time
from unittest import TestCase

from robotframework_practitest.models.practi_test.client import *

logging.basicConfig(format='[%(asctime)s][%(threadName)s : %(filename)s:\t%(lineno)d] %(levelname)s - %(message)s',
                    level='DEBUG')

_, file = os.path.split(__file__)
log_name, _ = os.path.splitext(file)

logger = logging.getLogger(log_name)


class TestPractiTest_Client(TestCase):
    api_client = None
    tests = []
    data = {}
    test_name_pattern = 'New RobotFW evaluate test #01'
    steps = [
        {
            "name": "Step1",
            "description": "First step",
            "expected-results": ""
        },
        {
            "name": "Step2",
            "description": "Second step",
            "expected-results": ""
        }
    ]

    @classmethod
    def setUpClass(cls):
        cls.api_client = PtClient(user_email='qa@ad.morphisec.com',
                                  user_token='a759a50060228f2830253ded6db9e8b3142b3941',
                                  project_name='Morphisec - linux',
                                  tester_name='Dmitry Oguz')
        cls.api_client.initiate_session()
        logger.info(f"Suite started: {cls.api_client}")

    @classmethod
    def tearDownClass(cls):
        cls.api_client.terminate_session()
        logger.info("Suite ended")

    def tearDown(self):
        logger.info("Test ended")

    def test_02_create_test_for_default_user_id(self):

        custom_fields = {
            'Test level': 'Regression',
            'Components': 'MLP',
            'Automation Covering': 'Done',
            'Tag/s': 'MLP'
        }
        for i in range(0, 5):
            test_res = self.api_client.create_test_case(f"{self.test_name_pattern}{i:02d}",
                                                        '2.5.2',
                                                        'Dmitry Oguz',
                                                        f"Test example {i}",
                                                        TestTypes.ScriptedTest, None, None,
                                                        *self.steps,
                                                        **custom_fields)
            print(f"Test created: {json.dumps(test_res, indent=4)}\n------------------------")

    #
    # def test_02_is_exists(self):
    #     for index, test in enumerate(self._get_tests_list):
    #         test_id = self.api_client.query_test(display_id=test['data']['attributes']['display-id'])
    #         assert test_id
    #         print(f"{index}. ID: {test_id}")

    # def test_04_create_set(self):
    #     self.data['test_set_name'] = 'RobotFW Evaluate#2'
    #     res = self.api_client.create_test_set('RobotFW Evaluate#2',
    #                                   *[t['data']['attributes']['display-id'] for t in self._get_tests_list],
    #                                   version='2.5.2',
    #                                   **{'Build': '2.5.2-173', 'ENV': 'MLP',
    #                                      'Test level': 'Regression', 'Created_By': 'Dmitry',
    #                                      'OS version': 'Debian10', 'Automation Covering': 'Done',
    #                                      'Components': 'Smoke', 'Sprint': 'Sprint31'
    #                                      })
    #     print(f"{json.dumps(res, indent=4)}")
    #     self.data['test_set'] = res
    #
    def test_041_create_test_set_by_pattern(self):
        self.data['tests'] = self.api_client.query_test(name_exact=self.test_name_pattern)
        user_id = self.api_client.query_user_id('Dmitry Oguz')
        res = self.api_client.create_test_set('RobotTestSetEval#3',
                                              [t['id'] for t in self.data['_get_tests_list']['data']],
                                              version='2.5.2', assigned_to_id=user_id, author_id=user_id,
                                              **{'Build': '2.5.2-173', 'ENV': 'MLP',
                                                 'Test level': 'Regression', 'Created_By': 'Dmitry',
                                                 'OS version': 'Debian10', 'Automation Covering': 'Done',
                                                 'Components': 'Smoke', 'Sprint': 'Sprint31'
                                                 }
                                              )
        self.data['test_set'] = res
        logger.info(f"TestSet: {json.dumps(res, indent=3)}\n------------------------")

    def test_05_get_run_instances(self):
        test_set_id = self.data['test_set']['data']['id']
        tests = sorted([t['id'] for t in self.data['_get_tests_list']['data']])
        status = True
        start = time.perf_counter()
        for index, test_id in enumerate(tests):
            time.sleep(2)
            instance_res = self.api_client.get_run_tests_instances(test_set_id, test_id)
            logger.info(f"Instance to run: {json.dumps(instance_res, indent=4)}\n------------------------")
            self.api_client.run_test_case(instance_res['data'][0]['id'], 0 if status else 1,
                                          int(time.perf_counter() - start), f"Bla-bla {index:02d}")
            status = not status

