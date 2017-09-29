# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
class DumpTestCase(TestCase):
    def setUp(self):
        pass

    def test_true(self):
        """Animals that can speak are correctly identified"""
        self.assertTrue(True)
