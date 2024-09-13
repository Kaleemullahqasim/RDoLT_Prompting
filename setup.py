from setuptools import setup, find_packages

setup(
    name="novel-prompt-system",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'argparse',
        'importlib',
        'random',
        'json',
        'openai',
    ],
    entry_points={
        'console_scripts': [
            'run-benchmark=benchmarks.run_benchmark:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A novel prompt system for evaluating various LLMs.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/novel-prompt-system",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
