# -*- coding: utf-8 -*-

import importlib
from muswmm.errors import *

class _Namedobjs():
    
    def __init__(self, project, namedobjs, namedobj_type):
        self._prj = project
        self._objs = namedobjs
        self._cur_index = 0
        self._count = self._objs.Count
        self.obj_type = namedobj_type
        
    def __len__(self):
        return self._objs.Count
    
    def __contains__(self, name):
        if self._objs.GetItem_1(name) is None:
            return False
        else:
            return True
    
    def __getitem__(self, key):
        if isinstance(key, int):
            if key < 0 or key > self._count:
                return None
        elif isinstance(key, str):
            if self._objs.GetItem_1(key) is None:
                return None
        module = importlib.import_module('muswmm.namedobject')
        obj_class = getattr(module, self.obj_type)
        return obj_class(self._prj, key)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._cur_index < self._count:
            obj = self.__getitem__(self._cur_index)
            self._cur_index += 1
            return obj
        else:
            raise StopIteration()
            
    @property
    def _name(self):
        return self._objs.GetItem(self._cur_index).Name
    
    def clear(self):
        self._objs.RemoveAll()


class RainGages(_Namedobjs):
    
    def __init__(self, project):
        super().__init__(project, project._prj.RainGages, 'RainGage')


class Subcatchments(_Namedobjs):
    
    def __init__(self, project):
        super().__init__(project, project._prj.Subcatchments, 'Subcatchment')

class Junctions(_Namedobjs):
    
    def __init__(self, project):
        super().__init__(project, project._prj.Junctions, 'Junction')
        
class Outfalls(_Namedobjs):
    
    def __init__(self, project):
        super().__init__(project, project._prj.Outfalls, 'Outfall')
        
class Storages(_Namedobjs):
    
    def __init__(self, project):
        super().__init__(project, project._prj.Storages, 'Storage')
        
class Dividers(_Namedobjs):
    
    def __init__(self, project):
        super().__init__(project, project._prj.Dividers, 'Divider')
        
class Conduits(_Namedobjs):
    
    def __init__(self, project):
        super().__init__(project, project._prj.Conduits, 'Conduit')
        
class Pumps(_Namedobjs):
    
    def __init__(self, project):
        super().__init__(project, project._prj.Pumps, 'Pump')
        
class Orifices(_Namedobjs):
    
    def __init__(self, project):
        super().__init__(project, project._prj.Orifices, 'Orifice')
        
class Weirs(_Namedobjs):
    
    def __init__(self, project):
        super().__init__(project, project._prj.Orifices, 'Weir')
        
class Outlets(_Namedobjs):
    
    def __init__(self, project):
        super().__init__(project, project._prj.Outlets, 'Outlet')
        
class TimeSeries(_Namedobjs):
    
    def __init__(self, project):
        super().__init__(project, project._prj.TimeSeries, 'TimeSerie')

class Pollutants(_Namedobjs):

    def __init__(self, project):
        super().__init__(project, project._prj.Pollutants, 'Pollutant')

class Landuses(_Namedobjs):

    def __init__(self, project):
        super().__init__(project, project._prj.Landuses, 'Landuse')