# Import dependencies
import numpy as np
import math
from scipy.io import wavfile
import time
import pygame
import sys

# Define some constants that will be used throughout the script
SONG_FILE = './pls.wav'
NUMBER_OF_PACKETS_PER_SEC = 15
NUMBER_OF_BINS = 50
BLOCK_SIZE = 20
PADDING = 5

# Color constants
CELL_COLOR = 255, 255, 255
BG_COLOR = 0, 0, 0

# Pygame window size
size = width, height = PADDING + NUMBER_OF_BINS*(BLOCK_SIZE + PADDING), 680

# Define an FFT function that we'll use for analysing audio

# Note how we also pass the number of samples as an argument
# since we call this function a lot and repeatedly calculating number of samples
# (which is a constant) will only slow it down


def FFT(stuff, sampling_rate, num_samples):
    # Perform an FFT on our audio data and grab the first half
    # since the second half is a mirror of the first in a fourier transform
    F = list(np.fft.fft(stuff))[:round(num_samples/2)]

    # Calculate sampling resolution
    sampling_resolution = sampling_rate/num_samples

    # For every frquency we get, double the data and get the magnitude of the vector,
    # and divide by number of samples to get actual amplitude
    return [(2*abs(freq)/num_samples, i*sampling_resolution) for i, freq in enumerate(F)]

    # Notice how we used a list comprehension (which is faster than a for loop) and enumerate()
    # instead of accessing F[i] repeatedly. We are trading memory space for speed.
    # However, note that this won't take a whole lot of memory since we work with only around
    # 2000 sized lists with pure numbers in it, and that all this memory space is deallocated
    # after the function returns.

# Write a function to get the size of the overlap between two ranges. We will use this for rebinning


def get_overlap(t1, t2):
    x = min(t1[1], t2[1]) - max(t1[0], t2[0])
    return x if x > 0 else 0


# Read in the song file
sample_rate, data = wavfile.read(SONG_FILE)


a = time.time()
# Check if audio file is stereo. If it is, convert it to mono
mono = False
if type(data[0]) == np.ndarray:
    mono = True
    print("Stereo Audio file detected, converting to Mono. The original file will NOT be modified.")
    data = [sum(k)/2 for k in data]
    print("Conversion to Mono completed.")

# Set some constants that will be used
N = len(data)
packet_len = int(sample_rate/NUMBER_OF_PACKETS_PER_SEC)

print("Processing audio...")
e = time.time()

# Break audio samples into packets, and perform FFT on each packet
packeted_data = [data[i*packet_len:(i+1)*packet_len]
                 for i in range(N//packet_len + 1)]
fft_ed_data = [FFT(packet, sample_rate, packet_len)
               for packet in packeted_data]
print("FFT completed.")
d = time.time()


rebinned = []

# Calculate new bin limits, and rebin each packet
for packet in fft_ed_data:
    amps, old_bins = zip(*packet)
    old_bins = list(old_bins)
    old_bins.append(sample_rate/2)
    bin_limits = [sample_rate/2 *
                  (B_i/NUMBER_OF_BINS)**2 for B_i in range(NUMBER_OF_BINS + 1)]

    new_bin_vals = []

    for i in range(1, NUMBER_OF_BINS + 1):
        # Some initial variables for rebinning
        low = 0
        l_lim = bin_limits[i-1]
        hi = 0
        h_lim = bin_limits[i]

        # Grab the intervals in old bins that become part of the new bins
        for j in range(hi, int(sample_rate/NUMBER_OF_PACKETS_PER_SEC + 1)):
            if old_bins[j - 1] <= l_lim:
                low = j
            if old_bins[j] >= h_lim:
                hi = j
                break
        # Initialize a sum and add the corresponding portion of the audio intensity to our new bin.
        s = 0
        for k in range(low, hi):
            s += packet[min(k, 1469)][0] * (get_overlap((bin_limits[i-1], bin_limits[i]),
                                                        (old_bins[max(0, k-1)], old_bins[min(k, 1469)])) / (old_bins[k] - old_bins[max(0, k-1)]))

        # Append the rebinned bin value to our new bin value list
        new_bin_vals.append(s)
    # Append packet to the rebinned binned list
    rebinned.append(new_bin_vals)

print("Rebinning completed.")
c = time.time()

# Interpolate data between packets and adjust the intensity of sound according to our smoothing function
interpolated = []
glob_max = max([max(packet) for packet in rebinned])
for i in range(len(rebinned) - 1):
    interpolated.append([math.log((m/glob_max)**2 + 1) /
                         math.log(2) for m in rebinned[i]])
    interpolated_packet = [
        (rebinned[i][j] + rebinned[i+1][j])/2 for j in range(NUMBER_OF_BINS)]
    interpolated.append([math.log((m/glob_max)**2 + 1)/math.log(2)
                         for m in interpolated_packet])


print("Interpolation completed.")
b = time.time()

# Print some timing information
print(f'Total: {b-a}, Interpolation: {b-c}, Binning: {c-d}, FFT: {d-e}, Mono Conversion: {0 if not mono else e-a}')

# Set FPS (slightly more than 30 so that the delay in rendering the bars is accounted for)
FPS = 32

# Initialise PyGame, and set some constants
pygame.init()

# Initialize audio
mixer = pygame.mixer
mixer.init()

# Loading the song for pygame to play
mixer.music.load(SONG_FILE)

# Setting the volume
mixer.music.set_volume(0.7)

# Start playing the song
# Create screen for showing viusalisation
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Audio Visualiser")

# Keep track of which packet is being rendered on screen
cur_packet_index = 0

# While game is running, for every frame,
mixer.music.play()
while cur_packet_index < len(interpolated):

    # Store events to process quit and KeyDown events
    events = pygame.event.get()

    # Handle exit event
    for event in events:
        # Let user exit
        if event.type == pygame.QUIT:
            sys.exit()

    # Fill the screen with BG_COLOR
    screen.fill(BG_COLOR)

    # Show every bar
    for ind, intensity in enumerate(interpolated[cur_packet_index]):
        pygame.draw.rect(screen, CELL_COLOR, pygame.Rect(
            PADDING + ind*(PADDING + BLOCK_SIZE), 690, BLOCK_SIZE, -int(intensity * 660)))

    # Update the display
    pygame.display.update()

    # Tick the display as per FPS, and move to next packet
    pygame.time.Clock().tick(FPS)
    cur_packet_index += 1
