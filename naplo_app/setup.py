from setuptools import setup

setup(
    name="NaplozoApp",
    version="1.0",
    packages=["naplo_app"],
    install_requires=[
        "streamlit",
        "pandas",
        "plotly",
    ],
    entry_points={
        "console_scripts": [
            "naplo_app=naplo_app.main:main",
        ],
    },
)
