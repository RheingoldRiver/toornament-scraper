import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="toornament_scraper",
    version="0.0.2",
    author=" SeanDrum",
    author_email="",
    description="Toornament scraper for Leaguepedia MENA coverage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SeanDrum/toornament-scraper",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=['beautifulsoup4', 'mwparserfromhell']  # im lazy sorry
)
