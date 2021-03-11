#!/bin/bash
set -e
set -x
# adduser kacy          # customize this to your liking
# usermod -aG sudo kacy # input your username instead of mine
sudo apt update
sudo apt dist-upgrade -y
sudo apt install git -y
# git config --global user.name "kacy"                  # input your username instead of mine
# git config --global user.email "my_email@gmail.com"   # input your email instead of mine
git config --global core.autocrlf false
cd ~ || exit 1
mkdir .ssh
chmod 700 .ssh
# cd .ssh || exit 1     # only do this and the following 3 steps if you have ssh set up on your windows machine
# cp /mnt/c/Users/Kacy/.ssh/id_rsa* .   # otherwise, look up how to set up ssh on github
# chmod 600 id_rsa
# chmod 644 id_rsa.pub
sudo apt install python3.9 python3-pip ipython3 -y
sudo apt install shellcheck -y
sudo apt install vim-gtk -y
sudo apt install build-essential -y
sudo apt install perl -y
# sudo apt install zsh -y   # this is only if you want to install ZSH, which is a nicer terminal
# sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)" -y # install OH MY ZSH to get the best zsh effect
sudo apt update
sudo apt dist-upgrade -y
printf "Don't forget to copy your ssh key to your github's authorized keys if you want to use github: "
# cat ~/.ssh/id_rsa.pub         # copies your public rsa key to the terminal so you can copy and paste it into github