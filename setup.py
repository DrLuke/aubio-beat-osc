from setuptools import setup, find_packages

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="aubio-beat-osc",
    version="1.3",
    py_modules=["aubio_beat_osc"],
    install_requires=[
        "pyaudio",
        "aubio",
        "python-osc",
        "numpy"
    ],

    author="Lukas Jackowski",
    description="Simple beat detection outputting to OSC servers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="aubio beat detection osc",

    project_urls={
        "Source Code": "https://github.com/DrLuke/aubio-beat-osc",
    },

    entry_points={
        "console_scripts": [
            "aubio-beat-osc=aubio_beat_osc:main",
        ]
    }
)
