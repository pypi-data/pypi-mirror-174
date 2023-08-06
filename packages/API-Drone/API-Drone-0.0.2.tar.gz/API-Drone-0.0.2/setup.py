from setuptools import setup, find_packages


VERSION = '0.0.2'
DESCRIPTION = 'PyMAVLink drone control via simple functions'

# Setting up
setup(
    name="API-Drone",
    version=VERSION,
    author="Joel Johera I Izquierdo",
    author_email="joel.johera.i@estudiantat.upc.edu",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pymavlink'],
    keywords=['pymavlink', 'ArduPilot'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
