from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="BlaiseKnapsack",
    version="0.0.1",
    description="Greedy Algorithm for the knapsack problem",
    py_modules=["BlaiseKnapsack"],
    package_dir={'': "src"},
    url= "https://github.com/Blaise143/Knapsack-Optimization",
    author = "Blaise Appolinary",
    author_email = "blaiseappol@gmail.com"
)