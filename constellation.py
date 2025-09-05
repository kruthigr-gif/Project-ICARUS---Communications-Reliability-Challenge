import numpy as np

def create_simple_constellation_display(rx_symbols, title, snr_db):
    """Create ASCII constellation diagram for BPSK"""
    print(f"\n{title}")
    print("=" * 80)
    
    width, height = 60, 25
    x_vals = rx_symbols.real
    y_vals = rx_symbols.imag
    
    x_min, x_max = -2, 2
    y_min, y_max = -1, 1
    
    x_bins = np.linspace(x_min, x_max, width)
    y_bins = np.linspace(y_min, y_max, height)
    
    bin_counts = np.zeros((height, width))
    
    for x, y in zip(x_vals, y_vals):
        x_idx = np.digitize(x, x_bins) - 1
        y_idx = np.digitize(y, y_bins) - 1
        
        if 0 <= x_idx < width and 0 <= y_idx < height:
            bin_counts[y_idx, x_idx] += 1
    
    print("Q (Imag)")
    print("↑")
    for i in range(height):
        y_val = y_bins[height - 1 - i]
        print(f"{y_val:5.2f}|", end="")
        for j in range(width):
            count = bin_counts[height - 1 - i, j]
            if count == 0:
                print(" ", end="")
            elif count <= 2:
                print("·", end="")
            elif count <= 5:
                print("o", end="")
            elif count <= 10:
                print("O", end="")
            else:
                print("●", end="")
        print()
    print(" " * 6 + "".join(f"{x_bins[k]:5.1f}" if k % 8 == 0 else " " * 5 for k in range(width)))
    print(" " * 6 + "→ I (Real)")
    print("\nLegend: ·=1-2 pts, o=3-5 pts, O=6-10 pts, ●=11+ pts")

def generate_bpsk_constellation(snr_db, num_symbols=1000):
    bits = np.random.randint(0, 2, num_symbols)
    symbols = 2 * bits - 1  

    snr_linear = 10 ** (snr_db / 10)
    noise_std = np.sqrt(1 / (2 * snr_linear))
    noise = noise_std * (np.random.randn(num_symbols) + 1j * 0) 
    
    rx_symbols = symbols + noise
    return rx_symbols, symbols

if __name__ == "__main__":
    snr_values = [5, 10, 15, 20]
    for snr in snr_values:
        rx_sym, sym = generate_bpsk_constellation(snr)
        create_simple_constellation_display(rx_sym, f"BPSK Constellation at {snr} dB SNR", snr)
