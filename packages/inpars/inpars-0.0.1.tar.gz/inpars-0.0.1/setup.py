from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'InPars'
LONG_DESCRIPTION = 'Inquisitive Parrots for Search'

# Setting up
setup(
        name="inpars", 
        version=VERSION,
        author="Hugo Abonizio",
        author_email="<hugo.abonizio@neuralmind.ai>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages("src"),
        install_requires=[
            'transformers',
            'accelerate',
            'ftfy',
            'ir_datasets',
            'bitsandbytes',
        ],
        
        keywords="nlp, machine learning, fewshot learning, transformers",
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Science/Research",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
        ]
)