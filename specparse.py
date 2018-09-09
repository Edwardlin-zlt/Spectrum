import re
import os
import pandas as pd
from collections import OrderedDict
import colour
import colour.plotting

def get_spec(filepath, start=380, end=780):
    """
    将仪器导出的数据转换成纯粹的光谱数据
    :filepath (str)
    :start(int) 开始的波长
    :end (int) 结束的波长取值
    :re (OrderedDict) spec_data OrderedDict from 350 to 1000 
    """
    formmer = "(.*mfp=\")(.*)(\".*)"

    with open(filepath) as f:
        data = ' '.join(f.readlines())
        data2 = re.match(formmer, data)
        data_zip = list(zip(range(350, 1001),map(float,data2.group(2).split(','))))
        for x in data_zip:
            if x[0] == start:
                start_index = data_zip.index(x)
            elif x[0] == end:
                end_index = data_zip.index(x)
        data_OrderedDict = OrderedDict(data_zip[start_index:end_index+1])
        return data_OrderedDict 

def get_specs(dirpath):
    """
    将目标文件夹所有的仪器导出数据转换成纯粹的光谱数据
    :dirpath (str)
    ::re (OrderedDict)
    """
    files = [x for x in os.listdir(dirpath) if os.path.splitext(x)[1]=='.sp']
    for f in files:
        yield get_spec('%s/%s' % (dirpath, f))

def out_csv(spec_data, csv_name):
    """将光谱数据字符串导出成csv表格，默认波长范围为380到780
    ::spec_data: (OrderedDict) 
    ::re(None)
    """
    value_list = list(spec_data.values())
    start = min(spec_data.keys())
    end = max(spec_data.keys())
    df = pd.DataFrame({'values':value_list}, index=range(start, end+1))
    df.to_csv(csv_name)

def single_spd_plotting(spec_data, spec_name='Sample'):
    """画出文件的光谱分布图
    ::spec_data (data_OrderedDict): 光谱数据
    ::spec_name: (str) 图名
    """
    spd = colour.SpectralPowerDistribution(spec_data, name=spec_name)
    colour.plotting.single_spd_plot(spd)
    
if __name__ == "__main__":
    """get_spec测试
    pathname = 'spectral/red1_2018_09_05_19_44_52.sp'
    pure_spec = get_spec(pathname)
    print(pure_spec)    
    """
    """单个out_csv测试
    pathname = 'spectral/red1_2018_09_05_19_44_52.sp'
    pure_spec = get_spec(pathname)
    out_csv(pure_spec,'test.csv')
    """
    """get_specs test
    dirpath = 'spectral'
    for spec in get_specs(dirpath):
        print('\n',spec,'\n')
    """
    """测试single_spd_plotting
    pathname = 'spectral/red1_2018_09_05_19_44_52.sp'
    single_spd_plotting(pathname, spec_name="Red1")
    """
    pathname = 'spectral/red1_2018_09_05_19_44_52.sp'
    single_spd_plotting(pathname, spec_name="Red1")

