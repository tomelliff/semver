# SemVer

Basic Python script for incrementing a project's version.

## Usage

Ideally this would be used by some build tool like a Gradle plugin but for now just copy the script into your repo and optionally create a `version.py` file with an initial version.

Then when you are ready to create a release run the script to increment the version number of the project.

## Tests

Run the tests with:

```sh
nosetests
```

or

```sh
python -m unittest discover -b
```
