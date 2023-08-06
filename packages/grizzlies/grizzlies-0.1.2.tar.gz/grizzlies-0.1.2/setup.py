from distutils.core import setup
setup(
  name = 'grizzlies',
  packages = ['grizzlies'],
  version = '0.1.2',
  license='MIT',
  description = 'Esta librería provee la capacidad de leer, convertir y guardar archivos csv a json, y viceversa.',
  author = 'Sendoa Busquet, Jon Jarrín',
  author_email = 'sendoa.busquet@alumni.mondragon.edu, jon.jarrin@alumni.mondragon.edu',
  url = 'https://github.com/JonJarrinVitoria/Grizzlies',
  download_url = 'https://github.com/JonJarrinVitoria/grizzlies/archive/refs/tags/v_01.2.tar.gz',
  keywords = ['CONVERT', 'JSON', 'CSV', 'NESTED', 'READ', 'SAVE'],
  install_requires=[
          'flatten_json',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
