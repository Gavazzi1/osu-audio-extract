import re
import os
from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
import urllib.parse

modpools = ['No Mod', 'Hidden', 'Hard Rock', 'Double Time', 'Free Mod', 'Tiebreaker', 'Rice', 'Long Note', 'Hybrid', 'Extreme']


class SongInfo:
    def __init__(self, fn, songlen):
        self.fn = fn
        self.songlen = songlen

    def __repr__(self):
        return 'fn={}, songlen={}'.format(self.fn, self.songlen)


def get_audio_tracks():
    """
    Read all mp3 and ogg files in CWD to SongInfo structs, then return them in a dictionary that maps:
    song title -> <fn=filename, songlen=length in seconds>
    """
    out = dict()

    for fn in os.listdir():
        if fn.lower().endswith('.mp3'):
            nominal_fmt = MP3
            backup_fmt = OggVorbis
        elif fn.lower().endswith('.ogg'):
            nominal_fmt = OggVorbis
            backup_fmt = MP3
        else:
            continue

        # 7KWC 2025 edit -- sometimes files might have incorrect extensions
        # osu! only supports mp3 and ogg, so just try the other if there's an error
        try:
            songdata = nominal_fmt(fn)
        except:
            songdata = backup_fmt(fn)

        title = fn[:-4]
        songlen = int(songdata.info.length)
        out[title] = SongInfo(fn, songlen)

    return out


def read_pool():
    """
    Read pool.txt, which contains the contents of simply copy-pasting the week's beatmap listing staring from "No Mod"
    (or "Rice" for MWC) and ending with the last character of the line containing the tiebreaker map

    Then, return list of dicts containing the artist, song title, mappers, and difficulty name
    """
    out = []
    c = re.compile('(?P<artist>.+) - (?P<title>.+) \((?P<mappers>.+)\) \[(?P<diff_name>.+)]( \(temporary link\))?$')

    try:
        fd = open('pool.txt', 'r')
    except FileNotFoundError:
        print("Could not find pool.txt. Please add the file and/or ensure you're in the same directory the files"
              "were extracted to")
        exit(1)

    for line in fd:
        ls = line.strip()
        if ls and ls not in modpools:
            result = c.match(ls)
            gd = result.groupdict()
            gd['title'] = gd['title'].replace('/', '')
            out.append(gd)

    fd.close()
    return out


if __name__ == '__main__':
    audio_data = get_audio_tracks()
    pool_info = read_pool()

    filedata = '#EXTM3U\n'

    for beatmap in pool_info:
        if beatmap['title'] not in audio_data:
            print('Could not find {}'.format(beatmap['title']))
            continue

        audio_file = audio_data[beatmap['title']]
        filedata += '#EXTINF:{},{} - {}\n'.format(audio_file.songlen, beatmap['artist'], beatmap['title'])
        filedata += '{}\n'.format(urllib.parse.quote(audio_file.fn))  # must url encode for VLC

    fn = os.getcwd().split('/')[-1] + '.m3u'
    with open(fn, 'w') as fd:
        fd.write(filedata)
    fd.close()
