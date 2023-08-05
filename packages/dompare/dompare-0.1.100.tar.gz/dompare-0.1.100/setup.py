from setuptools import setup, find_packages


readme = open('README.md').read()

setup(
    name="dompare",
    version="0.1.100",
    keywords=("dompare", "Linux", "diff", "directories"),
    description="A program to diff two directories recursively",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="MIT Licence",
    url="https://github.com/vra/dompare",
    author="Yunfeng Wang",
    author_email="wyf.brz@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        "binaryornot>=0.4.4",
        "coloredlogs>=10.0",
    ],
    scripts=[],
    entry_points={"console_scripts": ["dompare=dompare.__init__:main"]},
)
