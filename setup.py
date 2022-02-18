from setuptools import setup, Extension
from setuptools import find_packages

if __name__ == "__main__":
    setup(
        name="moosync",
        scripts=["script/moosync"],
        version="0.0.1",
        description="GPU scheduling tool.",
        long_description_content_type="text/markdown",
        author="Nitin Rai",
        author_email="mneonizer@gmail.com",
        url="https://github.com/imneonizer/moosync",
        license="MIT License",
        packages=find_packages(),
        include_package_data=True,
        install_requires=["pynvml>=11.4.1"],
        platforms=["linux", "unix"],
        python_requires=">3.5.2",
    )