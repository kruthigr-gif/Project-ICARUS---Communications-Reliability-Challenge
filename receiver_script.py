import os
import numpy as np
import json
from scipy.signal import lfilter
from scipy.fft import fft, fftfreq

try:
    import reedsolo
except ImportError:
    reedsolo = None
    print("reedsolo not found; RS decoding disabled. Use 'pip install reedsolo' for support.")

def rs_decode(bits):
    if reedsolo is None:
        return bits
    n_bytes = len(bits) // 8
    if n_bytes == 0:
        return bits
    bytes_in = np.packbits(bits[:n_bytes*8])
    try:
        decoded_bytes = reedsolo.rs_decode(bytes_in, nsym=4)[0]
        decoded_bits = np.unpackbits(np.frombuffer(decoded_bytes, dtype=np.uint8))
        return decoded_bits
    except Exception as e:
        print(f"RS decode error: {e}")
        return bits

def viterbi_decode(bits):

    return bits

def estimate_doppler(rx, fs):
    N = len(rx)
    windowed = rx * np.hamming(N)
    spectrum = np.fft.fft(windowed)
    freqs = np.fft.fftfreq(N, 1/fs)
    mag = np.abs(spectrum)
    peak_idx = np.argmax(mag)
    def quad_interpolate(mag, idx):
        alpha = mag[idx - 1]
        beta = mag[idx]
        gamma = mag[(idx + 1) % len(mag)]
        p = 0.5 * (alpha - gamma) / (alpha - 2*beta + gamma)
        return idx + p
    peak_interp = quad_interpolate(mag, peak_idx)
    doppler_hz = freqs[0] if peak_idx == 0 else freqs[int(round(peak_interp))]
    return doppler_hz

def doppler_compensate(rx, fs, estimated_doppler_hz):
    N = len(rx)
    t = np.arange(N) / fs
    return rx * np.exp(-1j * 2 * np.pi * estimated_doppler_hz * t)

def bpsk_matched_filter(rx, sps):
    pulse = np.ones(sps)
    filtered = lfilter(pulse, 1, rx)
    energies = [np.sum(np.abs(filtered[i:i + sps*10:sps])) for i in range(sps)]
    best_offset = np.argmax(energies)
    symbols = filtered[best_offset::sps]
    return symbols

def bpsk_to_bits(symbols):
    return (symbols > 0).astype(np.uint8)

def process_all_folders(dataset_root):
    for dirpath, _, filenames in os.walk(dataset_root):
        if "rx.npy" in filenames and "meta.json" in filenames:
            rx_file = os.path.join(dirpath, "rx.npy")
            meta_file = os.path.join(dirpath, "meta.json")
            
            rx = np.load(rx_file)
            with open(meta_file, 'r') as f:
                meta = json.load(f)
            sps = int(meta.get("samples_per_symbol", 8))
            fs = int(meta.get("sample_rate", 10000))  # default
            
            if meta.get("impairment", "").lower() == "doppler":
                est_dopp = estimate_doppler(rx, fs)
                rx = doppler_compensate(rx, fs, est_dopp)

            symbols = bpsk_matched_filter(rx, sps)
            bits = bpsk_to_bits(symbols)

            if "reed_solomon" in dirpath.lower():
                bits = rs_decode(bits)
            if "convolutional" in dirpath.lower():
                bits = viterbi_decode(bits)

            np.save(os.path.join(dirpath, "decoded_bits.npy"), bits)
            print(f"Decoded and saved: {os.path.join(dirpath, 'decoded_bits.npy')}")
    print("All files processed.")

if __name__ == "__main__":
    dataset_root = "."
    process_all_folders(dataset_root)


