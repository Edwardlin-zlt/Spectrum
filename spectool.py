#!usr/bin/env python

"""
为了处理光谱信息开发的小程序

Author: Edward
Email: Edwardlin.zlt@gmail.com
"""
import re
from keys import keys
from collections import OrderedDict

class Spectrum(object):
    """
    导入仪器数据，将其数据定义成一个光谱对象，主要属性有`data`和`spec_dict`
    """
    

    def __init__(self,filepath):
        """
        ::filepath (str): 仪器文件路径
        ::self.__data (dict): 包含亮度，色度坐标等信息的字典
        ::self.__spec_dict: SPD数据，默认为380-780之间的数据
        """
        self.__data, self.spec_dict = get_spec(filepath)
    
    
    def get(self, attr):
        return self.__data.get(attr)
    
    def __str__(self):
        return str(self.__data)


def get_spec(filepath, start=380, end=780):
    """
    将仪器导出的数据转换成纯粹的光谱数据
    :filepath (str)
    :start(int) 开始的波长
    :end (int) 结束的波长取值
    :re (OrderedDict) spec_data OrderedDict from 350 to 1000
    """
    former = r'(.*data=")([,\.\d-]*)(".*mfp=")(.*)(" \/>)'

    with open(filepath) as f:
        raw_data = f.read() 
        matched = re.match(former, raw_data)
        data = list(map(float,matched.group(2).split(',')))
        data = dict(zip(keys, data))

        raw_spec = list(zip(range(350, 1001),map(float,matched.group(4).split(','))))
        for x in raw_spec:
            if x[0] == start:
                start_index = raw_spec.index(x)
            elif x[0] == end:
                end_index = raw_spec.index(x)
        spec_dict= OrderedDict(raw_spec[start_index:end_index+1])
        return (data, spec_dict) 


pathname = 'spectral/red1_2018_09_05_19_44_52.sp'
red1 = Spectrum(pathname)

