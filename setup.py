from setuptools import setup, find_packages


if __name__ == "__main__":
    setup(
        name="pyYandexLinguistics",
        version="0.1.0",
        author="hell03end",
        author_email="hell03end@outlook.com",
        description="Yandex Linguistics APIs for Python 3.3+",
        license="MIT License",
        keywords="translate dictionary predict predictor yandex "
                 "yandex-translate yandex-dictionary yandex-predictor",
        url="https://github.com/hell03end/pyYandexLinguistics",
        packages=find_packages(),
        package_dir={'pyYandexLinguistics': 'pyYandexLinguistics'},
        provides=['pyYandexLinguistics'],
        classifiers=[
            "Intended Audience :: Developers",
            "Development Status :: 0.1 - Alpha",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.6"
            "Programming Language :: Python :: 3.5"
            "Programming Language :: Python :: 3.4"
            "Programming Language :: Python :: 3.3"
        ],
        platforms=['All'],
        install_requires=['requests>=2.9.1']
    )
