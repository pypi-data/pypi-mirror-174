from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(name='zdiab_tools',
      version='0.3',
      long_description=long_description,
      long_description_content_type='text/markdown',
      description='Rasa preprocessing package',
      packages=['zdiab_tools'],
      author = 'zohair diab',
      author_email = 'zohairdiab07@gmail.com',
      zip_safe=False)
