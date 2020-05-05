from unittest import TestCase
from utils import to_list


class TestTo_list(TestCase):
    def test_to_list(self):
        s = '[177,175,154,90,78,36,8]'
        a = to_list(s)
        self.assertEqual(type(a[2]), int)
        self.assertEqual(a[2], 154)
        self.assertEqual(s,str(a).replace(' ',''))

    def test_to_list_empty(self):
        s = '[]'
        a = to_list(s)
        self.assertEqual(s, str(a).replace(' ', ''))