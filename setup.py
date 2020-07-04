"""
Setup file for packaging Product aggregator
"""

# std

# third-party
import setuptools

# local
from product_aggregator import __version__


def setup():
    """Run setuptools setup"""
    setuptools.setup(
        name="product_aggregator",
        version=__version__,
        description=(
            "An excercise given to OndraK by Anna Marie Rybáčková. "
            "Did she want to spoil my weekend?"
        ),
        author="OndraK",
        author_email="ondrej.kajinek@tutamail.com",
        url="https://github.com/ondrejkajinek/applifting_exercise",
        packages=setuptools.find_packages(exclude=["test", "venv"])
    )


if __name__ == '__main__':
    setup()
