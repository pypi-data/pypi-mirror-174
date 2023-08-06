from distutils.core import setup
setup(
  name = 'simplest_descriptive_analysis',         
  packages = ['simplest_descriptive_analysis'],   
  version = '0.2',      
  license='MIT',        
  description = 'Esta librería permite generar un análisis descriptivo de forma rápida y sencilla',
  author = 'Nagore Bermeosolo y Ainhoa Paredes',              
  author_email = 'nagore.bermeosolo@alumni.mondragon.edu',   
  url = 'https://github.com/nagorebermeosolo/simplest_descriptive_analysis',   
  download_url = 'https://github.com/nagorebermeosolo/simplest_descriptive_analysis/archive/refs/tags/0.1.tar.gz',   
  keywords = ['EDA', 'Descriptive Analysis', 'Statistical Analysis'],   
  install_requires=[    
          'pandas',
          'numpy',
	    'matplotlib',
	    'seaborn'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
  ],
)