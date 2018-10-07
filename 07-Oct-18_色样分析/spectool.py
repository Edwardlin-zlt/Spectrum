#!usr/bin/env python

"""
为了处理光谱信息开发的小程序

Author: Edward
Email: Edwardlin.zlt@gmail.com
"""

# import modules----------------------------------------
import re
import os

import pandas as pd
import numpy as np
import colour
import colour.plotting as cpt
import pylab

from keys import keys
# import modules done-------------------------------------

class Spectrum(object):
    """
    导入仪器数据，将其数据定义成一个光谱对象，主要属性有`data`和`spec_dict`
    """

    def __init__(self,filepath, name):
        """
        ::filepath (str): 仪器文件绝对路径
        ::self.__data (dict): 包含亮度，色度坐标等信息的字典
        ::self.__spec_dict: SPD数据，默认为380-780之间的数据
        """
        # 文件路径，绝对路径最好
        self.filepath = filepath
        self.name = name 
        self._data, self.spec_dict = self.get_spec()
        self.x = self._data['x']
        self.y = self._data['y']
        self.xy_measure = np.array([self._data['x'],self._data['y']], dtype='float64')
        self.spd = self.to_spd()
        self.XYZ = self.spd_to_XYZ()

    def __str__(self):
        return (self.name, str(self._data))

    def __repr__(self):
        return self.name
    
    # 解析仪器测试出的sp文件
    def get_spec(self, start=380, end=780):
        """
        将仪器导出的数据转换成纯粹的光谱数据
        :filepath (str)
        :start(int) 开始的波长
        :end (int) 结束的波长取值
        :re (tuple of spec_data_info and 光谱能量分布) 光谱信息和380-780之间的光谱能量分布
        """
        former = r'(.*data=")([,\.\dE-]*)(".*mfp=")(.*)(" \/>)'
    
        with open(self.filepath) as f:
            # data是从原sp文件的提取出来的亮度等数据信息，可以查看`keys`模块了解有哪些信息
            raw_data = f.read() 
            matched = re.match(former, raw_data)
            data = list(map(float,matched.group(2).split(',')))
            data = dict(zip(keys, data))
    
            #提取指定区间的光谱
            raw_spec = list(zip(range(350, 1001),map(float,matched.group(4).split(','))))
            for x in raw_spec:
                if x[0] == start:
                    start_index = raw_spec.index(x)
                elif x[0] == end:
                    end_index = raw_spec.index(x)
            spec_dict= dict(raw_spec[start_index:end_index+1])
            return (data, spec_dict) 
    
    # 将一般的光谱字典`spec_dict`变成`colour`模块的光谱对象
    def to_spd(self):
        self.spd = colour.SpectralPowerDistribution(self.spec_dict, name=self.name)
        return self.spd

    #用于取得data中的某一项值，如亮度
    def get(self, attr):
        return self._data.get(attr,0)
    

    # 相关属性计算换算

    ## 计算涉及的标准常量
    cmfs = colour.STANDARD_OBSERVERS_CMFS['CIE 1931 2 Degree Standard Observer']
    illuminant = colour.ILLUMINANTS_RELATIVE_SPDS['D65']
    #print(cmfs, '\n', illuminant)
    
    ## 从光谱能量分布到三刺激值
    def spd_to_XYZ(self, cmfs=cmfs, illuminant=illuminant):
        XYZ = colour.spectral_to_XYZ(self.spd, cmfs, illuminant)
        return XYZ
    
    ## 从三刺激值转换到xy值
    def XYZ_to_xy(self):
        return colour.XYZ_to_xy(self.XYZ)

    # 画出自己的图TODO
    ## 画出自己的光谱分布图
    def spd_plot(self):
        cpt.single_spd_plot(self.spd)

    ## 画出SPD图


def sps_to_one_csv(dirpath):
    """
    将一个文件夹内所有的光谱文件信息放在一个表格里
    :: dirpath(str): 目标文件夹
    :: re(None): 在当前目录导出一个csv文件
    """
    columns = keys.copy()
    columns.insert(0, 'name')
    df = pd.DataFrame(None, columns= columns)
    i = 0
    files = [x for x in os.listdir(dirpath) if os.path.splitext(x)[1] == '.sp']
    print(files)
    for f in files:
        print("i: ", i)
        print("f: ", f)
        temp_spec = Spectrum(os.path.join(dirpath,f))
        incre_info = [temp_spec.get(x) for x in keys]
        incre_info.insert(0, f.split('_')[0])
        print(list(zip(columns, incre_info)))
        df.loc[i] = incre_info
        i += 1
    df.to_csv(os.path.join(dirpath, 'all.csv'))

#TODO传入多个光谱数据，将他们画在同一张 CIE1931图上
def spcs_in_one_diagram(*specs):
    """传入多个光谱数据，将他们画在同一张 CIE1931图上
    :: specs (instances of spectrum class): 该程序定义的类的实例
    :: re: None
    """
    num = len(specs)
    x = []
    y = []
    for spec in specs:
        x.append(spec.x)
        y.append(spec.y)
    cpt.chromaticity_diagram_plot_CIE1931(standalone=False)
    pylab.plot(x, y, 'o', color='k', mew=1, mec='k', alpha=0.5)
    # displaying the plot
    cpt.render(
            standalong=True,
            limits=(-0.1, 0.9, -0.1, 0.9),
            x_tighten=True,
            y_tighten=True)



if __name__ == "__main__":
    #dirname = './spectral'
    #sps_to_one_csv(dirname)
    specs = [Spectrum(os.path.join('/home/edward/Documents/Major/spectral', x)) for x in os.listdir('/home/edward/Documents/Major/spectral') if os.path.splitext(x)[1] == '.sp']
    
    spcs_in_one_diagram(*specs)

