# interpret-eaf
This script extracts information from an .eaf transcription file and calls ffmpeg to clip a full-length .wav file into .opus files corresponding to each transcription tier segment. The resulting .opus files are named with a numeric prefix corresponding to the line numbers displayed in ELAN's Transcription Mode.

There are currently two versions available here: one for use with .eaf files produced using ELAN version 5.9, and another for use with .eaf files produced using ELAN version 6.1. The crucial differences between these two scripts is that there is additional whitespace added to .eaf files created in ELAN 6.1 that is accounted for in the updated script.
