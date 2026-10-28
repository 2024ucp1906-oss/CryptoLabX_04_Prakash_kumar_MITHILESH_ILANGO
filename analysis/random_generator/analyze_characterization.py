import numpy as np
from collections import Counter

files = {
    "Linux /dev/urandom": "linux_urandom.bin",
    "OpenSSL rand": "openssl_rand.bin",
    "Windows CNG / .NET": "windows_dotnet.bin"
}

def analyze_dataset(label, filepath):
    with open(filepath, 'rb') as f:
        raw_bytes = f.read()
    
    data = np.frombuffer(raw_bytes, dtype=np.uint8)
    total_bytes = len(data)
    
    byte_counts = np.bincount(data, minlength=256)
    bits = np.unpackbits(data)
    ones_ratio = np.count_nonzero(bits) / len(bits)
    
    x_i = data[:-1].astype(np.float64)
    x_i1 = data[1:].astype(np.float64)
    mean_x = np.mean(data)
    serial_corr = np.sum((x_i - mean_x) * (x_i1 - mean_x)) / np.sum((data - mean_x)**2)
    
    ngrams = [raw_bytes[i:i+4] for i in range(len(raw_bytes) - 3)]
    ngram_counts = Counter(ngrams)
    max_repeat = max(ngram_counts.values())
    
    print(f"=== {label} ===")
    print(f"Total Bytes Analyzed       : {total_bytes:,}")
    print(f"Bit 1 Ratio                : {ones_ratio:.6f} (Ideal: 0.500000)")
    print(f"Serial Correlation (lag-1) : {serial_corr:.6f} (Ideal: 0.000000)")
    print(f"Max 4-Byte Sequence Repeat : {max_repeat} time(s)\n")

for label, path in files.items():
    analyze_dataset(label, path)
