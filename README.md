# MTA TURNSTILE DATA

This is an honest-to-goodness attempt to read the MTA [turnstile data](http://www.mta.info/developers/turnstile.html) published weekly.

The goal would be to specialize ajschumacher's "Calendar view" [visualization](http://bl.ocks.org/ajschumacher/5127001) of MTA usage to each train station (e.g. 125st & Lexington) and line (e.g. D ).

![](http://mathbabe.files.wordpress.com/2013/03/screen-shot-2013-03-11-at-6-50-19-am.png)

The weekly [metrocard swipes](http://www.mta.info/developers/fare.html) of the City are also available from 2010 onwards.

Both data sets would make great use of [mixture models](http://www.robots.ox.ac.uk/~az/lectures/ml/lect8.pdf) to make guesses:

- Among the people who enter/exit Times Square, what fraction is taking the S-train?
- Among the people who enter/exit Grand Central Station who is taking the 6-train