#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import sounddevice as sd
import sys

def main():
    FS = 44100  # Sampling rate = 44.1 kHz
    CARRIER = 1000
    HALF_BANDWIDTH = 100
    DURATION = 2.0
    FILENAME = None
    PLOT_DURATION = 0.2
    play_audio = False

    argc = len(sys.argv)
    if argc > 1:
        CARRIER = float(sys.argv[1])
    if argc > 2:
        HALF_BANDWIDTH = float(sys.argv[2])
    if argc > 3:
        PLOT_DURATION = float(sys.argv[3])
        DURATION = max(DURATION, PLOT_DURATION)
        play_audio = True
        #FILENAME = "_"
    if argc > 4:
        FILENAME = sys.argv[4]

    LOW = CARRIER - HALF_BANDWIDTH 
    HIGH = CARRIER + HALF_BANDWIDTH 

    def generate_narrowband_noise(fs, duration, lowcut, highcut):
        num_samples = int(fs * duration)
        white_noise = np.random.normal(0, 1, num_samples)
        # Transform to frequency domain
        fft_vals = np.fft.rfft(white_noise)
        frequencies = np.fft.rfftfreq(num_samples, d=1/fs)
        # Zero out frequencies outside the chosen band
        fft_vals[(frequencies < lowcut) | (frequencies > highcut)] = 0
        # Transform back to time domain
        return np.fft.irfft(fft_vals, n=num_samples)

    noise_signal = generate_narrowband_noise(FS, DURATION, LOW, HIGH)

    if play_audio:
        noise_normalized = noise_signal / np.max(np.abs(noise_signal))
        audio_data = np.int16(noise_normalized * 32767)
        try:
            sd.play(noise_normalized, FS)
            sd.wait()
        except KeyboardInterrupt:
            pass
        if FILENAME is not None:
            if not FILENAME.lower().endswith('.wav'):
                FILENAME = FILENAME.lower() + '.wav'
            # Normalize and convert to 16-bit integer format (standard for WAV)
            # This prevents clipping and ensures audio compatibility

            wavfile.write(FILENAME, FS, audio_data)
            print(f"Success: Audio saved to '{FILENAME}'")

    # Create an array of time points for each sample
    time_axis = np.arange(len(noise_signal)) / FS

    plt.figure(figsize=(12, 6))
    max_sample = int(FS * PLOT_DURATION)
    plt.plot(time_axis[:max_sample], noise_signal[:max_sample], color='blue', linewidth=1)

    # Add titles and labels
    plt.title(f"Narrowband Noise ({round(LOW)}{'\u2013'}{round(HIGH)} Hz)")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.xlim([0, PLOT_DURATION])
    plt.grid(True, linestyle='-', alpha=0.5)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
