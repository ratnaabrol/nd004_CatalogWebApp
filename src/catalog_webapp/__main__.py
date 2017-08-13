#!/usr/bin/env python3

"""Main script for the package. Runs our flask application.
NOT FOR PRODUCTION USE."""

from catalog_webapp.web.app import APP


if __name__ == "__main__":
    APP.secret_key =\
        b'4\xa5\xa8Pv\r\x05\x90\xc9\xe4^D\x1e{\xef\xd2\xb9n\x96\xa4\x92\xa4mP'
    APP.run(host="0.0.0.0", port=5000, debug=True)
