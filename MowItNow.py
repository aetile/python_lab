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

    def __init__(self, name, limX, limY, X, Y, compass):
        """
        parameters:
            name:       mower identifier (str)
            limit:      mower position limits (str)
            position:   mower position (str)

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


class Field:
    """
    Mower fleet field class

    """

    def __init__(self, width, length):
        """
        parameters:
            limit:     field limits (str)

        """
        self.length = length
        self.width = width
        self.matrix = np.zeros(shape=(self.width + 1, self.length + 1))
        self.mowers = []
        print(self.matrix)

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
        self.matrix[mower.X, mower.Y] = 1
        print(self.matrix)
        return mower

    def mower_move(self, mower, instructions):
        """
        parameters:
            mower:          mower instance to move
            instructions:   move instructions (str)

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

        print(self.matrix)
        return str(mower.X) + " " + str(mower.Y) + " " + str(mower.compass)

    def field_map(self, output_file):
        try:
            with open(output_file, "w") as outf:
                for mow in self.mowers:
                    line = str(mow.X) + " " + str(mow.Y) + " " + mow.compass
                    outf.write(line + "\n")
        except EnvironmentError as err:
            print("Unexpected environment error: {0}".format(err))
        return output_file


class Data:
    """
    Data processing class

    """

    def __init__(self, input_file, output_file):
        try:
            with open(input_file, "r") as inf:
                index = 0
                inf.seek(0)
                # Create mower field with line zero
                limit = inf.readline()
                limX, limY = limit.split(" ")
                limX, limY = int(limX), int(limY)
                self.garden = Field(limX, limY)
                # Additional lines gives mower position and instructions
                position, instruction = inf.readline(), inf.readline().strip()
                # Execute mower life
                while position:
                    name = "mower_" + str(index + 1)
                    # Mower has position: create mower instance
                    log.info(name + " - Position is: " + position)
                    currentmower = self.garden.mower_add(name, position)
                    # Mower has instructions: mower mows
                    log.info(name + " - Executing instruction: " + instruction)
                    new_position = self.garden.mower_move(currentmower, instruction)
                    log.info(name + " - New position is: " + new_position)
                    # Process next mower
                    position, instruction = inf.readline(), inf.readline()
                    index += 1
        except EnvironmentError as err:
            print("Unexpected environment error: {0}".format(err))
        self.garden.field_map(output_file)
        with open(output_file) as outf:
            print(outf.read())


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
    Data(input_file, output_file)


if __name__ == "__main__":
    main(sys.argv)
