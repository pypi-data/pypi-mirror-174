import distutils.util
from setuptools import setup, find_packages
# print(['<sys>', '<psutil>', ['win32gui'] if platform == 'win32' else ['<re>', '<subprocess>']])
print(distutils.util.get_platform())
setup(name='activewindow',
      version='0.2.2',
      author='Sonter',
      author_email='sonterkub@gmail.com',
      description='Active window information',
      long_description='Gives you information about active window in Windows / X11',
      packages=['activewindow'],
      install_requires=['setuptools',
                        'sys',
                        'psutil',
                        "win32gui;platform_system=='Windows'",
                        "win32gui;platform_system=='win-amd64'",
                        "re;platform_system=='linux-x86_64'",
                        "subprocess;platform_system=='linux-x86_64'"],
      keywords=['active window', 'activewindow', 'x11'],
      zip_safe=False,
      platforms=['linux-x86_64', 'win-amd64'],
      classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX :: Linux"
      ])
# py_modules=['win32gui', 'psutil', 'ctypes'],