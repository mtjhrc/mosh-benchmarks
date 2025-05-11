#!/usr/bin/sh

ip netns del ns_client
ip netns del ns_server
ip netns exec ns_client tc qdisc del dev veth_client root 2>/dev/null || true