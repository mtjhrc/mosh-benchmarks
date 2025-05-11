#!/bin/sh 

ip netns add ns_client
ip netns add ns_server
ip link add veth_client type veth peer name veth_server
ip link set veth_client netns ns_client
ip link set veth_server netns ns_server

ip netns exec ns_client ip link set dev veth_client up
ip netns exec ns_server ip link set dev veth_server up

ip netns exec ns_server ifconfig veth_server 10.0.0.1/24 up
ip netns exec ns_client ifconfig veth_client 10.0.0.2/24 up

if [ $# -gt 0 ]; then
    ip netns exec ns_client tc qdisc add dev veth_client root netem $@ seed 42
fi