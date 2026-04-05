FROM ubuntu:22.04

USER root
RUN apt-get -y update && apt-get -y install cowsay

# install tools
RUN apt-get install -y sudo file tmux screen byobu rsync python-is-python3

# change the user to make things easier
# RUN usermod -md /home/hacker -l hacker ubuntu && groupmod -n hacker ubuntu

