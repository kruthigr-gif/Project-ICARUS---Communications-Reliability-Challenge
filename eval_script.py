import os
import numpy as np
import json
from scipy.signal import lfilter
def _find_ground_truth_bits(dirpath, meta):

    for name in [
        "tx_bits.npy", "gt_bits.npy", "truth_bits.npy", "labels.npy",
        "bits.npy", "ref_bits.npy", "ground_truth.npy"
    ]:
        p = os.path.join(dirpath, name)
        if os.path.isfile(p):
            try:
                return (np.load(p).astype(np.uint8) & 1)
            except Exception:
                pass

    for key in [
        "ground_truth_bits", "ground_truth", "tx_bits", "gt_bits",
        "bits", "truth_bits", "labels"
    ]:
        if isinstance(meta.get(key), list):
            try:
                return (np.array(meta[key], dtype=np.uint8) & 1)
            except Exception:
                continue
      
        if isinstance(meta.get(key), dict):
            inner = meta[key]
            for inner_key in ["bits", "data", "values"]:
                if isinstance(inner.get(inner_key), list):
                    try:
                        return (np.array(inner[inner_key], dtype=np.uint8) & 1)
                    except Exception:
                        pass
    for k, v in meta.items():
        if isinstance(v, list) and len(v) > 0:
            arr = np.array(v)
            if arr.dtype.kind in ("i", "u") and np.isin(arr, [0, 1]).all():
                try:
                    return (arr.astype(np.uint8) & 1)
                except Exception:
                    pass
    return None


def _decode_if_missing(dirpath, meta):
    decoded_path = os.path.join(dirpath, "decoded_bits.npy")
    if os.path.isfile(decoded_path):
        return (np.load(decoded_path).astype(np.uint8) & 1)
    rx_path = os.path.join(dirpath, "rx.npy")
    if not os.path.isfile(rx_path):
        return None
    rx = np.load(rx_path)
    sps = int(meta.get("samples_per_symbol", 8))
    pulse = np.ones(sps)
    filtered = lfilter(pulse, 1, rx)
    energies = [np.sum(np.abs(filtered[i::sps])) for i in range(sps)]
    best_offset = int(np.argmax(energies))
    symbols = filtered[best_offset::sps]
    decoded = (symbols > 0).astype(np.uint8)
    np.save(decoded_path, decoded)
    print(f"Decoded and saved: {decoded_path}")
    return decoded


def evaluate_folder(dirpath):
    decoded_file = os.path.join(dirpath, "decoded_bits.npy")
    meta_file = os.path.join(dirpath, "meta.json")
    if not os.path.isfile(meta_file):
        return None
    with open(meta_file, 'r') as f:
        meta = json.load(f)
    if os.path.isfile(decoded_file):
        decoded = (np.load(decoded_file).astype(np.uint8) & 1)
    else:
        decoded = _decode_if_missing(dirpath, meta)
        if decoded is None:
            return None
    gt_bits = _find_ground_truth_bits(dirpath, meta)
    if gt_bits is None or gt_bits.size == 0:
        return None
    min_len = min(len(decoded), len(gt_bits))
    errors = np.sum(decoded[:min_len] != gt_bits[:min_len])
    ber = errors / min_len if min_len > 0 else float('nan')
    fer = 1 if errors > 0 else 0
    return ber, fer

def evaluate_all_folders(dataset_root):
    bers = []
    fers = []
    for root, _, files in os.walk(dataset_root):
        if ("meta.json" in files) and ("decoded_bits.npy" in files or "rx.npy" in files):
            result = evaluate_folder(root)
            if result is not None:
                ber, fer = result
                bers.append(ber)
                fers.append(fer)
                rel = os.path.relpath(root, dataset_root).replace(os.sep, "/")
                print(f"cubesat_dataset/{rel}: BER={ber:.2e} FER={int(fer)}")
    if bers:
        print(f"\nOverall mean BER: {np.mean(bers):.2e}")
        print(f"Overall mean FER: {np.mean(fers):.2e}")
    else:
        print("No valid results found to evaluate.")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    preferred_root = os.path.join(script_dir, "cubesat_dataset")
    dataset_root = preferred_root if os.path.isdir(preferred_root) else script_dir
    evaluate_all_folders(dataset_root)
