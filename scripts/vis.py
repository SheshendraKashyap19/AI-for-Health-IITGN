flow_path = "internship/Data/AP01/Flow - 30-05-2024.txt"
import pandas as pd

def load_signal(file_path):
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
        if line.strip() == "":
            continue

        parts = line.strip().split(";")
        if len(parts) != 2:
            continue

        timestamp_str = parts[0].strip()
        value_str = parts[1].strip()

        timestamps.append(timestamp_str)
        values.append(float(value_str))

    df = pd.DataFrame({
        "timestamp": timestamps,
        "value": values
    })


    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        format="%d.%m.%Y %H:%M:%S,%f"
    )

    df.set_index("timestamp", inplace=True)

    return df
flow_path = "internship/Data/AP01/Flow - 30-05-2024.txt"
nasal = load_signal(flow_path)

print(nasal.head())

import matplotlib.pyplot as plt

plt.figure(figsize=(12,4))
plt.plot(nasal.index[:3000], nasal.value[:3000])
plt.title("Nasal Airflow (First few seconds)")
plt.show()
def load_events(file_path):
    events = []

    with open(file_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()

      
        if not line or "Signal" in line or "Start Time" in line or "Unit" in line or "Signal Type" in line:
            continue

      
        parts = line.split(";")
        if len(parts) < 3:
            continue

      
        time_range = parts[0].strip()
        event_type = parts[2].strip()

        start_str, end_str = time_range.split("-")

        start_time = pd.to_datetime(start_str, format="%d.%m.%Y %H:%M:%S,%f")
        end_time = pd.to_datetime(end_str, format="%H:%M:%S,%f")

        # IMPORTANT: end_time is missing date, so we add same date as start
        end_time = end_time.replace(
            year=start_time.year,
            month=start_time.month,
            day=start_time.day
        )

        events.append({
            "start": start_time,
            "end": end_time,
            "event": event_type
        })

    events_df = pd.DataFrame(events)
    return events_df
nasal = load_signal(f"{base_path}/Flow - 30-05-2024.txt")
thoracic = load_signal(f"{base_path}/Thorac - 30-05-2024.txt")
spo2 = load_signal(f"{base_path}/SPO2 - 30-05-2024.txt")

events = load_events(f"{base_path}/Flow Events - 30-05-2024.txt")

fig, axes = plt.subplots(3, 1, figsize=(20, 12), sharex=True)

axes[0].plot(nasal.index, nasal.value, linewidth=0.5)
axes[0].set_title("Nasal Airflow ")

axes[1].plot(thoracic.index, thoracic.value, linewidth=0.5)
axes[1].set_title("Thoracic Movement")

axes[2].plot(spo2.index, spo2.value, linewidth=0.5)
axes[2].set_title("SpO2")


for _, row in events.iterrows():
    for ax in axes:
        ax.axvspan(row["start"], row["end"], color='red', alpha=0.3)

plt.tight_layout()

# Save PDF
os.makedirs("Visualizations", exist_ok=True)
plt.savefig("Visualizations/AP01_visualization.pdf")

plt.show()

