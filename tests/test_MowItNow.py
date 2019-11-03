#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import MowItNow


class ExpectOutput(unittest.TestCase):
    output_filename = os.getcwd() + "/MowItNow.out"

    def field_created(self):
        """
        Check if mower field is creates the correct bitmap
        """
        ref_filename = os.getcwd() + "/expected.out"
        input_filename = os.getcwd() + "/expected.txt"
        with open(input_filename) as hf:
            width, length = hf.readline()
            width, length = int(width), int(length)
        element = MowItNow.Field(input_filename, output_filename)
        self.assertEqual(width, element.width)
        self.assertEqual(length, element.length)

    def mower_moves(self):
        """
        Check if mower follows instructions
        """
        field_map = [[0, 0, 0][0, 0, 0]]
        element = MowItNow.Mower("mow_test1", 1, 2, 0, 0, "N", field_map)
        new_map = element.move("ADA", field_map)
        self.assertEqual(new_map, [[0, 0, 0], [0, 1, 0]])

    def mower_collide(self):
        """
        Check that mower ignores instruction when colliding another mower
        """
        field_map = [[0, 0, 0][0, 1, 0]]
        element = MowItNow.Mower("mow_test1", 1, 2, 0, 0, "N", field_map)
        new_map = element.move("AA", field_map)
        self.assertEqual(new_map, [[0, 1, 0][0, 1, 0]])

    def mower_expected(self):
        """
        Check that expected result from the test is met
        """
        ref_filename = os.getcwd() + "/expected.out"
        input_filename = os.getcwd() + "/expected.txt"
        element = MowItNow.main(input_filename)
        self.assertListEqual(list(open(output_filename)), list(open(ref_filename)))

    def mower_out_of_perimeter(self):
        """
        Check mower stays inside perimeter if receiving bad isntructions
        """
        ref_filename = os.getcwd() + "/mowerout.out"
        input_filename = os.getcwd() + "/mowerout.txt"
        element = MowItNow.main(input_filename)
        self.assertListEqual(list(open(output_filename)), list(open(ref_filename)))

    def mower_collision(self):
        """
        Check mowers continue to follow instructions after a bad instruction
        """
        ref_filename = os.getcwd() + "/mowercollision.out"
        input_filename = os.getcwd() + "/mowercollision.txt"
        element = MowItNow.main(input_filename)
        self.assertListEqual(list(open(output_filename)), list(open(ref_filename)))


if __name__ == "__main__":
    unittest.main()
