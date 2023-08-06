import setuptools

# Use setuptools.setup to configure the package metadata
setuptools.setup(
    name="discatcore",
    author="EmreTech",
    version="0.0.0",
    description="A lower level Discord API wrapper that functions as the core layer of DisCatPy.",
    #long_description=long_desc,
    #long_description_content_type="text/markdown",
    url="https://github.com/discatpy-dev/core.git",
    project_urls = {
        "Bug Tracker": "https://github.com/discatpy-dev/core/issues",
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
    packages=["discatcore"],
    python_requires=">=3.9.0",
    #install_requires=requirements,
)
