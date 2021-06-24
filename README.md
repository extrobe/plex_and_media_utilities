# sonarr_episode_changes
Simple tool to find mismatches between files and episodes

## Overview
This script is design to help identofy when there have been changes to the season/episode ordering at TVDB (the episode meta source for Sonarr)

When ordering gets changed / episodes are added and removed, this can result in Sonarr mapping your files incorretly.

Whilst this script doesn't directly identofy when there have been metadata changes, it checks to see if your current file<>episode names match up.

This only works if you keep the episode name as part of your file name.

However if you have other metadata in your file names, that should be fine.


## Setup
You only need the main.py file.
Update the URL, Port and API key (API key from Sonarr>Settings>General)
Save
Run as python main.py

this will create an output.txt file containing your results

## Known Limitations

- Multi-Episode files aren't always going to be handled well (as 1 file can't have two names!)