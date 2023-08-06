from setuptools import setup, find_packages

setup(
    name="collect4easyplot",
    version="0.14",
    description="A complementary library for using EasyPlot with Python",
    author="Guy Raichelgauz",
    author_email="guy.raichelgauz@gmail.com",
    url="https://github.com/RaichelgauzGuy/Collect4EasyPlot",
    packages=find_packages(),
    include_package_data=True,
    long_description="Use the collect method to grab data of any type to store it. After collecting, the data will "
                     "automatically appear in EasyPlot",
    long_description_content_type="text/markdown",
    exclude_package_data={'': ['.gitignore']},
    setup_requires=['setuptools-git'],
    install_requires=[
    ]
)
