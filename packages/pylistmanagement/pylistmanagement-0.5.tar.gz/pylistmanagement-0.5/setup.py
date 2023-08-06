from distutils.core import setup
setup(
  name = 'pylistmanagement',         # How you named your package folder (MyLib)
  packages = ['pylistmanagement'],   # Chose the same as "name"
  version = '0.5',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This library has 3 functions with which you can manage lists or columns of dataframes. You can impute, operate and filter.',   # Give a short description about your library
  author = 'Beñat Basabe, Mario Rodriguez & Iker Nieto',                   # Type in your name
  author_email = 'iker.nieto@alumni.mondragon.edu',      # Type in your E-Mail
  url = 'https://github.com/ikertxu123/pylistmanagement',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/ikertxu123/pylistmanagement/archive/refs/tags/v_05.tar.gz',    # I explain this later on
  keywords = ['List', 'List Management', 'Filter' , 'Impute'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)