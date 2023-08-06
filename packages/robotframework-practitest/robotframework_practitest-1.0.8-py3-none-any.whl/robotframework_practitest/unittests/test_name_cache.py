from unittest import TestCase

from robotframework_practitest.utils.data_service import CacheLibraryService, CacheItem


class TestNameCache(TestCase):
    data = None

    @classmethod
    def setUpClass(cls):
        cls.data = CacheLibraryService()

    def setUp(self):
        print(f"setUp: {self._testMethodName}")

    def tearDown(self):
        print(f"tearDown: {self._testMethodName}")

    def test_name_cache_01(self):
        cache_item = CacheItem('key1', 'key1.1')
        self.data[cache_item] = '11'
        print(f"{cache_item}: {self.data[cache_item]}")

    def test_name_cache_02(self):
        cache_item = CacheItem('key1', 'key1.2')
        self.data[cache_item] = '12'
        print(f"{cache_item}: {self.data[cache_item]}")

    def test_name_cache_021(self):
        cache_item = CacheItem('key1', 'key1.2')
        self.data[cache_item] = '13'
        print(f"{cache_item}: {self.data[cache_item]}")

    def test_name_cache_03(self):
        cache_item = CacheItem('key2', 'key2.1')
        self.data[cache_item] = '21'
        print(f"{cache_item}: {self.data[cache_item]}")

    def test_name_cache_04(self):
        cache_item = CacheItem('key2', 'key2.2')
        self.data[cache_item] = '22'
        print(f"{cache_item}: {self.data[cache_item]}")

