from setuptools import setup, find_packages
setup(name='activewindow',
      version='0.0.1',
      author='Sonter',
      author_email='sonterkub@gmail.com',
      description='Active window information',
      long_description='Gives you information about active window in Windows / X11',
      py_modules=['win32gui', 'psutil', 'ctypes'],
      keywords=['active window', 'activewindow', 'x11'],
      zip_safe=False,
      platforms=['win', 'win32'],
      classifiers=[
          "Programming Language :: Python :: 3",
          "Operating System :: Microsoft :: Windows",
      ])
