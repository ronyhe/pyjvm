from setuptools import setup

# noinspection SpellCheckingInspection
setup(
    python_requires='>=3.6.5',
    name='pyjvm',
    version='0.0.1',
    packages=['pyjvm', 'test'],
    entry_points='''
        [console_scripts]
        pyjvm=pyjvm.main:main
    ''',
    install_requires=[
        'click',
        'jawa',
        'pytest'
    ]
)
