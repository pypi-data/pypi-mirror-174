from setuptools import setup, find_packages

VERSION = '0.0.0.0.2'
DESCRIPTION = 'cipetpet cicikus'
LONG_DESCRIPTION = """
            cibili cibili cibili şak şak şak şak şak
            cibili? cibili cibili şak şak şak şak şak
            hadi yavrum bi daha vur
            şak şak şak şak şak
            bunlar lezzetli. bi de şimdi;
            ciriling ciriling prrrr ciyak ciyak ciyak ciyak
            bijining bijining aniyeeaaaa zrrrrrr
            bunlar kuş değil, ötüyo, amatörü eğlendirir.
            """
# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="cipetpet",
        author="tayyip.osman",
        author_email="toaydiner@armagroupholding.com",
        version= VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that
        # needs to be installed along with your package. Eg: 'caer'
        keywords=['python', 'cipetpet','cici kus cici kus'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)