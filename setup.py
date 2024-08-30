from setuptools import setup, find_packages

setup(
    name="przXCLI",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'tm=taskManager.taskManager:main'
        ]
    }
)