from setuptools import setup, find_packages

setup(
    name="VorteilAmazonPPC",          
    version="0.1.0",
    author="Conor Kelly",
    author_email="your.email@example.com",
    description="An Amazon PPC automation client",
    packages=find_packages(),         
    install_requires=[
        "requests",
        "python-dotenv",
        # add any other required packages here
    ],
    python_requires=">=3.7",
)



