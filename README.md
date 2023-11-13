# osu-audio-extract
Given a zip file containing .osz files, extracts the song audio from each beatmap and saves it to a new folder.

Simply run `./getaudio.sh <zip filename>`

All the audio files will be saved to a new directory with the same name as the zip file, but without the zip extension.

The audio files will have the same name as the song title in the respective .osu file, which sometimes breaks things. These have to be handled manually for now, but I patch the code each time to support them.
