# sonarr_episode_changes
Simple tool to find mismatches between files and episodes

## Overview
This script is design to help identofy when there have been changes to the season/episode ordering at TVDB (the episode meta source for Sonarr)

When ordering gets changed / episodes are added and removed, this can result in Sonarr mapping your files incorretly.

Whilst this script doesn't directly identofy when there have been metadata changes, it checks to see if your current file<>episode names match up.

This only works if you keep the episode name as part of your file name.

However if you have other metadata in your file names, that should be fine.

### Example of Misaligned Files
![Alt text](screens/sonarr.png?raw=true "Title")


### Example of Script Output
![Alt text](screens/output.png?raw=true "Title")


## Usage
Edit and run the script.

Review the output file it generates, and detirmine if you need to re-arrange your files.

**Note:**
Just because an item was flagged, doesn't mean it's a genuine issue - just means it didn't see the episode title in the file name

**Important:**
This script DOES NOT change anything in Sonarr. Only YOU do that. However, you should make sure you're comfortable with what this code is doing before you run it - don't trust random code on the internet!


## Setup
You only need the main.py file.
Update the URL, Port and API key (API key from Sonarr>Settings>General)
Save
Run as python main.py

this will create an output.txt file containing your results

It should be pretty fast - for me it scans > 30,000 files in under 60 seconds, with my instance being on a remote device

## Optional Settings

These can be edited directly in the main.py file

### ignore_default_episdode_name
Default = True

If you have episodes without a name, they just get 'Episode 1', but you may not want this in your file name. Setting to True ignore this files.
In the future I would like to instead 'test' these items against the SxxEyy string in the filename

### scrub__and__strings
Default = True

If you use '&' and 'and' interchangeably, it might flag files as an issue. Setting this to True scrubs the work 'and' from the comparisons. ('&' already gets scrubbed unless you're using Strict comparison - in which case you would want to set this value to False)

### allow_multi_part_episode_files
Default = True

When you have files covering multiple episodes, and the episode name is Episode Name (Part 1) & Episode Name (Part 2) , will match correctly if the rest of the episode name (excluding the 'part 1' part) matches

## Known Limitations

- There might still be some multi-episode files which don't get handled corectly, but believe most scenarios are now covered
- If the Episode doesn't have a title, it looks like it always defaults to 'Episode _N_ ' . This script has the option to ignore these, but doesn't (yet) instead check the 'Episode 1' matches up with the file name S01E01 episode ID
