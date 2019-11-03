#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import MowItNow


class ExpectOutput(unittest.TestCase):
    test_file = os.getcwd() + "/MowItNow.out"

    def mower_expected(self):
        ref_file = os.getcwd() + "/expected.out"
        input_file = os.getcwd() + "/expected.txt"
        element = MowItNow.main(input_file)
        self.assertListEqual(list(open(test_file)), list(open(ref_file)))

    def mower_out_of_perimeter(self):
        ref_file = os.getcwd() + "/mowerout.out"
        input_file = os.getcwd() + "/mowerout.txt"
        element = MowItNow.main(input_file)
        self.assertListEqual(list(open(test_file)), list(open(ref_file)))

    def mower_collision(self):
       ref_file = os.getcwd() + "/mowercollision.out"
       input_file = os.getcwd() + "/mowercollision.txt"
       element = MowItNow.main(input_file)
       self.assertListEqual(list(open(test_file)), list(open(ref_file)))

if __name__ == "__main__":
    unittest.main()
