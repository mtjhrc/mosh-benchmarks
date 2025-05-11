#!/usr/bin/sh

drop_priv() {
    sudo -E -u "$SUDO_USER" -- "$@"
}

mosh_bench() {
    mosh_bench_PROT="$1"
    mosh_bench_DIR="$2"
    shift 2
    drop_priv mkdir -p "$mosh_bench_DIR"
    ../create_ns.sh "$@"
    ./mosh_runner.py "$mosh_bench_PROT" "$mosh_bench_DIR"
    ../delete_ns.sh
}

ssh_bench() {
    ssh_bench_DIR="$1"
    shift
    drop_priv mkdir -p "$ssh_bench_DIR"
    ../create_ns.sh "$@"
    ./ssh_runner.sh "$ssh_bench_DIR"
    ../delete_ns.sh
}

plot_dir() {
    plot_dir_DIR="$1"
    drop_priv ./plot_results.py results/$plot_dir_DIR.png results/$plot_dir_DIR/mosh-udp "Mosh (UDP)" results/$plot_dir_DIR/mosh-tcp "Mosh (TCP)" results/$plot_dir_DIR/mosh-tcp-thin "Mosh (TCP; enabled thin stream)" results/$plot_dir_DIR/ssh "OpenSSH"
}

bench_group() {
    bench_group_DIR="$1"
    shift
    ssh_bench results/$bench_group_DIR/ssh "$@"
    MOSH_TCP_THIN=0 mosh_bench UDP results/$bench_group_DIR/mosh-udp "$@"
    MOSH_TCP_THIN=0 mosh_bench TCP results/$bench_group_DIR/mosh-tcp "$@"
    MOSH_TCP_THIN=1 mosh_bench TCP results/$bench_group_DIR/mosh-tcp-thin "$@"
    plot_dir $bench_group_DIR
}

bench_group good-net  delay 15ms 5ms distribution normal
bench_group worse-net delay 100ms 50ms distribution normal
bench_group loss-net  delay 100ms 50ms loss 30% distribution normal
