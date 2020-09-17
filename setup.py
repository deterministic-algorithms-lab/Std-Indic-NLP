from setuptools import setup
import os

pkg_lis = ['std_indic','std_indic.NMT']
script_lis = []

for pkg in pkg_lis[1:]:
    root = os.path.join(pkg.replace('.','/'), 'datasets')
    for f in os.listdir(root):
        if os.path.isfile(f) and f.endswith('.py'):
            script_lis.append(f)

pkg_data = {}
for pkg in pkg_lis[1:]:
    pkg_data[pkg]=[os.path.join(pkg.replace('.', '/'), 'README.md'), os.path.join(pkg.replace('.', '/'), 'CONTRIBUTING.md')]

setup(name='std_indic',
      version='0.0',
      packages=pkg_lis,
      scripts=script_lis,
      package_data=pkg_data)