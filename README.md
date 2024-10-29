# osu-audio-extract
Given a zip file containing .osz files, extracts the song audio from each beatmap and saves it to a new folder.

Simply run `./getaudio.sh <zip filename>`

All the audio files will be saved to a new directory with the same name as the zip file, but without the zip extension.

The audio files will have the same name as the song title in the respective .osu file, which sometimes breaks things. These have to be handled manually for now, but I patch the code each time to support them.

## M3U File Creation

Within the newly-created folder containing the audio files, you can run the `make_m3u.py` script to create a playlist of the songs in the order they appear in the mappool.

This requires a file in the current working directory called `pool.txt`, which should contain the text description, copied from the osu website, of the mappool contained in the zip file, starting from "No Mod" and ending with the last character in the last line of the mappool (usually the tiebreaker map).

If no such text exists, the format of `pool.txt` is `<artist> - <song title> (<mapper>) [<difficulty name>]` for each song, each on its own line in the file.

For example, 

```
CITROBAL - Celluloid (Kaine) [Fsjallink's Insane]
senya - Sakuretsu Irony (Satellite) [Satellite]
Two Door Cinema Club - Cigarettes In The Theatre (Lesjuh) [Insane]
```
