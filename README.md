# plex_and_media_utilities
A set of tools for managing and maintaining your media libraries

Please check the Wiki for more details on each script, but a short summary is detailed below

## Sonarr Episode CHanges
Simple tool to find mismatches between files and episodes

This script is design to help identify when there have been changes to the season/episode ordering at TVDB (the episode meta source for Sonarr)

When ordering gets changed / episodes are added and removed, this can result in Sonarr mapping your files incorretly.

Whilst this script doesn't directly identofy when there have been metadata changes, it checks to see if your current file<>episode names match up.

This only works if you keep the episode name as part of your file name.

However if you have other metadata in your file names, that should be fine.

## Plex Collection Content Ratings
Scans your Plex collections, and updates the Colection content rating to match the 'lowest' rating of the films within the collection

Use this tool when you have Content Rating restricted profiles on your Plex server.
This will ensure that collections containing a mixture of content ratings will still be available if at least 1 item matches the Content Rating restriction.

Note: This Doesn't mean the restricted user will see the restricted items - they will see the Collection, along with any items that meet the profile limit.

## Plex Meta Manager - Create Films YML File
Use this file in conjunction with Plex Meta Manager. It helps you create your initial YML file based on your existing custom metadata.