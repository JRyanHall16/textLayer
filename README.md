# textLayer
## Purpose
textLayer is a project that I have been working on that is written in Python. The purpose of textLayer is to connect to and log in to Cengage's website and download the pages of textbooks that are otherwise unavailable for download. It's support is more than likely spotty, but it works for the books that I needed access to on-the-go and had already paid to access. This project is not intended for illegal uses, but to grant offline access to the online material that you have paid money for already.
## Usage
This project uses Python in conjunction with Selenium to control your browser. As it currently operates, it won't work unless you modify the code to specify some things and as the Cengage site might change, so too will the identifiers the project uses to access elements of the various pages. As such, this should more than likely be used as a starting point, that you then modify to suit your needs (whatever those are.) Also, this is written under the assumption that you are using Firefox, which is the only browser I use because I am comfortable with it and it's fast (in my experience) so, again, you'll need to research/make changes to use some other browser.
## Links
* [Selenium for Python](https://selenium-python.readthedocs.io/)
* [GeckoDriver](https://github.com/mozilla/geckodriver/releases)
