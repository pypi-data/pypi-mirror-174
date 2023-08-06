#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from dataclasses import dataclass
from itertools import product

from MPSPlots.Utils import ToList, UnitArray


@dataclass
class XParameter(object):
    Name: str = None
    Values: str = None
    Format: str = ""
    LongLabel: str = ""
    Unit: str = ""
    Legend: str = ""
    Type: type = float
    Position: int = None

    def __post_init__(self):
        self.Values = ToList(self.Values).astype(self.Type) if self.Type is not None else ToList(self.Values)

        self.Values = self.Values

        self.Init()
        self.__base_variable__ = False

    def SetValues(self, Values):
        self.Values = Values

    def Init(self):
        self.Label = self.LongLabel + f" [{self.Unit}]" if self.LongLabel != "" else self.Name
        self.Legend = self.Legend if self.Legend != "" else self.Name

    @property
    def has_unique_value(self):
        if self.Values.shape[0] == 1:
            return True
        else:
            return False

    def Normalize(self):
        self.Unit = "[U.A.]"
        self.Init()

    def __getitem__(self, item):
        return self.Values[item]

    def __repr__(self):
        return self.Name

    def GetSize(self):
        return self.Values.shape[0]

    def __eq__(self, other):
        if other is None: 
            return False

        return True if self.Name == other.Name else False

    def iterate_through_values(self):
        if self.__base_variable__:
            yield slice(None), None, "", ""

        else:
            for n, value in enumerate(self.Values):
                if self.has_unique_value:
                    CommonLabel = f" | {self.LongLabel} : {value:{self.Format}}"
                    DiffLabel = ""
                else:
                    CommonLabel = ""
                    DiffLabel = f" | {self.LongLabel} : {value:{self.Format}}"

                yield n, value, CommonLabel, DiffLabel


@dataclass
class XTable(object):
    X: numpy.array

    def __post_init__(self):

        self.X = numpy.array(self.X)
        self.Shape = [x.GetSize() for x in self.X]
        self.Name2Idx = {x.Name: order for order, x in enumerate(self.X)}

        self.CommonParameter = []
        self.DiffParameter = []

        for x in self:
            if x.Values.size == 1:
                self.CommonParameter.append(x)
            else:
                self.DiffParameter.append(x)

    def GetValues(self, Axis):
        return self[Axis].Value

    def GetPosition(self, Value):
        for order, x in enumerate(self.X):
            if x == Value:
                return order

    def __getitem__(self, Val):
        if Val is None: 
            return None

        Idx = self.Name2Idx[Val] if isinstance(Val, str) else Val

        return self.X[Idx]



class YTable(object):
    def __init__(self, Y):
        self.Y = Y
        self.Name2Idx = self.GetName2Idx()

        for n, y in enumerate(self.Y):
            y.Position = n

    def GetShape(self):
        return [x.Size for x in self.Y] + [1]

    def GetName2Idx(self):
        return {x.Name: order for order, x in enumerate(self.Y)}

    def __getitem__(self, Val):
        if isinstance(Val, str):
            idx = self.Name2Idx[Val]
            return self.Y[idx]
        else:
            return self.Y[Val]

# -
