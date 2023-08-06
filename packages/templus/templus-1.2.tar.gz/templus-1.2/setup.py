import setuptools

with open("README.md") as file:
	big_descr = file.read()

setuptools.setup(name='templus',
      description='library for reading and receiving messages from https://tempmail.plus/ru/#!',
      version = "1.2",
      packages=["templus"],
      long_description = big_descr,
      download_url = "https://github.com/BitterTruth1/templus/archive/refs/heads/main.zip",
      long_description_content_type="text/markdown",
      url = "https://github.com/BitterTruth1/templus",
      author_email='bonnita1900432@gmail.com')
