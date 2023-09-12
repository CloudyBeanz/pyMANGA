import OpenGeoSys
import vtk as vtk
import numpy as np
from math import pi, sin
import os

def tidal_cycle(t):
    return ((sin(2 * pi * t / tide_daily_period) + 1) * tide_daily_amplitude)

def transectElevation(x, m=1e-2):
    return float(m * x)

def pressure_value(z,x, tidal_cycle):
    return 1000 * 9.81 * (max(tidal_cycle, transectElevation(x)) - z)

## Dirichlet BCs
class BCSea_p_D(OpenGeoSys.BoundaryCondition):

    def getDirichletBCValue(self, t, coords, node_id, primary_vars):
        x, y, z = coords
        tide = tidal_cycle(t)
        value = pressure_value(z, x, tide)
        if tide < z:
            return (False, 0)
        else:
            return (True, value)

class BCLand_p_D(OpenGeoSys.BoundaryCondition):
    def getDirichletBCValue(self, t, coords, node_id, primary_vars):
        x, y, z = coords
        value = pressure_value(z, x, 0)
        return (True, value)

## Dirichlet BCs
class BCSea_C(OpenGeoSys.BoundaryCondition):
    def getDirichletBCValue(self, t, coords, node_id, primary_vars):
        x, y, z = coords
        tide = tidal_cycle(t)
        value = seaward_salinity
        if tide < z:
            return (False, 0)
        else:
            return (True, value)

class BCLand_C(OpenGeoSys.BoundaryCondition):
    def getDirichletBCValue(self, t, coords, node_id, primary_vars):
        value = landward_salinity
        return (True, value)

landward_salinity = 0.025
seaward_salinity = 0.035
tide_daily_amplitude = 0.25
tide_monthly_amplitude = 0
tide_daily_period = 60 * 60 * 12.
tide_monthly_period = 60. * 60 * 24 * 31 / 2.

bc_tide_p = BCSea_p_D()
bc_land_p = BCLand_p_D()
bc_tide_C = BCSea_C()
bc_land_C = BCLand_C()
