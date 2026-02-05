from setuptools import setup, find_packages

setup(
    name="nearfix",
    version="1.0.0",
    description="NearFix - All-in-One Local Service Booking System",
    author="NearFix Team",
    author_email="contact@nearfix.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask==2.3.3",
        "Flask-MySQLdb==2.0.0",
        "Werkzeug==2.3.7",
        "mysqlclient==2.2.0",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
