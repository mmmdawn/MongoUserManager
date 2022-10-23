import sys
import setuptools

# try:
#     import mymongo
# except ImportError:
#     print("error: pywal requires Python 3.8 or greater.")
#     sys.exit(1)

setuptools.setup(
    name="mymongo",
    version="0.0.1",
    author="Dawn",
    author_email="congminh292k@gmail.com",
    description="MongoDB utilities",
    keywords="mongodb user-management mongodb-role",
    license="GNU",
    url="https://github.com/mmmdawn/MongoUserManager",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Topic :: Database"
    ],
    packages=["mymongo"],
    entry_points={"console_scripts": ["mymongo=mymongo.__main__:main"]},
    python_requires=">=3.8"
)
