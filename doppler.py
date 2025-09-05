import numpy as np

def create_spectrum_graph(freqs, spectrum_before, spectrum_after):
    """Create ASCII art graph for frequency spectrum"""
    print("\nDoppler Compensation Spectrum Analysis")
    print("=" * 60)
    
    width = 60
    height = 20
    
    positive_mask = freqs >= 0
    freqs_pos = freqs[positive_mask]
    spectrum_before_pos = spectrum_before[positive_mask]
    spectrum_after_pos = spectrum_after[positive_mask]
    
    max_val = max(np.max(spectrum_before_pos), np.max(spectrum_after_pos))
    spectrum_before_norm = spectrum_before_pos / max_val
    spectrum_after_norm = spectrum_after_pos / max_val
    
    grid_before = [[' ']*width for _ in range(height)]
    grid_after = [[' ']*width for _ in range(height)]
    
    step = len(freqs_pos) // width
    for i in range(0, len(freqs_pos), step):
        x = i // step
        y_before = int(spectrum_before_norm[i] * (height - 1))
        y_after = int(spectrum_after_norm[i] * (height - 1))
        y_before = height - 1 - y_before
        y_after = height - 1 - y_after
        if 0 <= x < width and 0 <= y_before < height:
            grid_before[y_before][x] = '*'
        if 0 <= x < width and 0 <= y_after < height:
            grid_after[y_after][x] = '+'
    
    print("\nSpectrum BEFORE Doppler Correction:")
    print("Magnitude")
    for i in range(height):
        mag_val = max_val * (height - 1 - i) / (height - 1)
        print(f"{mag_val:6.1f} |", end="")
        print(''.join(grid_before[i]))
    print("       " + ''.join([f"{freqs_pos[int(j*len(freqs_pos)/width)]:6.0f}" for j in range(0, width, 10)]))
    print("       Frequency (Hz)")
    
    print("\nSpectrum AFTER Doppler Correction:")
    print("Magnitude")
    for i in range(height):
        mag_val = max_val * (height - 1 - i) / (height - 1)
        print(f"{mag_val:6.1f} |", end="")
        print(''.join(grid_after[i]))
    print("       " + ''.join([f"{freqs_pos[int(j*len(freqs_pos)/width)]:6.0f}" for j in range(0, width, 10)]))
    print("       Frequency (Hz)")


if __name__ == "__main__":
    fs = 1000
    N = 1024 
    t = np.arange(N) / fs
    freq_carrier = 100
    freq_offset = 50  

    signal = np.exp(1j * 2 * np.pi * freq_carrier * t)
 
    rx = signal * np.exp(1j * 2 * np.pi * freq_offset * t)

    rx_corrected = rx * np.exp(-1j * 2 * np.pi * freq_offset * t)
    
    freqs = np.fft.fftfreq(N, d=1/fs)
    spectrum_before = np.abs(np.fft.fft(rx))
    spectrum_after = np.abs(np.fft.fft(rx_corrected))
    
    create_spectrum_graph(freqs, spectrum_before, spectrum_after)

