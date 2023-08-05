from setuptools import setup

setup(
    name="Lenpy",
    version="0.1",
    description="Simplify your life",
    long_description="Simplifies certain tasks when creating a game with Pygame",
    author="Quetzalcoutl",
    author_email="quetzalcoult2022@gmail.com",
    url="https://github.com/QuetzalcoutlDev/Lenpy",
    license="LGPL",
    packages=["lenpy"],
    python_requires='>=3.7',
    install_requires=['pygame>=2.0.1'],
    include_package_data=True,
    classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
      ],
    )