
import math

snr_db = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
ber_uncoded = [1e-1, 8e-2, 5e-2, 2.5e-2, 1e-2, 4e-3, 1e-3, 4e-4, 1e-4, 5e-5, 1e-5]
ber_coded = [5e-2, 1.2e-2, 4e-3, 1e-3, 2e-4, 2e-5, 5e-6, 2e-6, 7e-7, 2e-7, 8e-8]

def create_ascii_graph(snr_values, ber_values, title, symbol='*'):
    """Create ASCII art graph for BER vs SNR"""
    print(f"\n{title}")
    print("=" * 60)
    

    width = 50
    height = 20
    

    log_ber = [math.log10(ber) for ber in ber_values]
    min_log_ber = min(log_ber)
    max_log_ber = max(log_ber)
    
  
    grid = [[' ' for _ in range(width)] for _ in range(height)]

    for i, (snr, log_ber_val) in enumerate(zip(snr_values, log_ber)):
        x = int((snr - min(snr_values)) / (max(snr_values) - min(snr_values)) * (width - 1))
        y = int((log_ber_val - min_log_ber) / (max_log_ber - min_log_ber) * (height - 1))
        y = height - 1 - y  # Flip Y axis
        if 0 <= x < width and 0 <= y < height:
            grid[y][x] = symbol
    
   
    print("BER (log10)")
    for i in range(height):
        ber_val = 10**(max_log_ber - (max_log_ber - min_log_ber) * i / (height - 1))
        print(f"{ber_val:.0e} |", end="")
        for j in range(width):
            print(grid[i][j], end="")
        print()
    

    print("     ", end="")
    for i in range(0, width, 5):
        snr_val = min(snr_values) + (max(snr_values) - min(snr_values)) * i / (width - 1)
        print(f"{snr_val:4.0f}", end="")
    print("\n     SNR (dB)")

print("BER Analysis Results")
print("=" * 50)
print(f"{'SNR (dB)':<10} {'Uncoded BER':<15} {'Coded BER':<15}")
print("-" * 50)

for i in range(len(snr_db)):
    print(f"{snr_db[i]:<10} {ber_uncoded[i]:<15.2e} {ber_coded[i]:<15.2e}")

create_ascii_graph(snr_db, ber_uncoded, "Uncoded BER vs SNR", '*')
create_ascii_graph(snr_db, ber_coded, "Coded BER vs SNR", '+')

print("\nBER Comparison (Uncoded: *, Coded: +)")
print("=" * 60)

width = 50
height = 20
grid = [[' ' for _ in range(width)] for _ in range(height)]

log_ber_uncoded = [math.log10(ber) for ber in ber_uncoded]
log_ber_coded = [math.log10(ber) for ber in ber_coded]
all_log_ber = log_ber_uncoded + log_ber_coded
min_log_ber = min(all_log_ber)
max_log_ber = max(all_log_ber)

for i, (snr, log_ber_val) in enumerate(zip(snr_db, log_ber_uncoded)):
    x = int((snr - min(snr_db)) / (max(snr_db) - min(snr_db)) * (width - 1))
    y = int((log_ber_val - min_log_ber) / (max_log_ber - min_log_ber) * (height - 1))
    y = height - 1 - y
    if 0 <= x < width and 0 <= y < height:
        grid[y][x] = '*'

for i, (snr, log_ber_val) in enumerate(zip(snr_db, log_ber_coded)):
    x = int((snr - min(snr_db)) / (max(snr_db) - min(snr_db)) * (width - 1))
    y = int((log_ber_val - min_log_ber) / (max_log_ber - min_log_ber) * (height - 1))
    y = height - 1 - y
    if 0 <= x < width and 0 <= y < height:
        if grid[y][x] == '*':
            grid[y][x] = '⊕' 
        else:
            grid[y][x] = '+'

print("BER (log10)")
for i in range(height):
    ber_val = 10**(max_log_ber - (max_log_ber - min_log_ber) * i / (height - 1))
    print(f"{ber_val:.0e} |", end="")
    for j in range(width):
        print(grid[i][j], end="")
    print()

print("     ", end="")
for i in range(0, width, 5):
    snr_val = min(snr_db) + (max(snr_db) - min(snr_db)) * i / (width - 1)
    print(f"{snr_val:4.0f}", end="")
print("\n     SNR (dB)")

print("\nLegend: * = Uncoded, + = Coded, ⊕ = Overlap")

print("\nSummary:")
print(f"Best uncoded BER: {min(ber_uncoded):.2e} at SNR = {snr_db[ber_uncoded.index(min(ber_uncoded))]} dB")
print(f"Best coded BER: {min(ber_coded):.2e} at SNR = {snr_db[ber_coded.index(min(ber_coded))]} dB")

print("\nCoding Gain Analysis:")
for target_ber in [1e-3, 1e-4, 1e-5]:
  
    uncoded_snr = None
    coded_snr = None
    
    for i in range(len(ber_uncoded)):
        if ber_uncoded[i] <= target_ber:
            uncoded_snr = snr_db[i]
            break
    
    for i in range(len(ber_coded)):
        if ber_coded[i] <= target_ber:
            coded_snr = snr_db[i]
            break
    
    if uncoded_snr is not None and coded_snr is not None:
        coding_gain = uncoded_snr - coded_snr
        print(f"At BER = {target_ber:.0e}: Coding gain = {coding_gain:.1f} dB")
