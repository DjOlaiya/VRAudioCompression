import scipy.io.wavfile
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import math
import os


# # # # # # # # # # # # # # # # # # # # # # # # # #
# 1) Read in Wav File and Compression Parameters
Thresh_Val=120
c_Ratio=0
k_wide=0
att=0
rel=0
# # # # # # # # # # # # # # # # # # # # # # # # # #
# print("* Reading in .wav")
A="*Reading in .wav*"
if os.path.exists("compressed_track.wav"):
    os.remove("compressed_track.wav")

# Read in the sample rate and audio samples/amplitudes of the wav file
if os.path.exists("Sample_drum_short.wav"):
    sample_rate, audio = scipy.io.wavfile.read("Sample_drum_short.wav")

# Calculate audio array type, and length of the array
audio_type = audio.dtype
length = len(audio)

# Read in User-Inputted Compression Parameter Values
comp_threshold=1      # [-50, 0]
comp_ratio =2        # [1, 50]
knee_width = 10      # [0, 20]
attack = .3   # between 0 & 0.5
release =  .1    # between 0.001 & 2.5
"""
# # # # # # # # # # # # # # # # # # # # # # # # # #
# 2) Convert Amplitude to Decibels, and normalize to 0
# # # # # # # # # # # # # # # # # # # # # # # # # #
# print("* Converting Amplitude to Decibels")
B="* Converting Amplitude to Decibels"
# Create Intermediate Arrays as Floats, to avoid rounding/runoff errors
audio_db = np.zeros((length, 2), dtype=np.float64)
audio_db_norm = np.zeros((length, 2), dtype=np.float64)

# Convert audio amplitude values in decibel
# As log(0) is undefined, account for this case
for i in range(1, length, 1):
    for j in range(2):
        if audio[i, j] == 0:
            audio_db[i, j] = 0
        else:
            audio_db[i, j] = 20 * math.log10(abs(audio[i, j]))

# print("* Normalizing Decibels to 0")
C="* Normalizing Decibels to 0"
# Normalize the dB values to 0, using the theoretical limit for 16-bit audio, 96
for i in range(0, length, 1):
    for j in range(2):
        audio_db_norm[i, j] = audio_db[i, j] - 96

# # # # # # # # # # # # # # # # # # # # # # # # # #
# 3) Apply Compression
# # # # # # # # # # # # # # # # # # # # # # # # # #
# print("* Applying Compression")
D="* Applying Compression"

# define parameter-associated terms to reduce computations during compression
knee_width_half = knee_width / 2
knee_width_double = knee_width * 2
comp_ratio_inverse = 1 / comp_ratio

# Create Intermediate Arrays as Floats, to avoid rounding/runoff errors
audio_comp = np.zeros((length, 2), dtype=np.float64)
audio_gain = np.zeros((length, 2), dtype=np.float64)

# Compress audio, one sample at a time
for i in range(0, length, 1):
    # Sum left and right channels of the sample, to maintain left/right balance in final compressed file
    avg_sum = (audio_db_norm[i, 0] + audio_db_norm[i, 1]) / 2
    # If the sum is less than the lower limit of the threshold/knee cutoff, no compression is applied
    if avg_sum < (comp_threshold - knee_width_half):
        audio_comp[i, 0] = audio_db_norm[i, 0]
        audio_comp[i, 1] = audio_db_norm[i, 1]
    # If the sum is greater than the upper limit of the threshold/knee cutoff, full compression is applied
    elif avg_sum > (comp_threshold + knee_width_half):
        audio_comp[i, 0] = comp_threshold + ((audio_db_norm[i, 0] - comp_threshold) / comp_ratio)
        audio_comp[i, 1] = comp_threshold + ((audio_db_norm[i, 1] - comp_threshold) / comp_ratio)
    # Else the sum falls within the threshold/knee range,
    # Compression is applied in relation to where in the curve it falls
    else:
        audio_comp[i, 0] = audio_db_norm[i, 0] + (((comp_ratio_inverse - 1)
                                                  * (audio_db_norm[i, 0] - comp_threshold
                                                     + knee_width_half)**2) / knee_width_double)
        audio_comp[i, 1] = audio_db_norm[i, 1] + (((comp_ratio_inverse - 1)
                                                  * (audio_db_norm[i, 1] - comp_threshold
                                                     + knee_width_half)**2) / knee_width_double)

    # Audio_gain represents the amount of gain to be applied to the original signal
    audio_gain[i, 0] = audio_comp[i, 0] - audio_db_norm[i, 0]
    audio_gain[i, 1] = audio_comp[i, 1] - audio_db_norm[i, 1]

# # # # # # # # # # # # # # # # # # # # # # # # # #
# 4) Gain Smoothing
# # # # # # # # # # # # # # # # # # # # # # # # # #
# print("* Gain Smoothing")
E="* Gain Smoothing"
# The gain reduction calculated in step 3 is smoothed in this stage,
# This is to ensure a realistic, and pleasing to the listener, gain reduction curve

# Create Intermediate Array as Float, to avoid rounding/runoff errors
audio_smooth = np.zeros((length, 2), dtype=np.float64)

# Assign the first sample, as curving can not be carried out on the first sample
audio_smooth[0, 0] = audio_gain[0, 0]

# define parameter-associated terms to reduce computations during compression
alphaA = np.exp(-math.log10(9) / (sample_rate * attack))
alphaR = np.exp(-math.log10(9) / (sample_rate * release))
alphaA_inv = 1 - alphaA
alphaR_inv = 1 - alphaR

for i in range(1, length, 1):
    # Sum left and right channels of the sample, to maintain left/right balance in final compressed file
    avg_sum = (audio_gain[i, 0] + audio_gain[i, 1]) / 2
    # Sum previous sample's amplitude, to ensure smooth gain reduction over time
    avg_sum_prev = (audio_smooth[i-1, 0] + audio_smooth[i-1, 1]) / 2

    # If the sum of the current sample > previous sample, then it is in the 'Release' portion of the window
    if avg_sum > avg_sum_prev:
        audio_smooth[i, 0] = (alphaR * audio_smooth[i - 1, 0]) + (alphaR_inv * audio_gain[i, 0])
        audio_smooth[i, 1] = (alphaR * audio_smooth[i - 1, 1]) + (alphaR_inv * audio_gain[i, 1])
    # If the sum of the current sample < previous sample, then it is in the 'Attack' portion of the window
    else:
        audio_smooth[i, 0] = (alphaA * audio_smooth[i - 1, 0]) + (alphaA_inv * audio_gain[i, 0])
        audio_smooth[i, 1] = (alphaA * audio_smooth[i - 1, 1]) + (alphaA_inv * audio_gain[i, 1])


# # # # # # # # # # # # # # # # # # # # # # # # # #
# 5) Apply Make Up Gain
# # # # # # # # # # # # # # # # # # # # # # # # # #
# print("* Applying Make Up Gain")
F="* Applying Make Up Gain"
# After compression and smoothing, the audio values have been condensed
# This results in a quieter signal than the original
# To account for this, makeup gain is applied to the values in the array
# This will result in the compressed file being approximately the same volume as the original

# Create Intermediate Array as Float, to avoid rounding/runoff errors
audio_makeup = np.zeros((length, 2), dtype=np.float64)

# The makeup value is the greatest amount of compression applied to the original signal
# This is represented as the smallest value in audio_smooth
makeup = np.min(audio_smooth)

# Add the makeup value to all terms in the array
for i in range(0, length, 1):
    for j in range(2):
        audio_makeup[i, j] = audio_smooth[i, j] - makeup

# # # # # # # # # # # # # # # # # # # # # # # # # #
# 6) Calculate Linear Gain and Apply to Original Signal, Write Array to New .wav File
# # # # # # # # # # # # # # # # # # # # # # # # # #
# print("* Converting Decibels to Amplitude")
G="* Converting Decibels to Amplitude"

# Create Intermediate Arrays as Floats, to avoid rounding/runoff errors
audio_lin = np.zeros((length, 2), dtype=np.float64)
final_comp_audio = np.zeros((length, 2), dtype=audio_type)

# Convert array values from decibels back into amplitude
for i in range(0, length, 1):
    for j in range(2):
        audio_lin[i, j] = np.float(10.0**(audio_makeup[i, j]/20.0))

        # Multiply original signal by compression values
        # This will obtain the Final compressed audio array
        final_comp_audio[i, j] = audio[i, j] * audio_lin[i, j]


final_difference = np.zeros((length, 2), dtype=np.float64)
for i in range(0, length, 1):
    for j in range(2):
        final_difference[i, j] = np.float(final_comp_audio[i, j]) - np.float(audio[i, j])


# Write compressed array to new .wav file
# print("* Writing New .wav")
H="* Writing New .wav"
# scipy.io.wavfile.write("compressed_track.wav", sample_rate, final_comp_audio)


# # # # # # # # # # # # # # # # # # # # # # # # # #
# 7) Create Graphs
# # # # # # # # # # # # # # # # # # # # # # # # # #
# print("* Calculating Graph Info for Printing")
I="* Calculating Graph Info for Printing"
final_audio_db = np.zeros((length, 2), dtype=np.float64)
final_audio_db_norm = np.zeros((length, 2), dtype=np.float64)
for i in range(1, length, 1):
    for j in range(2):
        if final_comp_audio[i, j] == 0:
            final_audio_db[i, j] = 0
        else:
            final_audio_db[i, j] = 20 * math.log10(abs(float(final_comp_audio[i, j])))

        final_audio_db_norm[i, j] = final_audio_db[i, j] - 96

final_difference_db = np.zeros((length, 2), dtype=np.float64)
final_difference_db_norm = np.zeros((length, 2), dtype=np.float64)
for i in range(0, length, 1):
    for j in range(2):
        final_difference_db[i, j] = np.float(final_audio_db[i, j]) - np.float(audio_db[i, j])

        final_difference_db_norm[i, j] = np.float(audio_db_norm[i, j]) - np.float(final_audio_db_norm[i, j])

# print("* Printing Graphs")
J="* Printing Graphs"
gs = gridspec.GridSpec(3, 1)
max_y = 100
plt.figure()
ax = plt.subplot(gs[0, :])
plt.plot(audio_db_norm[4000:7000, 1])
# label the axes
plt.ylim([-15, 0])
plt.ylabel("Amplitude")
plt.xlabel("Time (samples)")
# Show the major grid lines with dark grey lines
plt.grid(b=True, which='major', color='#666666', linestyle='-')

# Show the minor grid lines with very faint and almost transparent grey lines
plt.minorticks_on()
plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.5)

plt.axhline(y=comp_threshold, color='r', linestyle='-')
# set the title
plt.title("Original")


ax = plt.subplot(gs[1, :])
plt.plot(final_audio_db_norm[4000:7000, 1])
# label the axes
plt.ylabel("Amplitude")
plt.ylim([-15, 0])
plt.xlabel("Time (samples)")
# Show the major grid lines with dark grey lines
plt.grid(b=True, which='major', color='#666666', linestyle='-')

# Show the minor grid lines with very faint and almost transparent grey lines
plt.minorticks_on()
plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.5)
# set the title
plt.title("Compressed")


ax = plt.subplot(gs[2, :])
plt.plot(final_difference_db_norm[:, 1])
# label the axes
plt.ylabel("Amplitude")
plt.ylim([-11, 0])
plt.xlabel("Time (samples)")
# set the title
plt.title("Difference")
# Show the major grid lines with dark grey lines
plt.grid(b=True, which='major', color='#666666', linestyle='-')

# Show the minor grid lines with very faint and almost transparent grey lines
plt.minorticks_on()
plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.5)
# display the plot
plt.show()

"""
