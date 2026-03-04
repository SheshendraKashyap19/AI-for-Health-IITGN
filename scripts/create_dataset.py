#loading->filtering->loading events->assign labels->creating dataset

%%writefile create_dataset.py
def load_signal(file_path):
    import pandas as pd
    timestamps = []
    values = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
    data_start = 0
    for i, line in enumerate(lines):
        if line.strip() == "Data:":
            data_start = i + 1
            break
    for line in lines[data_start:]:
        if not line.strip():
            continue
        parts = line.strip().split(";")
        if len(parts) != 2:
            continue
        timestamps.append(parts[0].strip())
        values.append(float(parts[1].strip()))
    df = pd.DataFrame({
        "timestamp": pd.to_datetime(timestamps, format="%d.%m.%Y %H:%M:%S,%f"),
        "value": values
    })
    df.set_index("timestamp", inplace=True)
    return df



def bandpass_filter(signal, fs):
    from scipy.signal import butter, filtfilt
    low = 0.17
    high = 0.4
    order = 4
    nyquist = 0.5 * fs
    low = low / nyquist
    high = high / nyquist
    b, a = butter(order, [low, high], btype='band')
    filtered = filtfilt(b, a, signal)
    return filtered



def load_events(file_path):
    import pandas as pd
    events = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if ";" in line and "-" in line:
            parts = line.strip().split(";")
            time_range = parts[0].strip()
            label = parts[2].strip()
            start_str, end_str = time_range.split("-")
            start_time = pd.to_datetime(start_str, format="%d.%m.%Y %H:%M:%S,%f")
            end_time_only = pd.to_datetime(end_str, format="%H:%M:%S,%f")
            end_time = end_time_only.replace(
                year=start_time.year,
                month=start_time.month,
                day=start_time.day
            )
            events.append((start_time, end_time, label))
    return events


def assign_label(window_start, window_end, events):
    window_duration = (window_end - window_start).total_seconds()
    for start, end, label in events:
        overlap = (min(window_end, end) - max(window_start, start)).total_seconds()
        if overlap > 0:
            if overlap / window_duration > 0.5:
                return label
    return "Normal"


def create_dataset(in_dir, out_dir):
    import os
    import pandas as pd
    import numpy as np

    print("Creating dataset...")
    base_path = os.path.join(in_dir, "AP01")
    nasal = load_signal(os.path.join(base_path, "Flow - 30-05-2024.txt"))
    events = load_events(os.path.join(base_path, "Flow Events - 30-05-2024.txt"))
    fs = 32
    filtered_signal = bandpass_filter(nasal["value"].values, fs)
    window_size = 30 * fs
    step_size = 15 * fs
    rows = []
    for start in range(0, len(filtered_signal) - window_size, step_size):
        end = start + window_size
        window_signal = filtered_signal[start:end]
        window_start_time = nasal.index[start]
        window_end_time = nasal.index[end]
        label = assign_label(window_start_time, window_end_time, events)
        rows.append({
            "mean": np.mean(window_signal),
            "std": np.std(window_signal),
            "max": np.max(window_signal),
            "min": np.min(window_signal),
            "label": label
        })
    dataset = pd.DataFrame(rows)
    os.makedirs(out_dir, exist_ok=True)
    dataset.to_csv(os.path.join(out_dir, "breathing_dataset.csv"), index=False)
    print("Total windows:", len(dataset))
    print("Dataset successfully created!")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-in_dir", required=True)
    parser.add_argument("-out_dir", required=True)
    args = parser.parse_args()
    create_dataset(args.in_dir, args.out_dir)


!python create_dataset.py -in_dir "internship/Data" -out_dir "internship/Dataset"
