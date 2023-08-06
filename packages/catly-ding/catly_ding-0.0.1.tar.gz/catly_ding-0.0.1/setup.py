import os
import shutil
import requests
import setuptools



# version = requests.get("https://pypi.org/pypi/catly-ding/json").json()["info"]["version"]
version = "0.0.0"
v0, v1, v2 = map(int, version.split("."))
if v2 < 10:
    v2 += 1
else:
    v1 += 1
    v2 = 0
if v1 > 10:
    v0 += 1
    v1 = 0
version = ".".join(map(str, [v0, v1, v2]))

with open("src/catly_ding/__version.py", "w+") as file:
    file.write(f'version = "{version}"')

with open("requirements.txt", encoding="UTF-8") as file:
    install_requires = [i.rstrip("\n") for i in file.readlines()]
    

if os.path.exists("build"):
    shutil.rmtree("build")
if os.path.exists("dist"):
    shutil.rmtree("dist")
setuptools.setup(
    name="catly_ding",
    version=version,
    author="Tunglies",
    author_email="Tunglies@outlook.com",
    description="Simple & Easy Way For Ding Talk Robot Sending Message",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Tunglies/catly_ding",
    package_dir={"":"src"},
    packages=setuptools.find_packages(where="src"),
    package_data={
        "": ["*.js"]
    },
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    install_requires=install_requires,
    keywords=["dingtalk", "robot"]
) 