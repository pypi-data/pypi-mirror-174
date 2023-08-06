from distutils.core import setup
setup(
  name = 'daug_ga',         
  packages = ['daug_ga'],   
  version = '0.1',      
  license='MIT',        
  description = 'This is a package that makes data augmentation by optimizing the distributions of the variables using a single objective algorithm.',
  author = 'Ane Martínez and Elene Astondoa',              
  author_email = 'anemartinezorellana@outlook.es',   
  url = 'https://github.com/anemartinez1/daga_aug',   
  download_url = 'https://github.com/anemartinez1/daug_ga/archive/refs/tags/0.1.tar.gz',   
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