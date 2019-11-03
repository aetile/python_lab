#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import MowItNow


class TestMower(unittest.TestCase):
    output_filename = os.getcwd() + "/test_MowItNow.out"

    def test_field_created(self):
        """
        Check if mower field is creates the correct bitmap
        """
        ref_filename = os.getcwd() + "/expected.out"
        input_filename = os.getcwd() + "/expected.txt"
        with open(input_filename) as hf:
            width, length = hf.readline().split(' ')
            width, length = int(width), int(length)
        element = MowItNow.Field(input_filename, self.output_filename)
        self.assertEqual(width, element.width)
        self.assertEqual(length, element.length)

    def test_mower_moves(self):
        """
        Check if mower follows instructions
        """
        field_map = [
                    [0 for i in range(4)] for j in range(3)
                ]
        result_map = field_map
        result_map[1][1] = 1
        element = MowItNow.Mower("mow_test1", 3, 2, 0, 0, "S")
        new_map = element.move("ADA", field_map)
        self.assertEqual(new_map, result_map)

    def test_mower_collide(self):
        """
        Check that mower ignores instruction when colliding another mower
        """
        field_map = [
                    [0 for i in range(4)] for j in range(3)
                ]
        field_map[1][1] = 1
        result_map = field_map
        result_map[0][1] = 1
        element = MowItNow.Mower("mow_test1", 3, 2, 0, 0, "S")
        new_map = element.move("ADA", field_map)
        self.assertEqual(new_map, result_map)

    def test_mower_expected(self):
        """
        Check that expected result from the test is met
        """
        ref_filename = os.getcwd() + "/expected.out"
        input_filename = os.getcwd() + "/expected.txt"
        sys.argv = [ sys.argv[0], input_filename, self.output_filename]
        element = MowItNow.main(sys.argv)
        self.assertListEqual(list(open(self.output_filename)), list(open(ref_filename)))

    def test_mower_out_of_perimeter(self):
        """
        Check mower stays inside perimeter if receiving bad isntructions
        """
        ref_filename = os.getcwd() + "/mowerout.out"
        input_filename = os.getcwd() + "/mowerout.txt"
        sys.argv = [ sys.argv[0], input_filename, self.output_filename]
        element = MowItNow.main(sys.argv)
        self.assertListEqual(list(open(self.output_filename)), list(open(ref_filename)))

    def test_mower_collision(self):
        """
        Check mowers continue to follow instructions after a bad instruction
        """
        ref_filename = os.getcwd() + "/mowercollision.out"
        input_filename = os.getcwd() + "/mowercollision.txt"
        sys.argv = [ sys.argv[0], input_filename, self.output_filename]
        element = MowItNow.main(sys.argv)
        self.assertListEqual(list(open(self.output_filename)), list(open(ref_filename)))


if __name__ == "__main__":
    unittest.main()
