#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""

from TreeModelLib.GrowthAndDeathDynamics.Mortality.NoGrowth import NoGrowth


class Memory(NoGrowth):

    def __init__(self, args, case):
        super().__init__(args, case)
        # Read input parameters from xml file
        self.getInputParameters(args)
        # Default values if no inputs are given
        try:
            self._threshold
        except:
            # Threshold for biomass increment: 0.5 %
            self._threshold = 0.5 / 100
            print("NOTE: Use default `threshold`: " + str(self._threshold) +
                  ".")
        try:
            self._period
        except:
            # Duration of growth memory: 1 year
            self._period = 1 * 365.25 * 24 * 3600
            print("NOTE: Use default `period`: " + str(self._period) + ".")

    def setSurvival(self, args):
        self._survive = 1

        # Get the number of values representing the memory period
        steps = int(self._period / args.time)

        # Slice grow_memory array to get only relevant data
        relevant_grow_memory = args.grow_memory[-steps:]

        # Check only for survival if memory exist
        if relevant_grow_memory:
            # Calculate total growth during memory period (m³ per period)
            grow_memory = sum(relevant_grow_memory)

            # Calculate growth relative to biomass (m³ per m³)
            relative_grow = grow_memory / args.volume

            # Check if relative growth is below a certain threshold
            if relative_grow < self._threshold:
                self._survive = 0
                print("\t Tree died (Memory).")

    def getSurvive(self):
        return self._survive

    def setMortalityVariables(self, args, growth_concept_information):
        # Variable to store growth (m³ per time step)
        try:
            args.grow_memory = growth_concept_information["grow_memory"]
        except KeyError:
            args.grow_memory = []

    def getMortalityVariables(self, args, growth_concept_information):
        args.grow_memory.append(args.grow)
        growth_concept_information["grow_memory"] = \
            args.grow_memory
        return growth_concept_information

    def getInputParameters(self, args):
        # All tags are optional
        missing_tags = ["type", "mortality", "threshold", "period"]
        for arg in args.iterdescendants():
            tag = arg.tag
            if tag == "threshold":
                self._threshold = float(args.find("threshold").text)
            elif tag == "period":
                self._period = float(args.find("period").text)
            elif tag == "type":
                case = args.find("type").text
            try:
                missing_tags.remove(tag)
            except ValueError:
                print("WARNING: Tag " + tag + " not specified for " +
                      super().getConceptName() + " (" + case + ") " +
                      "mortality initialisation!")
