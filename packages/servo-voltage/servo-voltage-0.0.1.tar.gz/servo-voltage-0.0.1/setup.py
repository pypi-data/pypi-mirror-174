from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='servo-voltage',
    version='0.0.1',
    packages=['servo_voltage'],
    url='https://github.com/Adam-Software/Servo-voltage',
    license='MIT',
    author='vertigra',
    author_email='a@nesterof.com',
    description='Read voltage data for feetech servo',
    long_description_content_type="text/markdown",
    long_description=long_description,
    install_requires=['servo-serial', 'loguru'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Other',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ]
)
