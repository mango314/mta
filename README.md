# MTA TURNSTILE DATA

This is an honest-to-goodness attempt to read the MTA [turnstile data](http://www.mta.info/developers/turnstile.html) published weekly.

`wget http://www.mta.info/developers/data/nyct/turnstile/turnstile_130803.txt`

The goal would be to specialize ajschumacher's "Calendar view" [visualization](http://bl.ocks.org/ajschumacher/5127001) of MTA usage to each train station (e.g. 125st & Lexington) and line (e.g. D ).

![](http://mathbabe.files.wordpress.com/2013/03/screen-shot-2013-03-11-at-6-50-19-am.png)

The weekly [metrocard swipes](http://www.mta.info/developers/fare.html) of the City are also available from 2010 onwards.

Both data sets would make great use of [mixture models](http://www.robots.ox.ac.uk/~az/lectures/ml/lect8.pdf) to make guesses:

- Among the people who enter/exit Times Square, what fraction is taking the S-train?
- Among the people who enter/exit Grand Central Station who is taking the 6-train?

# How to Decipher the Turnstile Data
In order to read MTA's data set you need to understand lines like

	R151,G009,STILLWELL AVE,DFNQ,BMT

and 

	A002,R051,02-00-00,
	07-27-13,00:00:00,REGULAR,004209603,001443585,
	07-27-13,04:00:00,REGULAR,004209643,001443593,
	07-27-13,08:00:00,REGULAR,004209663,001443616,
	07-27-13,12:00:00,REGULAR,004209741,001443687,
	07-27-13,16:00:00,REGULAR,004210004,001443740,
	07-27-13,20:00:00,REGULAR,004210276,001443777,
	07-28-13,00:00:00,REGULAR,004210432,001443801,
	07-28-13,04:00:00,REGULAR,004210472,001443805 
                                                                                                                 
## Example #1 - Remote-Booth-Station

Hopefully we recognize the 3rd & 4th items in 	`R151,G009,STILLWELL AVE,DFNQ,BMT`.  They say that

- The station name is **Stillwell Ave**
- The **D,F,N,Q** trains run through this station
- This is a BMT line

We New Yorkers can point this spot on a map!  What about `R151,G009`?  These are the *Remote* and the *Booth* (and "Stillwell Ave" was the *Station*).

It is hard to decipher these two pieces of MTA jargon.  Could be they kind of map to [station entrances](https://groups.google.com/forum/#!msg/mtadeveloperresources/gGWAd6U9EuI/N-Ya8n08kD8J).

## Example 2: Times Square
	R032,R145,42 ST-TIMES SQ,1237ACENQRS,IRT
	R032,A021,42 ST-TIMES SQ,1237ACENQRS,BMT
	R032,R143,42 ST-TIMES SQ,ACENQRS1237,IRT
	R032,R146,42 ST-TIMES SQ,1237ACENQRS,IRT
	R033,R151,42 ST-TIMES SQ,1237ACENQRS,IRT
	R033,R148,42 ST-TIMES SQ,1237ACENQRS,IRT
	R033,R150,42 ST-TIMES SQ,1237ACENQRS,IRT
	R033,R153,42 ST-TIMES SQ,1237ACENQRS,IRT
	R033,R147,42 ST-TIMES SQ,1237ACENQRS,IRT

The 11 lines 1-2-3-7-A-C-E-N-Q-R-S pass thru here.  There are two "remotes" with 4 and 5 "booths".  This makes sense since Times Square is very large

## Example 3: 125st + Lexington Ave (4-5-6)

	R034,R174,125 ST,1,IRT

[125 st](http://en.wikipedia.org/wiki/125th_Street_(IRT_Lexington_Avenue_Line)) - one of the busiest stations in the MTA system gets only 1 remote and 1 booth.

## Example 4: Turnstile Data - A002

MTA's turnstile data set is comma-separated, with 3 items related to the station and turnstile, followed by groups of five.

A typical line has 3+5×8=43 items for [59st + Lexington Ave](http://en.wikipedia.org/wiki/Lexington_Avenue_/_59th_Street_(New_York_City_Subway)) station on July 27, 2013.

	A002,R051,02-00-00,
	07-27-13,00:00:00,REGULAR,004209603,001443585,
	07-27-13,04:00:00,REGULAR,004209643,001443593,
	07-27-13,08:00:00,REGULAR,004209663,001443616,
	07-27-13,12:00:00,REGULAR,004209741,001443687,
	07-27-13,16:00:00,REGULAR,004210004,001443740,
	07-27-13,20:00:00,REGULAR,004210276,001443777,
	07-28-13,00:00:00,REGULAR,004210432,001443801,
	07-28-13,04:00:00,REGULAR,004210472,001443805

- the first column is the date
- the second column is the time stamp.  it usually checks every **4** hours
- the status is **REGULAR**
- the *entries* read "004209603" and the *exits* read "001443585"
- between 8am and 12am on July 23, 741-663=78 passengers entered the station (and 71 exited ) *through this turnstile*

The three info `A002,R051,02-00-00` specify a single turnstile in the entire MTA system.  Looking at `remote-booth-station.csv` we find it was part of a group of 3 entrances, itself part of two sets of entrances.

	R050,R244,59 ST,456NQR,IRT
	R050,R244A,59 ST,456NQR,IRT
	R050,A004,LEXINGTON AVE,456NQR,BMT
	R051,R245,59 ST,456NQR,IRT
	R051,R245A,59 ST,456NQR,IRT
	R051,A002,LEXINGTON AVE,456NQR,BMT

This is a very busy station with passengers between Queens, the Upper East Side, Times Square, and Midtown East.