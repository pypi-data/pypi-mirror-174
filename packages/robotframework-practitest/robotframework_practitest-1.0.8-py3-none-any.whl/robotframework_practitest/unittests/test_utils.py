from unittest import TestCase
from robotframework_practitest.models.practi_test.data_formatters import practi_test_duration


class TestUtils(TestCase):
    def test_practi_test_duration_35(self):
        dur = 35
        pt_dur = practi_test_duration(dur)
        print(f"{dur} - {pt_dur}")

    def test_practi_test_duration_60(self):
        dur = 60
        pt_dur = practi_test_duration(dur)
        print(f"{dur} - {pt_dur}")

    def test_practi_test_duration_120(self):
        dur = 120
        pt_dur = practi_test_duration(dur)
        print(f"{dur} - {pt_dur}")

    def test_practi_test_duration_3645(self):
        dur = 3645
        pt_dur = practi_test_duration(dur)
        print(f"{dur} - {pt_dur}")

    def test_practi_test_duration_3760(self):
        dur = 3760
        pt_dur = practi_test_duration(dur)
        print(f"{dur} - {pt_dur}")
