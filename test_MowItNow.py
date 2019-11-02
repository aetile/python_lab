#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
import MowItNow
import io


class ExpectOutput(unittest.TestCase):
    def mower_expected(self):
        test_file = os.getcwd() + "/MowItNow.out"
        ref_file = os.getcwd() + "/expected.out"
        input_file = os.getcwd() + "/expected.txt"
        element = MowItNow.main(input_file)
        self.assertListEqual(list(io.open(test_file)), list(io.open(ref_file)))

    def mower_out_of_perimeter(self):
        test_file = os.getcwd() + "/MowItNow.out"
        ref_file = os.getcwd() + "/mowerout.out"
        input_file = os.getcwd() + "/mowerout.txt"
        element = MowItNow.main(input_file)
        self.assertListEqual(list(io.open(test_file)), list(io.open(ref_file)))

if __name__ == "__main__":
    unittest.main()
