import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="yourtools",
    version="0.2.1",
    author="zfang",
    author_email="founder517518@163.com",
    description="Python helper tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/yourtools/",
    packages=setuptools.find_packages(),
    data_files=["requirements.txt"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    # install_requires=required,
    install_requires=[
        "aniso8601==9.0.1"
        "bcrypt==4.0.1"
        "certifi==2022.9.24"
        "cffi==1.15.1"
        "chardet==3.0.4"
        "cheroot==8.6.0"
        "click==8.1.3"
        "configtools==0.3.3"
        "cryptography==37.0.2"
        "DBUtils==1.3"
        "distlib==0.3.6"
        "filelock==3.8.0"
        "Flask==1.1.2"
        "Flask-Cors==3.0.10"
        "Flask-RESTful==0.3.8"
        "gunicorn==20.0.4"
        "idna==2.10"
        "itsdangerous==1.1.0"
        "jaraco.functools==3.0.1"
        "Jinja2==2.11.2"
        "logconfig==0.4.0"
        "logutils==0.3.5"
        "MarkupSafe==1.1.1"
        "more-itertools==8.6.0"
        "paramiko==2.11.0"
        "platformdirs==2.5.2"
        "psutil==5.9.1"
        "pycparser==2.21"
        "PyMySQL==0.10.1"
        "PyNaCl==1.5.0"
        "pytz==2020.4"
        "PyYAML==5.3.1"
        "redis==3.5.3"
        "requests==2.25.0"
        "simplejson==3.17.2"
        "six==1.15.0"
        "sshtunnel==0.4.0"
        "urllib3==1.26.2"
        "virtualenv==20.16.5"
        "web.py==0.62"
        "Werkzeug==1.0.1"
    ]
)
