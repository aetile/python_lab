#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import logging
import numpy as np

log = logging.getLogger()
log.setLevel("INFO")


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

    def __init__(self, name, limit, position):
        """
        param name: mower identifier (str)
        param limit: mower position limits (str)
        param position: mower position (str)

        """
        self.name = name
        self.limX, self.limY = limit.split(" ")
        self.limX, self.limY = int(self.limX), int(self.limY)
        self.X, self.Y, self.compass = position.split(" ")
        self.X, self.Y, self.compass = int(self.X), int(self.Y), self.compass.strip()
        self.step = {
            "N": (lambda x, y: (x, min(y + 1, self.limY))),
            "S": (lambda x, y: (x, max(y - 1, 0))),
            "E": (lambda x, y: (min(x + 1, self.limX), y)),
            "W": (lambda x, y: (max(x - 1, 0), y)),
        }


class Field:
    """
    Mower field class

    """

    def __init__(self, limit):
        """
        param length: field length (int)
        param width: field width (int)
        param mowers: instances of mower class belonging to the field (list of mower class instances)

        """

        self.length, self.width = limit.split(" ")
        self.length, self.width = int(self.length), int(self.width)
        self.mowers = []
        self.matrix = np.zeros(shape=(self.width +1, self.length +1))
        print(self.matrix)

    def add_mower(self, name, limit, position):
        """
        param limit: mower limits (str)
        param position: mower postion (str)

        """
        mower = Mower(name, limit, position)
        self.mowers.append(mower)
        self.matrix[mower.X, mower.Y] = 1
        print(self.matrix)
        return mower

    def move_mower(self, mower, instructions):
        """
        param mower: mower instance to move
        param instructions: move instruction (str)

        """
        for instr in instructions.strip():
            if instr in mower.rotate:
                mower.compass = mower.orientations[mower.compass][instr]
            elif instr == mower.forward:
                x, y = mower.step[mower.compass](mower.X, mower.Y)
                if self.matrix[x, y] == 0:
                    self.matrix[x, y], self.matrix[mower.X, mower.Y] = 1, 0
                    mower.X, mower.Y = x, y
            else:
                log.error("Invalid instruction: {}".format(instr))

        return str(mower.X) + " " + str(mower.Y) + " " + str(mower.compass)


def main(argv):
    # Log handler
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    )
    log.addHandler(handler)

    # Expecting one argument
    if len(argv) == 1:
        raise RuntimeError("Input file not specified")
    input_file = argv[1]
    output_file = os.getcwd() + "/MowItNow.out"

    # Expecting an input file
    if not os.path.isfile(input_file):
        raise RuntimeError("Invalid input file or file not found")

    # Initialize output file
    with open(output_file, "w") as outf:
        outf.truncate()

    # Execute input file instructions
    try:
        with open(input_file, "r") as inf:
            index = 0
            fleet = []
            inf.seek(0)
            # Line zero gives field limits
            limit = inf.readline()
            garden = Field(limit)
            # The following 2 lines respectively gives position and instructions
            position, instruction = inf.readline(), inf.readline()
            while position:
                name = "mower_" + str(index + 1)
                log.info(name + " - Position is: " + position)
                currentmower = garden.add_mower(name, limit, position)
                log.info(name + " - Executing instruction: " + instruction)
                new_position = garden.move_mower(currentmower, instruction)
                log.info(name + " - New position is: " + new_position)
                with open(output_file, "a") as outf:
                    outf.write(new_position + "\n")
                position, instruction = inf.readline(), inf.readline()
                index += 1
    except EnvironmentError as err:
        print("Unexpected environment error: {0}".format(err))

    return output_file


if __name__ == "__main__":
    main(sys.argv)
