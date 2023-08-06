from distutils.core import setup
setup(
  name = 'nagore',         
  packages = ['nagore'],   
  version = '0.1',      
  license='MIT',        
  description = 'This is a package that makes data augmentation by optimizing the distributions of the variables using a single objective algorithm.',
  author = 'Nagore Bermeosolo y Ainhoa Paredes',              
  author_email = 'nagore.bermeosolo@alumni.mondragon.edu',   
  url = 'https://github.com/nagorebermeosolo/nagore',   
  download_url = 'https://github.com/nagorebermeosolo/nagore/archive/refs/tags/0.1.tar.gz',   
  keywords = ['Data Augmentation', 'Distributions', 'Single-Objective'],   
  install_requires=[    
          'pandas',
          'opencv-python',
	    'matplotlib',
	    'sdv',
          'scikit-learn'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9'
  ],
)