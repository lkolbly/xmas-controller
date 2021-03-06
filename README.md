Christmas Light Controller
==========================

Welcome to the Christmas Light Controller codebase. This repository contains all of the code required to run

The music algorithm is currently run by a made-up algorithm which consumes mel energy data about the song in question. The mel energy data can be generated by running the demo_mel-energy.py script on the wav file of your choice:

```
$ . setup.sh
$ python demo_mel-energy.py carol.of.the.bells.stirling.wav > carol.of.the.bells.stirling.mel
```

Once the mel file is created, it can be consumed by the playSong method in xmas.py, which takes a ncurses screen and the prefix of the song. (".wav" is appended to get the audio file, ".mel" is appended to get the mel data)

```
$ python xmas.py carol.of.the.bells.stirling
```

If the `SIMULATE` variable is True, then gpiozero will not be used to control the lights (as it is in production), and instead of playing over the radio, the audio file will be played by running "mplayer <audio file>" in a shell.

(note: The demo_mel-energy.py file is largely based on an example from the aubio library, and thus is largely not my own work)
