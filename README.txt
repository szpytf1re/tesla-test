This project was created and tested on an Ubuntu 16.04 machine.

Please run the `setup.sh` script to install the required libraries and create a sqlite database.

Please run `python mange.py runserver` to start the Django web server. The homepage can be found at http://localhost:8000.

Note that the code in this project would not be acceptable for production use. However, given the time permitted, this first cut demonstrates the features available.

Some improvements that could be made:
- UI components should be tested using Selenium
- All python logic unit tested, including mocking out Yahoo! finance library responses
- A proper process for minifying, concatenating JS/CSS should be devised and all inline JS/CSS removed
