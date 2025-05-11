#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import subprocess
import sys

def plot_letter_times(msg, datasets, labels, output):
    colors = plt.cm.tab10.colors[:len(datasets)]
    assert labels is not None

    offsets = [(i - len(datasets) / 2) * 0.2 for i in range(len(datasets))]

    # Create the plot
    plt.figure(figsize=(12, 7))

    for dataset, color, label, offset in zip(datasets, colors, labels, offsets):
        for idx, times in enumerate(dataset):
            # Offset the x-values slightly for each dataset
            x_values = [idx + offset for _ in times]
            plt.scatter(x_values, times, color=color, label=label if idx == 0 else "", alpha=0.6)


    # Flatten all datasets to compute y-tick range
    all_values = [value for dataset in datasets for times in dataset for value in times]
    y_min, y_max = min(all_values), max(all_values)
    
    # Dynamically compute 10 evenly spaced y-ticks
    y_ticks = np.linspace(y_min, y_max, 10).astype(int)

    plt.xlabel('Keystrokes', fontsize=13)
    plt.ylabel('Time to echo the character', fontsize=13)
    #plt.title('Comparison of Time Analysis for Each Character', fontsize=14)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xticks(range(len(msg)), list(msg), fontsize=12, weight="bold")
    plt.yticks(y_ticks, [f"{tick/1000:.02f} ms" for tick in y_ticks])
    plt.legend(title="Program", loc="upper right")
    plt.xlim(-0.7, len(MSG) - 0.7)
    
    plt.tight_layout()
    
    if output == "GUI":
        plt.show()
    else:
        plt.savefig(output)

def compute_measurments(msg, recording_dir, test_range):
    results =  [[] for _ in msg]
    for i in test_range:
        for c_index, c in enumerate(msg):
            cmd = ["../prefix/bin/termrec", "measure", "-d", recording_dir, 
                "--after-event", f"m:msg_{i:03}", 
                "--before-event",f"m:msg_{i+1:03}",
                "--from-event", f"i:{c}", 
                "--to-frame-with-text", MSG[:c_index+1], 
                "--ignore-sequence", "\x1B[4m", # underline
                "--ignore-sequence", "\x1B[0m"  # reset
            ]
            try:
                result = subprocess.run(cmd, capture_output=True,check=True)
                print(f"{i:03} -> {i+1:03} = {result.stdout}")
            except Exception as e:
                print("FAILED: "," ".join(cmd))
                print(e)
                exit(1)
            results[c_index].append(int(result.stdout))
    return results

MSG = "Hi_World!"
TEST_RANGE = range(30, 129)
args = sys.argv[1:]
assert len(args) >= 3, "Usage: ./plot_results.py RECORDING LABEL"
assert len(args) % 2 == 1, "Mismatched number of RECORDING/LABEL arguments"

output = sys.argv[1]

recordings = []
labels = []
for (recording, label) in zip(sys.argv[2::2], sys.argv[3::2]):
    recordings.append(recording)
    labels.append(label)

measurements = [compute_measurments(MSG, recording, TEST_RANGE) for recording in recordings]
plot_letter_times(MSG, datasets=measurements, labels=labels, output=output)
