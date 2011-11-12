import setuptools

setuptools.setup(name='chronos',
      version='0.1',
      description='OpenStack Performance Testing Application',
      author='Brian Waldon',
      author_email='bcwaldon@gmail.com',
      package_dir={'chronos': 'chronos/'},
      packages=setuptools.find_packages(where="chronos"),
      setup_requires=["nose"],
      test_suite = "nose.collector",
)
