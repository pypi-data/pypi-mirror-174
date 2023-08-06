import setuptools

# Use setuptools.setup to configure the package metadata
setuptools.setup(
    name="discatpy",
    author="EmreTech",
    version="0.0.0-post1",
    description="A high level, asynchronous Discord API wrapper made completely from scratch.",
    #long_description=long_desc,
    #long_description_content_type="text/markdown",
    url="https://github.com/discatpy-dev/library.git",
    project_urls = {
        "Bug Tracker": "https://github.com/discatpy-dev/library/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
        "Framework :: AsyncIO",
        "Framework :: aiohttp",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=["discatpy"],
    python_requires=">=3.9.0",
    #install_requires=requirements,
)
