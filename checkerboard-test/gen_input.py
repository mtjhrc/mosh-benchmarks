with open("build/input.termrec", "w") as f:
    f.write("termrec:v1:inp:\\\n")
    n = 131
    signals = ["aaa", "bbb"]
    for i in range(n):
        signal = signals[i%len(signals)]
        f.write(f"w:{len(signal)}:{signal}\\\n")
        marker = f"frame_{i:03}"
        f.write(f"m:{len(marker)}:{marker}\\\n")
        f.write(f"i:0:1:n\\\n")
    
    signal = signals[n % len(signals)]
    f.write(f"w:{len(signal)}:{signal}\\\n")
    f.write(f"i:0:1:q\\\n")
