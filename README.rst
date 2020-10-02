lastfm-collage
===============

lastfm-collage is a tool to generate image collages from last.fm user's top albums and artists, like `this <https://gist.github.com/connnnor/b0970c52ebc53a6b586a7abf49c171f2/raw/f407f1910900a09ca81429e0a91e4f45539b39c5/1month.png>`_

I created this as part of a project to mess around with Django. The original idea to generate album art collages is from `tapmusic <http://tapmusic.net>`_

Quickstart
----------

lastfm-collage can be installed via `pip
<https://docs.python.org/3/installing/index.html>`_,

.. code-block:: console

  $ pip install git+https://github.com/connnnor/lastfm-collage#egg=lastfm_collage

lastfm-collage requires an API account from `Last.fm <https://www.last.fm/api>`_
once you have an account, place your API details in the lastfm-creds.json file like


.. code-block:: JSON

  {
    "api_key": "aaaaaaaaabbbbbbbbbcccccccccddddd",
    "api_secret": "eeeeeeeeefffffffff00000000011111"
  }

Or set the LASTFM_API_KEY and LASTFM_API_SECRET variables in your shell like

.. code-block:: console

  $ export LASTFM_API_KEY="aaaaaaaaabbbbbbbbbcccccccccddddd"
  $ export LASTFM_API_SECRET="eeeeeeeeefffffffff00000000011111"


Credits
-------

Thanks to `pylast 
<https://pypi.org/project/pylast/>`_, for making accessing the last.fm API very simple!
