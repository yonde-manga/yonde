import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yonde",
    version="0.1",
    author="yanhuishi",
    author_email="contatoyonde@protonmail.com",
    description="Mangá downloader (para leitura offline) voltado para sites e scans brasileiros.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yonde-manga/yonde",
    project_urls={
        "Bug Tracker": "https://github.com/yonde-manga/yonde/issues",
    },
    entry_points={
        'console_scripts': [
            'yonde = yonde.__main__:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests',
        'cloudscraper',
        'pillow',
        'lxml',
        'natsort'
    ],
    python_requires=">=3.7",
)
