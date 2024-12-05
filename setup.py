from setuptools import setup, find_packages

setup(
    name="mastermind", 
    version="0.1.0", 
    description="A MasterMind game implemented in Python",  
    author="Wilson Huang",  # Your name
    author_email="your.email@example.com",  
    packages=find_packages(where="src"), 
    package_dir={"": "src"}, 
    include_package_data=True, 
    install_requires=[
        # List your dependencies here (e.g., `requests`, `numpy`)
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  
)