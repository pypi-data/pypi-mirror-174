from distutils.core import setup
setup(
  name = 'descriptive_analysis_beginner_friendly',         
  packages = ['descriptive_analysis_beginner_friendly'],   
  version = '0.1',      
  license='MIT',        
  description = 'Este paquete permite generar un analisis descriptivo con estadisticos y visualizaciones de manera sencilla.',
  author = 'Nagore Bermeosolo y Ainhoa paredes',              
  author_email = 'nagore.bermeosolo@alumni.mondragon.edu',   
  url = 'https://github.com/nagorebermeosolo/descriptive_analysis_beginner_friendly',   
  download_url = 'https://github.com/nagorebermeosolo/descriptive_analysis_beginner_friendly/archive/refs/tags/0.1.tar.gz',   
  keywords = ['Descriptive Analysis', 'Statistics', 'EDA'],   
  install_requires=['pandas', 'warnings', 'itertools', 'numpy', 'math', 'seaborn', 'matplotlib'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9'
  ],
)