import re
import os
import pandas

def get_spec(filepath):
    """
    将仪器导出的数据转换成纯粹的光谱数据
    :filepath (str)
    :re (str)
    """
    formmer = "(.*mfp=\")(.*)(\".*)"

    with open(filepath) as f:
        data = ' '.join(f.readlines())
        data2 = re.match(formmer, data)
        i = 0
        for j in data2.group(2).split(','):
            i += 1
            print(i, ':', j)
        return data2.group(2)

def get_specs(dirpath):
    """
    将目标文件夹所有的仪器导出数据转换成纯粹的光谱数据
    :dirpath (str)
    """
    files = [x for x in os.listdir(dirpath) if os.path.splitext(x)[1]=='.sp']
    for f in files:
        get_spec(f)


if __name__ == "__main__":
    pathname = 'spectral/red1_2018_09_05_19_44_52.sp'
    pure_spec = get_spec(pathname)
