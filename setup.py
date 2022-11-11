import setuptools

setuptools.setup(
    name="mongo-user-manager",
    version="0.0.2",
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
    dependencies=[
        "inquirerpy ~= 0.3.4",
        "pymongo ~= 4.3.2",
    ],
    packages=["mymongo", "mymongo.database", "mymongo.utils"],
    entry_points={"console_scripts": ["mun=mymongo.__main__:main"]},
    python_requires=">=3.8",
)
