# VTOFG: Vibration Test Object Function Generator

## Introduction

A function generator that uses the audio output (3.5mm port, speaker, or usb-c) on a computer, for use with a vibration test object (VTO) for testing of doppler ultrasound. This can be used as a general function generator if plot is set to False.

When the function generator is ran it has the following inputs:
-- Master amplitude: the overall amplitude of the signal (essentially the volume when played through a speaker)
- Generator frequency: the frequency of the audio frames in the signal
- Resolution: the resolution of each audio frame
- Buffer time: the length of each segment that is calculated/played (the next segment is calculated while the previous one is being played)
- Transducer Frequency: The ultrasound wave frequency in kHz
- Pulse Repetition Frequency: The Pulse Repetition Frequency that the scanner is using in Hz
- Display Time: The time period displayed
- Display Samples: The number of lines per time period
- Wall Filter: The wall filter frequency used (A simple cutoff mask is used)
- Gain: Arbitrary value use to scale the displayed signal
- Display Speed: used to control the display speed if it is out of sync with the signal
- For each sweep wave:
  - Wave amplitude: relative to each other, changing this will not change the overall signal amplitude
  - Start Frequency: the frequency to start the sweep
  - End Frequency: the frequency to end the sweep
  - Sweep Time: the period of the sweep

## Installation Instructions

### Windows

Use pip to install the vtofg package:

`pip install vtofg`

Run the following python script:
```
import vtofg

gen = vtofg.FunctionGenerator(plot=True)
gen.mainloop()
```

Set plot to False if you don't want the plotter.

See Example.PNG for expected output when ran with settings shown in image.

### Mac and others

Installation of the package is largely the same, except you will need to run `pip3 install vtofg` instead of `pip install vtofg`. You may also need to manually install a version of python through your package manager which includes tkinter, as the default version of python3 preloaded onto your system may not contain this.

### Python Version
An installation of python 3.7.9 is recommended, other versions have not been tested.

## Roadmap
- Adding functionality to save/load waves
- Add functionaality to run .wav files

## Contributing
Contributions are welcome

## Contributors
- Zack Ravetz

## License
This project is licensed under the BSD license.
