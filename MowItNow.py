#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import logging
from pprint import pformat

log = logging.getLogger()
log.setLevel("INFO")


class Mower:
    """
    Automated finite-state mower class

    """

    forward = "A"
    rotate = "DG"
    orientations = {
        "N": {"D": "E", "G": "W"},
        "S": {"D": "W", "G": "E"},
        "E": {"D": "S", "G": "N"},
        "W": {"D": "N", "G": "S"},
    }

    def __init__(self, name, lim_x, lim_y, x, y, compass):
        """
        parameters:
            name:       mower identifier (str)
            lim_x:      mower x position limit (int)
            lim_y:      mower y position limit (int)
            x:          mower current x position (int)
            y:          mower current y position (int)
            compass:    mower cardinal direction (char)

        """
        self.name = name
        self.lim_x = int(lim_x)
        self.lim_y = int(lim_y)
        self.x = int(x)
        self.y = int(y)
        self.compass = compass.strip()
        # Mower is a finite-state machine
        self.step = {
            "N": (lambda x, y: (x, min(y + 1, self.lim_y))),
            "S": (lambda x, y: (x, max(y - 1, 0))),
            "E": (lambda x, y: (min(x + 1, self.lim_x), y)),
            "W": (lambda x, y: (max(x - 1, 0), y)),
        }

    def move(self, instructions, field_map):
        """
        parameters:
            instructions:   move instructions (str)
            field_map:      mower field bitmap (array)

        """
        for instr in instructions.strip():
            if instr in self.rotate:
                self.compass = self.orientations[self.compass][instr]
            elif instr == self.forward:
                x, y = self.step[self.compass](self.x, self.y)
                # Collision detection: if destination bit is 1 a mower is already present: instruction is ignored
                if not field_map[x][y]:
                    (
                        field_map[self.lim_y - y][x],
                        field_map[self.lim_y - self.y][self.x],
                    ) = (1, 0)
                    self.x, self.y = x, y
            else:
                log.error("Invalid instruction: {}".format(instr))

        return field_map


class Field:
    """
    Mower fleet field class

    """

    def __init__(self, in_fname, out_fname):
        """
        parameters:
            input_file:     input file containing data: field dimensions, mowers postions and instructions (file)
            output_file:    output file for writing mowers final positions (file)

        """
        self.in_fname = in_fname
        self.out_fname = out_fname
        self.width = 0
        self.length = 0
        self.mowers = []
        self.map = []
        self.mow()

    def mower_add(self, name, position):
        """
        parameters:
            name:       mower identifier (str)
            position:   mower position (str)

        """
        pos_x, pos_y, orientation = position.split(" ")
        pos_x, pos_y = int(pos_x), int(pos_y)
        mower = Mower(name, self.width, self.length, pos_x, pos_y, orientation)
        self.mowers.append(mower)
        self.map[self.length - mower.y][mower.x] = 1
        log.info("Current bitmap:\n" + pformat(self.map))
        return mower

    def mower_report(self):
        """
        """
        try:
            with open(self.out_fname, "w") as outf:
                for mow in self.mowers:
                    line = str(mow.x) + " " + str(mow.y) + " " + mow.compass
                    outf.write(line + "\n")
        except EnvironmentError as err:
            log.error("Unexpected environment error: {0}".format(err))
        return self.out_fname

    def mow(self):
        """
        """
        try:
            with open(self.in_fname, "r") as hf:
                index = 0
                # Create mower field bitmap with line zero
                limit = hf.readline()
                self.width, self.length = limit.split(" ")
                self.width, self.length = int(self.width), int(self.length)
                self.map = [
                    [0 for i in range(self.width + 1)] for j in range(self.length + 1)
                ]
                log.info("Current bitmap:\n" + pformat(self.map))
                # Additional lines gives mower position and instructions
                position, instruction = hf.readline(), hf.readline().strip()
                # Execute mower life
                while position:
                    name = "mower_" + str(index + 1)
                    # Mower has position: create mower instance
                    log.info(name + " - Position is: " + position)
                    currentmower = self.mower_add(name, position)
                    # Mower has instructions: mower mows
                    log.info(name + " - Executing instruction: " + instruction)
                    self.map = currentmower.move(instruction, self.map)
                    new_position = (
                        str(currentmower.x)
                        + " "
                        + str(currentmower.y)
                        + " "
                        + currentmower.compass
                    )
                    log.info(name + " - New position is: " + new_position)
                    log.info("Current bitmap:\n" + pformat(self.map))
                    # Process next mower
                    position, instruction = hf.readline(), hf.readline()
                    index += 1
        except EnvironmentError as err:
            log.error("Unexpected environment error: {0}".format(err))
        return self.mower_report()


def main(argv):
    # Output file path
    output_filename = os.getcwd() + "/MowItNow.out"

    # Logging handler
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    )
    log.addHandler(handler)

    # Expecting one argument
    if len(argv) == 1:
        raise RuntimeError("No argument specified")
    input_filename = argv[1]

    # Expecting an input file
    if not os.path.isfile(input_filename):
        raise RuntimeError("Invalid input file or file not found")

    # Process data
    garden = Field(input_filename, output_filename)


if __name__ == "__main__":
    main(sys.argv)
