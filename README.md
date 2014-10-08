songblocks
==========

A python script to remotely control a Sonos music player with NFC tags.  For an overview of the full Song Blocks project, see [here](http://shawnrk.github.io/songblocks).

The main source file is songblocks.py.

I'm a mediocre developer at best and this is my first Python project.  I was more interested in getting it working than doing it right, so I absolutely cut some corners.  For instance, part of the nfcpy library is part of this repo because I didn't have the patience to figure out how Python's module path stuff worked, so I just put the module I needed in my working directory.  Also, _common.py is sourced from the TweetPony library and used to set up the connection to Twitter.

Thanks to the developers of the SoCo, nfcpy, and TweetPony, libraries. All were pretty easy to use for a novice.
