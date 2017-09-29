# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
class DumbTestCase(TestCase):
    def setUp(self):
        pass

    def test_true(self):
        """ Test to see if the test suite works"""
        self.assertTrue(True)
