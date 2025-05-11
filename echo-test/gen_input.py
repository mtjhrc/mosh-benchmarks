def fmt_marker(n):
   return f"msg_{n:03}"  

def main():
    n = 131
    frame_signals = ["aaaa", "bbbb"]
    
    with open("build/input.termrec", "w") as f:
        f.write("termrec:v1:inp:\\\n")
        f.write(f"w:{len(frame_signals[0])}:{frame_signals[0]}\\\n")

        for i in range(n):
            marker = fmt_marker(i)
            signal = frame_signals[(i+1) % 2]
            
            last_time = 0
            def next_t():
                nonlocal last_time
                last_time += 70000
                return last_time
            
            f.write(f"m:{len(marker)}:{marker}\\\n"
                    f"i:{next_t()}:1:H\\\n"
                    f"i:{next_t()}:1:i\\\n"
                    f"i:{next_t()}:1:_\\\n"
                    f"i:{next_t()}:1:W\\\n"
                    f"i:{next_t()}:1:o\\\n"
                    f"i:{next_t()}:1:r\\\n"
                    f"i:{next_t()}:1:l\\\n"
                    f"i:{next_t()}:1:d\\\n"
                    f"i:{next_t()}:1:!\\\n"
                    f"w:1:!\\\n"
                    f"i:0:1:\n"
                    f"w:{len(signal)}:{signal}")

        marker = fmt_marker(n+1);
        f.write(f"m:{len(marker)}:{marker}\\\n");
        f.write("i:0:1:q\\\n")

main()
