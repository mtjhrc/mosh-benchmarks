
# Instruction how to run
1. Build the dependencies:
`./build.sh`
2. copy/link the tested mosh-server and mosh-client binaries into the bin directory
3. Make sure you have the required kernel:
`sudo modprobe sch_netem`
4. Enable the usage of the `TCP_THIN_LINEAR_TIMEOUTS` socket option:
`$ net.ipv4.tcp_thin_linear_timeouts`
4. Run echo-test benchmark
`$ cd echo-test`
`$ make`
`$ sudo ./run.sh`
5. Run checkerboard-test benchmark
`$ cd checkerboard-test`
`$ make`
`$ sudo ./run.sh`

