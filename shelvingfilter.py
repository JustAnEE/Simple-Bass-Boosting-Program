import numpy as np
from scipy.signal import lfilter
from scipy.io import wavfile


# -- Define all functions to be used in this implementation
def low_shelf_params(K, G):
    b_0 = 1 + np.sqrt(2 * G) * K + G * K ** 2
    b_1 = -2 + 2 * G * K ** 2
    b_2 = 1 - np.sqrt(2 * G) * K + G * K ** 2

    a_0 = 1 + np.sqrt(2) * K + K ** 2
    a_1 = -2 + 2 * K ** 2
    a_2 = 1 - np.sqrt(2) * K + K ** 2

    b = np.array([b_0, b_1, b_2])
    a = np.array([a_0, a_1, a_2])

    return b, a


def low_shelf(data, N, K, G):
    b, a = low_shelf_params(K, G)

    # -- Apply shelving filter to input data channel
    bass_boosted_data = lfilter(b, a, data, axis=0)  # Wouldn't work without axis = 0 ??
    bass_boosted_data = np.asarray(bass_boosted_data, dtype=np.float32)

    return bass_boosted_data


# -- Read in input song again
fs, song = wavfile.read('githubsample.wav')

# -- Length of one channel
N = len(song)

# -- Cutoff frequency
f_c = 65  # I liked the performance of this cutoff better for this implementation

# -- Gain
gain = 6.5  # Again I'd keep this lower than 10, it can be pushed higher than the first implementation though

# -- Nyquist frequency
f_N = (1 / 2) * fs

# -- Normalized Cutoff
normal_cutoff = (f_c / f_N) * np.pi  # This pi factor is magic that makes this work. I have no idea why this fixed it
# considering that normalized frequencies would have pi factors divided out :/
# -- Adjust for frequency warp
K = np.tan(normal_cutoff / 2)

# -- Check if song is mono and create stereo file if it is
if np.size(np.shape(song)) == 1:
    left_channel = song
    right_channel = song

    song = np.zeros((N, 2), dtype=np.float32)

    song[:, 0] = left_channel
    song[:, 1] = right_channel

# -- Proceed with stereo implementation

left_channel = low_shelf(song[:, 0], N, K, gain)
right_channel = low_shelf(song[:, 1], N, K, gain)

# -- Construct stereo audio
new_song = np.zeros((N, 2), dtype=np.float32)
new_song[:, 0] = left_channel
new_song[:, 1] = right_channel

# -- Write new audio
wavfile.write('githubsample_shelved.wav', fs, new_song)

