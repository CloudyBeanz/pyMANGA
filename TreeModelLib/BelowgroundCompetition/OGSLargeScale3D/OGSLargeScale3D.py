#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
import numpy as np
from TreeModelLib.BelowgroundCompetition import BelowgroundCompetition
import vtk as vtk
from lxml import etree
from os import path


class OGSLargeScale3D(BelowgroundCompetition):
    def __init__(self, args):
        ## SimpleTest case for belowground competition concept. This case is
        #  defined to test the passing of information between the instances.
        #  @VAR: Tags to define SimpleTest: type
        #  @date: 2019 - Today
        case = args.find("type").text
        self.ogs_project_folder = args.find("ogs_project_folder").text.strip()
        self.ogs_project_file = args.find("ogs_project_file").text.strip()
        self.ogs_source_mesh = args.find("source_mesh").text.strip()
        self.tree = etree.parse(path.join(self.ogs_project_folder,self.ogs_project_file))
        time_loop = self.tree.find("time_loop")
        time_loop__processes = time_loop.find("processes")
        time_loop__processes__process = time_loop__processes.find("process")
        time_stepping = time_loop__processes__process.find("time_stepping")
        self.xml_t_initial = time_stepping.find("t_initial")
        self.xml_t_end = time_stepping.find("t_end")
        self.cell_information = CellInformation(path.join(self.ogs_project_folder,self.ogs_source_mesh))
        self.volumes = self.cell_information.getCellVolumes()
        self.tree.write("test.xml")
        self.source_mesh_name = args.find("source_mesh").text
        print("Initiate belowground competition of type " + case + ".")

    def calculateBelowgroundResources(self):
        ## This function returns the BelowgroundResources calculated in the
        #  subsequent timestep. In the SimpleTest concept, for each tree a one
        #  is returned
        #  @return: np.array with $N_tree$ scalars
        exit()


    def prepareNextTimeStep(self, t_ini, t_end):
        ## This functions prepares the competition concept for the competition
        #  concept. In the SimpleTest concept, trees are saved in a simple list
        #  and the timestepping is updated. In preparation for the next time-
        #  step, the list is simply resetted.
        #  @VAR: t_ini - initial time for next timestep \n
        #  t_end - end time for next timestep
        self.trees_to_mesh_cell_id_map = []
        self.i = 0

        self.xml_t_initial.text = str(t_ini)
        self.xml_t_end.text = str(t_end)

        self.constant_contributions = np.zeros_like(self.volumes)
        self.salinity_prefactors = np.zeros_like(self.volumes)
        #  TODO: rename file
        filename = path.join(self.ogs_project_folder, self.ogs_project_file)
        self.tree.write("test.xml")

    def addTree(self, x, y, geometry, parameter):
        ## Before being able to calculate the resources, all tree enteties need
        #  to be added with their current implementation for the next timestep.
        #  Here, in the SimpleTest case, each tree is represented by a one. In
        #  general, an object containing all necessary information should be
        #  stored for each tree
        #  @VAR: position, geometry, parameter
        self.i +=1
        self.trees_to_mesh_cell_id_map.append(1)
        affected_cells = self.cell_information.getCellIDsAtXY(x,y)
        v = 0

        for cell_id in affected_cells:
            v_i = self.volumes.GetTuple(cell_id)[0]

            v+=v_i

        for cell_id in affected_cells:
            self.constant_contributions[cell_id] += .1
            self.salinity_prefactors[cell_id] += .1



class CellInformation:
    def __init__(self, source_mesh):
        meshReader = vtk.vtkXMLUnstructuredGridReader()
        meshReader.SetFileName(source_mesh)
        meshReader.Update()
        self.grid = meshReader.GetOutput()
        self.cell_finder = vtk.vtkCellLocator()
        self.cell_finder.SetDataSet(self.grid)
        self.cell_finder.LazyEvaluationOn()
        cells = self.grid.GetCellData()
        self.volumes = cells.GetArray("Volume")

    def getCellId(self, x, y, z):
        cell_id = self.cell_finder.FindCell([x, y, z])
        return cell_id

## This function returns all the cell ids of the grid at a given x,y coordinate
#  At the moment, it is only implemented as a "hackish" thing. Suggestions for
#  improvements are most welcome.
    def getCellIDsAtXY(self, x, y):
        p1 = [x, y, 22]
        p2 = [x, y, self.grid.GetBounds()[-2]]
        def linepoint(y):
            return np.array(p1) + y * (np.array(p2) - np.array(p1))
        search = 1
        i = 0
        ids = []
        while(search):
            xi = np.random.uniform()
            point = (linepoint(xi))
            iD = (self.getCellId(point[0],point[1],point[2]))
            if (iD not in ids) and (iD != -1):
                ids.append(iD)
            i+=1
            if len(ids)==3:
                search = 0
            elif i == 1e9:
                search = 0
                raise ValueError("Search algorithm failed! Please improve" +
                                 " algorithm!")
        return ids

    def getCellVolumeFromId(self, cell_id):
        cell_volume = self.volumes.GetTuple(cell_id)[0]
        return cell_volume

    def getCellVolumeFromCoordinates(self, x, y, z):
        cell_id = self.getCellId(self, x, y, z)
        return self.getCellVolumeFromId(self, cell_id)

    def getCellVolumes(self):
        return self.volumes

source = "/home/bathmann/Dokumente/UFZ/code/tmp/testproject/prj/source_domain.vtu"
cell_finder = CellInformation(source)
cell_finder.getCellIDsAtXY(55,50)
