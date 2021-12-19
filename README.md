# plex_and_media_utilities
A set of tools for managing and maintaining your media libraries

Please check the Wiki for more details on each script, but a short summary is detailed below

## Sonarr Episode Changes
Simple tool to find mismatches between files and episodes

* [Wiki](https://github.com/extrobe/plex_and_media_utilities/wiki/Sonarr-Episode-Changes)
* [Source](https://github.com/extrobe/plex_and_media_utilities/blob/main/sonarr_episode_changes.py)


This script is design to help identify when there have been changes to the season/episode ordering at TVDB (the episode meta source for Sonarr)

When ordering gets changed / episodes are added and removed, this can result in Sonarr mapping your files incorretly.

Whilst this script doesn't directly identofy when there have been metadata changes, it checks to see if your current file<>episode names match up.

This only works if you keep the episode name as part of your file name.

However if you have other metadata in your file names, that should be fine.

## Plex Collection Content Ratings
Scans your Plex collections, and updates the Colection content rating to match the 'lowest' rating of the films within the collection

* [Wiki](https://github.com/extrobe/plex_and_media_utilities/wiki/Plex-Collection-Content-Ratings)
* [Source](https://github.com/extrobe/plex_and_media_utilities/blob/main/plex_collection_content_rating.py)

Use this tool when you have Content Rating restricted profiles on your Plex server.
This will ensure that collections containing a mixture of content ratings will still be available if at least 1 item matches the Content Rating restriction.

Note: This Doesn't mean the restricted user will see the restricted items - they will see the Collection, along with any items that meet the profile limit.

## Plex Title Card Matcher
Looks up any shows you have against the subreddit r/PlexTitleCards to find any matches, and flag any 'incomplete' asset sets in your library.

* [Wiki](https://github.com/extrobe/plex_and_media_utilities/wiki/Plex-Title-Card-Finder)
* [Source](https://github.com/extrobe/plex_and_media_utilities/blob/main/plex_title_card_finder.py)


## Plex Meta Manager - Create Films YML File
Use this file in conjunction with Plex Meta Manager. It helps you create your initial YML file based on your existing custom metadata.