from setuptools import setup, find_packages
setup(name='activewindow',
      version='0.0.3',
      author='Sonter',
      author_email='sonterkub@gmail.com',
      description='Active window information',
      long_description='Gives you information about active window in Windows / X11',
      packages=find_packages(),
      keywords=['active window', 'activewindow', 'x11'],
      zip_safe=False,
      classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX :: Linux"
      ])
# py_modules=['win32gui', 'psutil', 'ctypes'],