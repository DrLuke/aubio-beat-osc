# Beat Detection with OSC

This is a simple beat detector built with [aubio](https://github.com/aubio/aubio).
It will detect the beat and BPM on the default audio input.
On every beat, the current BPM is sent to one or more OSC servers.

## Installation

```
pip install aubio-beat-osc 
```

## Usage

```
aubio-beat-osc [-h] -c IP PORT ADDRESS [-b BUFSIZE] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -c IP PORT ADDRESS, --client IP PORT ADDRESS
                        OSC Client address (multiple can be provided)
  -b BUFSIZE, --bufsize BUFSIZE
                        Size of audio buffer for beat detection (default: 128)
  -v, --verbose         Print BPM on beat
```

### `-c`/`--client`
Add an `IP`, `PORT` and OSC `ADDRESS` to which the BPM beat signal will be sent to. Example: `-c 127.0.0.1 31337 /foo/beat`

### `-b`/`--bufsize`
Select the size of the buffer used for beat detection. A larger buffer is more accurate, but also more sluggish. Refer to the [aubio](https://github.com/aubio/aubio) documentation of the tempo module for more details. Example: `-b 128`

### `-v`/`--verbose`
Output a handy beat indicator and the current BPM to stdout.

## Example

```
$ aubio-beat-osc -c 127.0.0.1 31337 /foo/bar -c 10.10.13.37 12345 /test/baz -v
```

This will send beat messages to the OSC address `/foo/bar` on `127.0.0.1:31337` and `/test/baz` on `10.10.13.37:12345`. Additionally the current BPM will be printed to stdout.
