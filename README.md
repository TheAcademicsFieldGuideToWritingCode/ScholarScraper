# ScholarScraper
A Google Scholar paper scraper



To turn your script into a Python package and distribute it through PyPI, follow these steps:

1. **Organize your code into a package structure**: Create a directory for your package, and move your scripts into this directory. For example, if your package is called `scholarly_analysis`, create a directory with that name and move your `main.py` and `gpt_analysis.py` files into it. Also, create an empty `__init__.py` file inside the `scholarly_analysis` directory. This file indicates that the directory is a Python package.

```
scholarly_analysis/
    __init__.py
    main.py
    gpt_analysis.py
```

2. **Create a setup.py file**: In your project's root directory, create a `setup.py` file to specify your package's metadata and dependencies. Here's an example `setup.py` file:

```python
from setuptools import setup, find_packages

setup(
    name="scholarly-analysis",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "openai",
        "scholarly",
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "scholarly-analysis = scholarly_analysis.main:main",
        ],
    },
    author="Your Name",
    description="A tool to collect and analyze scholarly papers using Google Scholar and OpenAI GPT-3",
    license="MIT",
)
```

3. **Create a README file**: Write a README.md file to provide documentation and usage instructions for your package.

4. **Create a .gitignore file**: Create a `.gitignore` file to exclude files and directories that should not be tracked by Git. Some examples of what to exclude are `__pycache__`, virtual environments, and any generated files.

5. **Initialize a Git repository**: In your project's root directory, run `git init` to initialize a Git repository. Commit your code with `git add .` and `git commit -m "Initial commit"`.

6. **Create an account on PyPI**: If you haven't already, create an account on [PyPI](https://pypi.org/) and [Test PyPI](https://test.pypi.org/).

7. **Install required tools**: Install the `setuptools`, `wheel`, and `twine` packages, which are needed for packaging and uploading your package:

```
pip install setuptools wheel twine
```

8. **Build your package**: In your project's root directory, run the following command to build your package:

```
python setup.py sdist bdist_wheel
```

This will create a `dist` directory containing the source distribution and the wheel distribution of your package.

9. **Upload your package**: Use `twine` to upload your package to Test PyPI (or PyPI) as follows:

```
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

Replace `https://test.pypi.org/legacy/` with `https://upload.pypi.org/legacy/` when you're ready to upload to the main PyPI repository.

10. **Install and test your package**: You can now install and test your package using `pip`. For Test PyPI, use the following command:

```
pip install --index-url https://test.pypi.org/simple/ scholarly-analysis
```

For the main PyPI repository, simply run:

```
pip install scholarly-analysis
```

That's it! Your package is now available on PyPI for others to install and use. Remember to update your package version in `setup.py` when you make changes and want to release a new version.