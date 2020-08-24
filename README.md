# :musical_note: Audio Visualizer
This is a python script that visualizes music files. (Currently only limited to 16 and 32 bit PCM encoded .wav files). I know that sounds very specific, but don't worry! Your audio file when in wav format is probably already compatible since this is one of the most popular formats.

Stereo audio files are converted to mono for processing. This takes more time to analyze audio, but the original audio file is not modified.

Read the [Jupyter notebook](./Explanation.ipynb) for more information.

## Why?
Some day in May 2020, I had too much coffee, and sat down to learn how JPEG compression works (because I just got finished watching Silcon Valley, and my interest in compression peaked). I learnt about the DCT, and slowly as I went down the rabbit hole, I came out the other side of the coin: I was learning how DFTs can be used for wave analysis.

It had to be done. I had to write an audio visualizer.

So I sat down, read up about DFTs, and tried a small example of an FFT with numpy in a Jupyter Notebook. I used matplotlib to sketch the graphs, and ffmpeg to stitch the frames for the video together. But, I hadn't written any documentation or comments. I was happy with analysing one file, and I uploaded it to GitHub.

Later in August, someone asked me about the most fun project I've worked on. My mind immediately went to this project. However, I couldn't really show or explain it since it was just a wall of text with badly named variables. So, I decided to document it, and optimize parts of it.

And now, here it is. It is complete with a mathematical explanation of how the audio is analyzed.

Easily one of my proudest projects.

## Usage
The complete explanation of how this works is in the [Jupyter notebook](./Explanation.ipynb). I'd suggest reading that before going through the [main script](./AudioVisualizer.py).

The script is a python script that requires numpy, scipy, and pygame. These can be installed by running `pip install -r requirements.txt`. After that, you can can edit the `AudioVisualizer.py` to load your music file instead of the test one I've included.

:warning: **The test file I've included (tst.wav) is a full pan of the 0-22kHz audio spectrum. It contains very irritating sounds.**

To run the visualizer, run `python ./AudioVisualizer.py`

The script is fairly slow, especially the rebinning process. I might optimize this in the future, and may make rebinning optional.

The script is slow only in 2 parts:
- Converting stereo to mono, and
- Rebinning the data we get after performing the FFT.

If you decide to feed it a mono file, it will be much faster since the script need not convert it in memory.

On a test audio file, I got the following timings in seconds for each step:
- **Mono file:** Total: 38.949s, Interpolation: 0.396s, Binning: 34.263s, FFT: 4.290s, Mono Conversion: 0
- **Stereo file:** Total: 62.783s, Interpolation: 0.392s, Binning: 31.888s, FFT: 4.96s, Mono Conversion: 25.539s

## Contribution
*Any* help with optimization is appreciated. Other than that, more audio formats, and miscellaneous features are also welcome. Please create an Issue, and if possible, a Pull Request for new/suggested features.
