import setuptools
from sys import version

if version < '2.2.3':
	from distutils.dist import DistributionMetadata
	DistributionMetadata.classifiers = None
	DistributionMetadata.download_url = None
	
from distutils.core import setup


setuptools.setup(
    name='mercadopago_qr',
    version='1.0.2',
    author='@rockscripts',
    author_email='rockscripts@gmail.com',
    description='MercadoPago - QR code for payments',
    long_description="",
    install_requires=[
                        'requests',
                     ],
    platforms='any',
    url='https://api.whatsapp.com/send?phone=573128097090',
    packages=[
                'mercadopago_qr',
                'mercadopago_qr.qr',
                'mercadopago_qr.http'
            ],
    python_requires=">=3",
    classifiers=[
                    'License :: OSI Approved :: BSD License',
                    'Programming Language :: Python :: 3',
                    'Topic :: Software Development :: Libraries :: Python Modules',
                ],
)