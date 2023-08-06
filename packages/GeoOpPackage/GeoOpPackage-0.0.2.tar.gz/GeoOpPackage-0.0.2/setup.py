import setuptools

setuptools.setup(
    name='GeoOpPackage',
    version='0.0.2',
    url="https://github.com/sherinnn/Geometric-Shapes-Package",
    author='Sherin Thomas',
    author_email="tsherin140@gmail.com",
    description='Geometric operations package',
    long_description='This is a python library that includes operations on all 1D, 2D and 3D Geometric shapes',
    license='MIT',
    install_requires=[''],
    #packages=setuptools.find_packages(where="GeoOpPackage"),
    py_modules=["arcLen","centAngle","circArea","circum","coneArea","cubeArea","cuboidArea","cylArea","OneDdistance","polPeri","pyrSurfArea","pyrVol","slope","sphArea","sumInterior","TwoDdistance"],
    package_dir={"": "GeoOpPackage"},
)