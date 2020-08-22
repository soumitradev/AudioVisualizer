# Audio Visualizer
This is an old project (around 2 weeks old) in which I used FFTs to create a simple audiovisualizer. The code is not documented, and it is very hard to understand. It reads in a music file (.wav format) and spits out a .mp4 file with a graph of the frequencies. A sample .mp4 file is in the repo. To run this, make sure to replace tst.wav everywhere in your code with your wav file, and make sure the ffmpeg command at the end spits out the video file name you want.

 I might document and rewrite for live audio using pygame later.


## How does this work?
Well, FFTs. What are those?

tl;dr is, they approximate functions as a sum of many sinusoidal functions.

Now, notice how this is perfect for what we want to do. We have an audio signal, which is a function, and we want to express it as a sum of many sinusoidal functions. These sinusoidal functions are our frequencies.

Lets go deeper.

Lets start with our function $f$