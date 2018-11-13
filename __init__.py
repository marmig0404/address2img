import setuptools
import support


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='address2img',
     version='1.0.0',
     scripts=[''],
     author="Martin Miglio",
     author_email="marmig0404@gmail.com",
     description="Converts addresses to maps based on open source map data and mapnik",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/marmig0404/address2img",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 2.7",
     ],
 )


def standalone_init():
    # TODO
    pass
    support.write_to_log("Initializing standalone address2img.")


def module_init():
    support.write_to_log("Initializing address2img as a module.")


if __name__ == "__main__":
    standalone_init()
else: # functioning as a module
    module_init()
