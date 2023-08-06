from setuptools import setup, find_packages
import json
import pathlib


HERE = pathlib.Path(__file__).parent.resolve()

def locked_requirements(section):
    """Look through the 'Pipfile.lock' to fetch requirements by section."""
    with open('Pipfile.lock') as pip_file:
        pipfile_json = json.load(pip_file)

    if section not in pipfile_json:
        print(f"{section} section missing from Pipfile.lock")
        return []

    return [package + detail.get('version', "") for package, detail in pipfile_json[section].items()]


setup(
    name="astana_hub",
    version="0.0.1",

    description="Get Networking cards from https://astanahub.com/ with ease!",
    long_description=(HERE / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",

    url="https://github.com/vladzen13/astana_hub",

    author="Vladislav Zenin",
    author_email="vladzen13@yandex.ru",

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],

    # keywords="sample, setuptools, development",  # Optional

    # package_dir={"": "astana_hub"},

    packages=find_packages(),

    python_requires=">=3.9, <4",
    install_requires=locked_requirements('default'),
    extras_require={
        "dev": locked_requirements('develop'),
    },

    # tests_require=['pytest'],   ????????????? from pinnacle/ is it valid ?

    # package_data={  # Optional
    #     "sample": ["package_data.dat"],
    # },

    # data_files=[("my_data", ["data/data_file"])],  # Optional

    # entry_points={  # Optional
    #     "console_scripts": [
    #         "sample=sample:main",
    #     ],
    # },

    project_urls={
        "Bug Reports": "https://github.com/vladzen13/astana_hub/issues",
        "Source": "https://github.com/vladzen13/astana_hub/",
        # "Funding": "https://donate.pypi.org",
        # "Say Thanks!": "http://saythanks.io/to/example",
    },
)
