import solar_system,sys,os
from setuptools import setup

try:os.chdir(os.path.split(__file__)[0])
except:pass

desc="""Solar system gravity simulation using Python turtle graphics and physical algorithm. \
使用turtle模块及物理算法的天体引力模拟程序。"""

try:
    with open("README.rst") as f:
        long_desc=f.read()
except OSError:
    long_desc=''

setup(
    name='solar-system',
    version="1.3.2.1",
    py_modules=['solar_system'],
)
