#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from dataclasses import dataclass
import itertools

import DataVisual.Tables as Table
import MPSPlots.Render2D as Plots


class DataV(object):
    def __init__(self, array, Xtable, Ytable, **kwargs):

        self.Data = array

        self.Xtable = Xtable if isinstance(Xtable, Table.XTable) else Table.XTable(Xtable) 
   
        self.Ytable = Ytable if isinstance(Ytable, Table.YTable) else Table.YTable(Ytable) 

    @property
    def Shape(self):
        return self.Data.shape

    def Mean(self, axis: str):
        """Method compute and the mean value of specified axis.
        The method then return a new DataV daughter object compressed in
        the said axis.

        Parameters
        ----------
        axis : :class:`str`
            Axis for which to perform the operation.

        Returns
        -------
        :class:`DataV`
            New DataV instance containing the mean value of axis.

        """
        Array = numpy.mean(self.Data, axis=axis.Position)

        return DataV(Array, Xtable=[x for x in self.Xtable if x != axis], Ytable=self.Ytable)

    def Std(self, axis: str):
        """
        Method compute and the std value of specified axis.
        The method then return a new DataV daughter object compressed in
        the said axis.

        Parameters
        ----------
        axis : :class:`str`
            Axis for which to perform the operation.

        Returns
        -------
        :class:`DataV`
            New DataV instance containing the std value of axis.

        """

        Array = numpy.mean(self.Data, axis=axis.Position)

        return DataV(array=Array, Xtable=[x for x in self.Xtable if x != axis], Ytable=self.Ytable)

    def Rsd(self, axis: str):
        """Method compute and the rsd value of specified axis.
        The method then return a new DataV daughter object compressed in
        the said axis.
        rsd is defined as std/mean.

        Parameters
        ----------
        axis : :class:`str`
            Axis for which to perform the operation.

        Returns
        -------
        :class:`DataV`
            New DataV instance containing the rsd value of axis.

        """

        Array = numpy.std(self.Data, axis=self.Xtable.NameTable[axis]) \
                /numpy.mean(self.Data, axis=self.Xtable.NameTable[axis])

        return DataV(array=Array, Xtable=[x for x in self.Xtable if x != axis], Ytable=self.Ytable)

    def Plot(self, x, y, Normalize=False, Std=None, **kwargs):

        Fig = Plots.Scene2D(UnitSize=(12, 4))

        ax = Plots.Axis(Row=0, Col=0, xLabel=x.Label, yLabel=y.Label, Legend=True, **kwargs)

        Fig.AddAxes(ax)

        if Normalize: 
            y.Normalize()

        if Std is not None:
            Artists = self.PlotSTD(x=x, y=y, Std=Std, **kwargs)
        else:
            Artists = self.PlotNormal(x=x, y=y, **kwargs)

        ax.AddArtist(*Artists)

        return Fig

    def _get_xTable_generator_(self, base_variable):
        Generators = []
        for x in self.Xtable:
            if x in base_variable:
                x.__base_variable__ = True
            x.generator = x.iterate_through_values()
            Generators.append(x.generator)

        return itertools.product(*Generators)

    def PlotNormal(self, x: Table.XParameter, y: Table.XParameter, **kwargs):
        """
        Method plot the multi-dimensional array with the x key as abscissa.
        args and kwargs can be passed as standard input to matplotlib.pyplot.

        Args:
            x: Key of the self dict which represent the abscissa.
            y: Key of the self dict which represent the ordinate.

        """  
        Artist = []
        DiffLabel = y.Legend

        for iteration in self._get_xTable_generator_(base_variable=[x]): 
            CommonLabel = ""
            slicer = []

            for idx, value, common, diff in iteration:
                slicer += [idx]
                CommonLabel += common
                DiffLabel += diff

            data = self.Data[tuple([*slicer, y.Position])]

            Artist.append(Plots.Line(X=x.Values, Y=data, Label=DiffLabel))

        Artist.append(Plots.Text(Text=CommonLabel, Position=[0.9, 0.9], FontSize=8))

        return Artist

    def PlotSTD(self, x, y, Std, **kwargs):
        """
        Method plot the multi-dimensional array with the x key as abscissa.
        args and kwargs can be passed as standard input to matplotlib.pyplot.

        Args:
            x: Key of the self dict which represent the abscissa.
            y: Key of the self dict which represent the ordinate.

        """

        Artist = []
        DiffLabel = y.Legend

        for iteration in self._get_xTable_generator_(base_variable=[x, Std]): 
            CommonLabel = ""
            slicer = []

            for idx, value, common, diff in iteration:
                slicer += [idx]
                CommonLabel += common
                DiffLabel += diff

            Ystd = numpy.std(self.Data, axis=Std.Position, keepdims=True)[tuple([*slicer, y.Position])]
            Ymean = numpy.mean(self.Data, axis=Std.Position, keepdims=True)[tuple([*slicer, y.Position])]

            Artist.append(Plots.STDLine(X=x.Values, YMean=Ymean.squeeze(), YSTD=Ystd.squeeze(), Label=DiffLabel))

        Artist.append(Plots.Text(Text=CommonLabel, Position=[0.9, 0.9], FontSize=8))

        return Artist

    def __str__(self):
        name = [parameter.Name for parameter in self.Ytable]

        text = f'DataVisual array: Variable: {name.__str__()}'

        text += "Parameter" + newLine

        for xParameter in self.Xtable:
            text += f"""| {xParameter.Label:40s}\
            | dimension = {xParameter.Name:30s}\
            | size      = {xParameter.GetSize()}\
            \n"""

        return text
