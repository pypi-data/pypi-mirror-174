from distutils.core import setup
setup(
  name = 'libreria_correlaciones',         # How you named your package folder (MyLib)
  packages = ['libreria_correlaciones'],   # Chose the same as "name"
  version = '0.7',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Esta librería sirve para la deteccion de correlaciones de cara a limpiar los datos para un modelo de clasificacion binaria.',   # Give a short description about your library
  author = 'Paula',                   # Type in your name
  author_email = 'paula.hermosilla@alumni.mondragon.edu',      # Type in your E-Mail
  url = 'https://github.com/PaulaHermosilla/libreria_correlaciones',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/PaulaHermosilla/libreria_correlaciones/archive/refs/tags/v_07.tar.gz',    # I explain this later on
  keywords = ['CORRELACIONES', 'CLASIFICACION_BINARIA', 'HISTOGRAMAS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'seaborn',
          'matplotlib',
          'numpy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.9',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)