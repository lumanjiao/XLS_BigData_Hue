
"""A plugin to run nosetests more interactively

nosetty is a plugin for [http://somethingaboutorange.com/mrl/projects/nose/ nose], a test runner for python.  It accepts various commands at the terminal, giving you some one-on-one quality time with your tracebacks.  Most importantly, editing a failure point is as easy as typing a number.  How about a screenshot?

http://farmdev.com/projects/nosetty/nosetty-screenshot.png

== Install ==

{{{
easy_install nosetty
}}}

get the [http://peak.telecommunity.com/DevCenter/EasyInstall easy_install command here].

Development versions are available as:

{{{
easy_install nosetty==dev
}}}

...or via subversion at [http://nosetty.googlecode.com/svn/trunk/#egg=nosetty-dev http://nosetty.googlecode.com/svn/trunk/]

== Usage ==

Activate the plugin like so:

{{{
nosetests --tty
}}}

But to get some useful results, you'll have to tell it how to hook into your editor and other things.  All this is described in detail on the [Recipes] page.

To give the plugin a whirl, you can [http://code.google.com/p/nosetty/source checkout the source] and type...

{{{
cd src/nosetty
easy_install .
nosetests -w examples --tty
}}}

...to get what's shown in the above screenshot.

== Project Page ==

If you're not already there, the nosetty project lives on [http://code.google.com/p/nosetty/ google code].  Please submit any bugs, patches, failing tests, et cetera using the [http://code.google.com/p/nosetty/issues/list Issue Tracker].

"""

__version__ = "0.4"

try:
    import nose
except ImportError:
    # there's probably a better way to do this that I can't think of right now.
    # In this situation, we have downloaded the module from setuptools but the 
    # dependencies (nose) haven't been installed yet
    pass
else:
    del nose
    from nosetty import *