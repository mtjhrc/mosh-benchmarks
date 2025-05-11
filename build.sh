#!/usr/bin/sh

set -x

mkdir -p prefix

cd openssh-portable
./autogen.sh 
./configure --prefix=$(realpath ../prefix) --sysconfdir=$(realpath $PWD/../prefix/ssh_dir) --without-pam --without-selinux --without-privsep
make
make install
cd ..

ssh-keygen -f ./prefix/ssh_host_key -N ''
ssh-keygen -f ./prefix/ssh_client_key -N ''
cat <<EOF > ./prefix/ssh_dir/sshd_config 
AuthorizedKeysFile $(realpath ./prefix/ssh_client_key.pub)
HostKey $(realpath ./prefix/ssh_host_key)
PasswordAuthentication no
PermitRootLogin no
PermitEmptyPasswords no
EOF

cargo install --path ./termrec --root ./prefix