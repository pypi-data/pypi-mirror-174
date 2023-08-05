from distutils.core import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()



setup(
  name = 'mlforall',         # How you named your package folder (MyLib)
  packages = ['mlforall'],   # Chose the same as "name"
  version = '0.4',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Library that easily allows to create machine learning progress for more unexperiencied programmers.',   # Give a short description about your library
  author = 'Unai Torrecilla',                   # Type in your name
  author_email = 'unai.torrecilla@alumni.mondragon.edu',      # Type in your E-Mail
  url = 'https://github.com/UnaiTorrecilla/MLForAll',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/UnaiTorrecilla/MLForAll/archive/refs/tags/v_04.tar.gz',    # I explain this later on
  long_description = long_description,
  long_description_content_type = 'text/markdown',
  keywords = ['Machine learning', 'Easy to use'],   # Keywords that define your package best
  install_requires = [            # I get to this in a second
          'pandas',
          'numpy',
          'scikit-learn',
          'openpyxl'
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.9'      #Specify which pyhton versions that you want to support
  ],
)
