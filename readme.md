# Python Noise

Tiny Python scripts to plot and listen to random signals.

Currently we just have *narrowband noise*. This is white noise that is passed through an (ideal) bandpass filter. I think it's pretty neat.

$n(t) = r(t) \cos (2\pi f_c t + \phi (t))$

## Installation
```bash
pip install -e .
pip install -r requirements.txt
```

## Usage
### Narrowband Noise
```bash
nbn <fcarrier> <hbandwidth> <duration> <wavfile>
````

All arguments are optional.
- `fcarrier` defaults to 1000 Hz
- `hbandwidth` defaults to 100 Hz
- if `duration` is not specified, audio does not play
- if `wavfile` is not specified, no file is not saved
