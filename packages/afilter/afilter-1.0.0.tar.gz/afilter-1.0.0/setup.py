from setuptools import find_packages, setup

version_file = 'afilter/version.py'

def get_version():
    with open(version_file, 'r') as f:
        exec(compile(f.read(), version_file, 'exec'))
    return locals()['__version__']


if __name__ == '__main__':
    setup(
        name= 'afilter',
        version= get_version(),
        packages = find_packages(),
        author='WJG',
        author_email='wangjiangong2018@ia.ac.cn',
        license='Apache',
        url='',
        python_requires=">=3.6",
        install_requires=[
            "argparse",
            "numpy",
            "grpcio",
            "pillow",
            "nvidia-pyindex",
            "tritonclient[all]",
        ],
    )
