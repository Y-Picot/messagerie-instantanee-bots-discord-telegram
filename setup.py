"""
Configuration d'installation pour le projet de bots Discord et Telegram.
"""

from setuptools import setup, find_packages

setup(
    name='messagerie-instantanee-bots',
    version='1.0.0',
    description='Bots Discord et Telegram pour la gestion de commandes de livraison',
    author='Y-Picot',
    packages=find_packages(),
    install_requires=[
        'discord.py>=2.0.0',
        'python-telegram-bot>=13.0'
    ],
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)


