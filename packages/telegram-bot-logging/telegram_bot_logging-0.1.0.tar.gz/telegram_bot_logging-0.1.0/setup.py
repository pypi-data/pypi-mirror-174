from setuptools import find_packages, setup
setup(
    name='telegram_bot_logging',
    packages=find_packages(include=['telelogging']),
    version='0.1.0',
    description='My first Python library',
    author='Me',
    license='MIT',
    setup_requires=['requests==2.28.1', 'pymongo==4.3.2'],
)
