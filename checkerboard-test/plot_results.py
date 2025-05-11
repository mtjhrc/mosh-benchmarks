#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import subprocess
import sys

def plot_times(msg, datasets, labels, output):
    colors = plt.cm.tab10.colors[:len(datasets)]
    
    assert labels is not None

    offsets = [(i - len(datasets) / 2) * 0.2 for i in range(len(datasets))]

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
    y_ticks = np.linspace(y_min, y_max, len(datasets)).astype(int)

    # Adding labels and title
    plt.xlabel('', fontsize=13)
    plt.ylabel('Time to redraw screen', fontsize=13)
    #plt.title('Comparison of Time Analysis for Each Character', fontsize=14)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xticks(range(len(msg)), list(msg), fontsize=12, weight="bold")
    plt.yticks(y_ticks, [f"{tick/1000:.02f} ms" for tick in y_ticks])
    plt.legend(title="Program", loc="upper right")
    plt.xlim(-0.7, len(msg) - 0.7)
    
    plt.tight_layout()
    
    if output == "GUI":
        plt.show()
    else:
        plt.savefig(output)

def compute_measurments(recording_dir, test_range):
    results = [[]]
    for i in test_range:
        cmd = ["../prefix/bin/termrec", "measure", "-d", recording_dir, 
            "--after-event", f"m:frame_{i:03}", 
            "--before-event",f"m:frame_{i+1:03}",
            "--from-event", f"i:n", 
            "--to-frame", "reference_frame_aaa" if i % 2 == 0 else "reference_frame_bbb", 
        ]
       
        try:
            result = subprocess.run(cmd, capture_output=True,check=True)
            print(" ".join(cmd), "  -> ", int(result.stdout))
        except Exception as e:
            print("FAILED: "," ".join(cmd))
            print(e)
            exit(1)
        results[0].append(int(result.stdout))
    return results

TEST_RANGE = range(30, 130)
args = sys.argv[1:]
assert len(args) >= 3, "Usage: ./plot_results.py RECORDING LABEL"
assert len(args) % 2 == 1, "Mismatched number of RECORDING/LABEL arguments"

output = sys.argv[1]

recordings = []
labels = []
for (recording, label) in zip(sys.argv[2::2], sys.argv[3::2]):
    recordings.append(recording)
    labels.append(label)

measurements = [compute_measurments(recording, TEST_RANGE) for recording in recordings]
plot_times([""], datasets=measurements, labels=labels, output=output)
