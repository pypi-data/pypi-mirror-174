from setuptools import setup

setup(
    name='fax_ai',
    version='0.1.0',
    description='A explanation based approach for fair supervised learning',
    url='https://github.com/social-info-lab/FaX-AI',
    author='Przemyslaw Grabowicz, Nicholas Perello, Aarshee Mishra',
    author_email='nperello1@gmail.com',
    license='MIT',
    python_requires='>=3.7',
    packages=['fax_ai'],
    install_requires=['numpy', 'scipy', 'scikit-learn','numpy','torch'],
    extras_require={
        "full": ["matplotlib", "aif360","shap","pandas"],
    },
    long_description="Fair and Explainable AI (FaX-AI) framework provides implementations for fair learning methods that remove direct discrimination without the induction of indirect discrimination. These methods are based on a joining of concepts in fairness and explainability literature in machine learning. They inhibit discrimination by nullifying the influence of the protected feature on a system's output, while preserving the influence of remaining features.",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
