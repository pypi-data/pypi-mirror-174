"""This module includes Robot service for reporting results to Report Portal.

"""
from __future__ import annotations

import logging
from typing import Optional

from robot.api import logger
from robot.result.model import TestSuite as RSuite, TestCase as RTest
from robot.running import TestSuite as ESuite, TestCase as ETest

import robotframework_practitest.models.practi_test as practit_m
import robotframework_practitest.models.robot as robot_m
from robotframework_practitest.models import adapter
from robotframework_practitest.models.robot.helpers import PT_MANAGED_ITEMS, set_tag_mapping, publish_to_metadata, \
    log_report
from robotframework_practitest.models.robot.running import get_parents_path
from robotframework_practitest.utils.background_service import *
from robotframework_practitest.utils.logger import LOGGER as bg_logger
from robotframework_practitest.utils.misc_utils import get_error_info, read_variables


class PractiTestReportService(adapter.RobotToPractiTest_Adapter):
    """Class represents service that sends Robot items to PractiTest API."""
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        """Initialize service attributes."""
        self.enabled_reporting = False
        self.api_client: Optional[practit_m.PtClient] = None
        self.test_set_level = None
        self.current_suite_path_list = []

        self.version = None
        self.external_run_id = None
        self._metadata_collection = []

        adapter.RobotToPractiTest_Adapter.__init__(self)

    @property
    def test_set_name(self):
        return '/'.join(self.current_suite_path_list)

    def init_api(self, **kwargs):
        """Initialize common PractiTest API client."""
        if self.api_client is None:
            try:
                log_level = kwargs.get('LOG_LEVEL')
                logging.basicConfig(
                    format='[%(asctime)s][%(threadName)s : %(filename)s: %(lineno)d] %(levelname)s - %(message)s',
                    level='DEBUG' if log_level == 'TRACE' else log_level,
                    handlers=[logging.StreamHandler()])
                endpoint = kwargs.get('PT_ENDPOINT', None)
                project = kwargs.get('PT_PROJECT_NAME', None)
                tester_name = kwargs.get('PT_USER_NAME', None)
                user_email = kwargs.get('PT_USER_NAME_EMAIL', None)
                user_token = kwargs.get('PT_USER_TOKEN', None)
                set_tag_mapping(kwargs.get('TAG_MAPPING'))
                bg_logger.info(
                    'PractiTest API - Init session: '
                    'endpoint={0}, project={1}, User={2}'.format(endpoint, project, tester_name))

                self.version = kwargs.get('PT_VERSION')
                self.external_run_id = kwargs.get('PT_EXTERNAL_RUN_ID')
                self.test_set_level = kwargs.get('PT_TEST_SET_LEVEL', 0)
                self.api_client = practit_m.PtClient(endpoint, project_name=project, tester_name=tester_name,
                                                     user_email=user_email, user_token=user_token,
                                                     foreground=kwargs.get('PT_FOREGROUND', False))
                self.api_client.initiate_session()
                self.init_adapter(self.api_client, *kwargs.get('PT_FIELDS_MAP'),
                                  **{PT_MANAGED_ITEMS.Test.name: kwargs.get(PT_MANAGED_ITEMS.Test.value),
                                     PT_MANAGED_ITEMS.TestSet.name: kwargs.get(PT_MANAGED_ITEMS.TestSet.value),
                                     PT_MANAGED_ITEMS.Instance.name: kwargs.get(PT_MANAGED_ITEMS.Instance.value)
                                     })
                self.enabled_reporting = True
            except AssertionError as e:
                f, li = get_error_info()
                bg_logger.warn(f"{e}; File: {f}:{li}")
        else:
            bg_logger.warn('Practitest service already initialized.')

    def close(self):
        """Terminate common PractiTest API Client."""
        BackgroundAsync.join()
        BackgroundSync.join()
        if self.api_client is not None:
            self.api_client.terminate_session()

    def start_suite(self, suite: ESuite, result: RSuite):
        """Call start_test method of the common client.

        :param result:
        :param suite: model.Suite object
        :return:
        """
        try:
            if suite.parent is None:
                self.init_api(**read_variables(*practit_m.PRACTI_TEST_VARIABLES))
            if not self.enabled_reporting:
                return

            if len(get_parents_path(suite)) == self.test_set_level:
                data_snapshot = robot_m.running.PTestSuite(suite)
                self.create_test_set(data_snapshot, self.version, run_id=self.external_run_id)
                set_data = self.get_active_test_set_id(20)
                self._metadata_collection.append(dict(suite=suite.name, project_id=self.project_id, **set_data))
        except Exception as e:
            f, li = get_error_info()
            logger.error(f"{e}; File: {f}:{li}")

    def end_suite(self, suite: ESuite, result: RSuite):
        if not self.enabled_reporting:
            return
        if suite.parent is None:
            publish_to_metadata("PractiTest report", *self._metadata_collection)
            log_report("PractiTest report", *self._metadata_collection)
            # links = []
            # for index, meta_item in enumerate(self._metadata_collection):
            #     links.append(add_to_suite_metadata(nl='' if index == 0 else '<br>\n', **meta_item))
            # logger.warn(
            #     "PractiTest reports:\n\t{}".format('\n\t'.join([f"{i+1:02d}. {n}" for i, n in enumerate(links)])),
            #     html=True)

        bg_logger.log_background_messages()

    def start_test(self, test: ETest, result: RTest):
        if not self.enabled_reporting:
            return
        try:
            bg_logger.log_background_messages()
            BackgroundSync.put(Task(
                self.create_test_instance, robot_m.running.PTestCase(test), self.version)
            )
            # self.create_test_instance(robot_m.running.PTestCase(test), self.version)
        except Exception as e:
            f, li = get_error_info()
            logger.warn(f"{e}; File: {f}:{li}")

    def end_test(self, test: ETest, result: RTest):
        if not self.enabled_reporting:
            return
        try:
            bg_logger.log_background_messages()
            BackgroundAsync.put(Task(
                self.set_test_results, robot_m.running.PTestCase(test), robot_m.running.PTestResult(result))
            )
            # self.set_test_results(robot_m.running.PTestCase(test), robot_m.running.PTestResult(result))
        except Exception as e:
            f, w = get_error_info()
            logger.warn(f"{e}; File: {f}:{w}")


__all__ = [
    'PractiTestReportService'
]
