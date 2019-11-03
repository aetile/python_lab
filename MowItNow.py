#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import logging
import pprint

log = logging.getLogger()
log.setLevel("INFO")
pp = pprint.PrettyPrinter(indent=4)


class Mower:
    """
    Automated mower class

    """

    forward = "A"
    rotate = "DG"
    orientations = {
        "N": {"D": "E", "G": "W"},
        "S": {"D": "W", "G": "E"},
        "E": {"D": "S", "G": "N"},
        "W": {"D": "N", "G": "S"},
    }

    def __init__(self, name, limX, limY, X, Y, compass):
        """
        parameters:
            name:       mower identifier (str)
            limX:       mower abscissa limit (int)
            limY:       mower ordinate limit (int)
            X:          mower current abscissa (int)
            Y:          mower current ordinate (int)
            compass:    mower cardinal direction (char)

        """
        self.name = name
        self.limX = int(limX)
        self.limY = int(limY)
        self.X = int(X)
        self.Y = int(Y)
        self.compass = compass.strip()
        self.step = {
            "N": (lambda x, y: (x, min(y + 1, self.limY))),
            "S": (lambda x, y: (x, max(y - 1, 0))),
            "E": (lambda x, y: (min(x + 1, self.limX), y)),
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
                x, y = self.step[self.compass](self.X, self.Y)
                if field_map[x][y] == 0:
                    field_map[x][y], field_map[self.X][self.Y] = 1, 0
                    self.X, self.Y = x, y
            else:
                log.error("Invalid instruction: {}".format(instr))

        return field_map


class Field:
    """
    Mower fleet field class

    """

    def __init__(self, input_file, output_file):
        """
        parameters:
            input_file:     input file containing data: field dimensions, mowers postions and instructions (file)
            output_file:    output file for writing mowers final positions (file)

        """
        self.input_file = input_file
        self.output_file = output_file
        self.width = 0
        self.length = 0
        self.mowers = []
        self.mow()

    def mower_add(self, name, position):
        """
        parameters:
            name:       mower identifier (str)
            position:   mower position (str)

        """
        posX, posY, orientation = position.split(" ")
        posX, posY = int(posX), int(posY)
        mower = Mower(name, self.width, self.length, posX, posY, orientation)
        self.mowers.append(mower)
        self.map[mower.X][mower.Y] = 1
        pp.pprint(self.map)
        return mower

    def mower_report(self):
        """
        """
        try:
            with open(self.output_file, "w") as outf:
                for mow in self.mowers:
                    line = str(mow.X) + " " + str(mow.Y) + " " + mow.compass
                    outf.write(line + "\n")
        except EnvironmentError as err:
            print("Unexpected environment error: {0}".format(err))
        return self.output_file

    def mow(self):
        """
        """
        try:
            with open(self.input_file, "r") as inf:
                index = 0
                inf.seek(0)
                # Create mower field bitmap with line zero
                limit = inf.readline()
                self.width, self.length = limit.split(" ")
                self.width, self.length = int(self.width), int(self.length)
                self.map = [
                    [0 for i in range(self.width + 1)] for j in range(self.length + 1)
                ]
                pp.pprint(self.map)
                # Additional lines gives mower position and instructions
                position, instruction = inf.readline(), inf.readline().strip()
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
                        str(currentmower.X)
                        + " "
                        + str(currentmower.Y)
                        + " "
                        + currentmower.compass
                    )
                    log.info(name + " - New position is: " + new_position)
                    pp.pprint(self.map)
                    # Process next mower
                    position, instruction = inf.readline(), inf.readline()
                    index += 1
        except EnvironmentError as err:
            print("Unexpected environment error: {0}".format(err))
        return self.mower_report()


def main(argv):
    # Output file path
    output_file = os.getcwd() + "/MowItNow.out"

    # Logging handler
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    )
    log.addHandler(handler)

    # Expecting one argument
    if len(argv) == 1:
        raise RuntimeError("No argument specified")
    input_file = argv[1]

    # Expecting an input file
    if not os.path.isfile(input_file):
        raise RuntimeError("Invalid input file or file not found")

    # Process data
    garden = Field(input_file, output_file)


if __name__ == "__main__":
    main(sys.argv)
