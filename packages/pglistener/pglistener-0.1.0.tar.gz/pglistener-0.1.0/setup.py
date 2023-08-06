from distutils.core import setup

setup(
    name='pglistener',
    version="0.1.0",
    packages=['pglistener'],
    package_dir={'': '.'},
    package_data={'': ['libgomodule.so']},
    long_description='demo to show golang python async interop',
    )
