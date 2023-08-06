from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name = "bendu",
    version = "1.0.2",
    author = "Thodoris Mavroeidakos",
    description = ("A tool automating operations with docker containers"),
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=["bendu"],
    install_requires=['docker', 'click', 'requests'],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    #package_dir={"": "src"},
    #packages=find_packages(where="src"),
    python_requires=">=3.7, <4",
    entry_points='''
        [console_scripts]
        bendu=bendu:bendu
    ''',

    project_urls={
    'Docker Project': 'https://github.com/tmavroeid/bendu',

},
)
