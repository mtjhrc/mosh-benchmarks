#!/usr/bin/sh
set -x

export LANG="en_US.UTF-8"
export LC_ALL="en_US.UTF-8"
export TERM="xterm-256color"

ip netns exec ns_server $(realpath ../prefix/sbin/sshd) -f ../prefix/ssh_dir/sshd_config

ip netns exec ns_client sudo -E -u $SUDO_USER \
  ../prefix/bin/termrec record --child-stderr /dev/null -i build/input.termrec -d $1 -- \
  ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
  -i ../prefix/ssh_client_key \
  $SUDO_USER@10.0.0.1 -t $(realpath build/checkerboard)

pkill -n sshd