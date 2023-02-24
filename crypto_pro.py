import sys

from os.path import dirname, abspath
p = dirname(abspath(__file__)) + '\\pycades'
sys.path.append(p)
print(sys.path)
import pycades


print(pycades.ModuleVersion())