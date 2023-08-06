from setuptools import setup, find_packages

# * Read the README.md and add as long_description
with open("README.md", "r", encoding="utf-8") as rm:
    long_description = rm.read()

# * Build the setup()
setup(
    name="ldap3-ad-leavers",
    version="0.5.0",
    author="Mervin Hemaraju",
    author_email="th3pl4gu33@gmail.com",
    description="A helper library for offboarding user from AD.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mervinhemaraju/ldap3-ad-leavers",
    packages=find_packages(exclude=['*tests*']),
    install_requires=["ldap3>=2.9.1"],
    test_suite="tests",
    python_requires=">=3.7",
)