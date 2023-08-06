from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(name='hackebds',
      version='0.1.9',
      description='This tool is used for backdoor and shellcode generation for various architecture devices',
      long_description_content_type="text/markdown",
      long_description=long_description,
      url='https://github.com/doudoudedi/hackEmbedded',
      author='doudoudedi',
      author_email='doudoudedi233@gmail.com',
      license='MIT',
      py_modules=['hackebds.arm','hackebds.mips',"hackebds.aarch64","hackebds.extract_shellcode"],
      data_files=["README.md"],
      entry_points={
      'console_scripts': [
      'hackebds = hackebds:main'
    ]
  },
)

