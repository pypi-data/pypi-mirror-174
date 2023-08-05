from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="qa-e-nsi",
    version="1.0.0b1",
    description="Assurance qualité sur e-nsi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://forge.aeif.fr/e-nsi/outils",
    author="Vincent-Xavier Jumel",
    author_email="vincent-xavier.jumel@ac-paris.fr",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Education",
        "Topic :: Education :: Testing",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7, <4",
    install_requires=[],
    entry_points={  # Optional
        "console_scripts": [
            "verifier_sujet=verifier_sujet:main",
        ],
    },
    project_urls={  # Optional
        "Bug Reports": "https://forge.aeif.fr/e-nsi/outils/-/issues",
        "Source": "https://forge.aeif.fr/e-nsi/outils/",
    },
)
