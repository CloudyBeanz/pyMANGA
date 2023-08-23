#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from ResourceLib import ResourceModel


class FON(ResourceModel):
    def __init__(self, args):
        """
        Below-ground resource concept.
        Args:
            args: FON module specifications from project file tags
        """
        case = args.find("type").text
        print("Initiate belowground competition of type " + case + ".")
        self.getInputParameters(args)
        super().makeGrid()
        if self._mesh_size > 0.25:
            print("Error: mesh not fine enough for FON!")
            print("Please refine mesh to grid size < 0.25m !")
            exit()

    def prepareNextTimeStep(self, t_ini, t_end):
        self._fon_area = []
        self._fon_impact = []
        self._resource_limitation = []
        self._salinity_reduction = []
        self._xe = []
        self._ye = []
        self._salt_effect_d = []
        self._salt_effect_ui = []
        self._r_stem = []
        self._t_ini = t_ini
        self._t_end = t_end
        self._fon_height = np.zeros_like(self._my_grid[0])

    def addPlant(self, plant):
        x, y = plant.getPosition()
        geometry = plant.getGeometry()
        parameter = plant.getParameter()
        self._xe.append(x)
        self._ye.append(y)
        self._salt_effect_d.append(parameter["salt_effect_d"])
        self._salt_effect_ui.append(parameter["salt_effect_ui"])
        self._r_stem.append(geometry["r_stem"])

    def calculateBelowgroundResources(self):
        """
        Calculate a growth reduction factor for each plant based on competition and
        pore-water salinity below the centre of each plant.
        Sets:
            numpy array with shape(number_of_plants)
        """
        self._r_stem = np.array(self._r_stem)
        distance = (((self._my_grid[0][:, :, np.newaxis] -
                      np.array(self._xe)[np.newaxis, np.newaxis, :])**2 +
                     (self._my_grid[1][:, :, np.newaxis] -
                      np.array(self._ye)[np.newaxis, np.newaxis, :])**2)**0.5)
        my_fon = self.calculateFonFromDistance(distance=distance)

        fon_areas = np.zeros_like(my_fon)
        # Add a one, where plant is larger than 0
        fon_areas[np.where(my_fon > 0)] += 1
        # Count all nodes, which are occupied by plants
        # returns array of shape (nplants)
        fon_areas = fon_areas.sum(axis=(0, 1))
        fon_heigths = my_fon.sum(axis=-1)

        fon_impacts = fon_heigths[:, :, np.newaxis] - my_fon
        fon_impacts[np.where(my_fon < self._fmin)] = 0
        fon_impacts = fon_impacts.sum(axis=(0, 1))

        # tree-to-tree competition, eq. (7) Berger & Hildenbrandt (2000)
        stress_factor = fon_impacts / fon_areas
        stress_factor = np.nan_to_num(stress_factor, nan=0)
        resource_limitations = 1 - 2 * stress_factor
        resource_limitations[np.where(resource_limitations < 0)] = 0
        self.belowground_resources = resource_limitations

    def calculateFonFromDistance(self, distance):
        """
        Calculate the FON height of each plant at each grid point.
        Args:
            distance (int): array of distances of all mesh points to plant position
        Returns:
            numpy array with shape(x_grid_points, y_grid_points, number_of_plants)
        """
        # fon radius, eq. (1) Berger et al. 2002
        fon_radius = self._aa * self._r_stem**self._bb
        cc = -np.log(self._fmin) / (fon_radius - self._r_stem)
        height = np.exp(-cc[np.newaxis, np.newaxis, :] *
                        (distance - self._r_stem[np.newaxis, np.newaxis, :]))
        height[height > 1] = 1
        height[height < self._fmin] = 0
        return height

    def getInputParameters(self, args, required_tags=None):
        tags = {
            "prj_file": args,
            "required": ["type", "domain", "x_1", "x_2", "y_1", "y_2", "x_resolution",
                         "y_resolution", "aa", "bb", "fmin", "salinity"]
        }
        super().getInputParameters(**tags)
        self.x_resolution = int(self.x_resolution)
        self.y_resolution = int(self.y_resolution)
        self._aa = self.aa
        self._bb = self.bb
        self._fmin = self.fmin
        self._salinity = self.salinity
