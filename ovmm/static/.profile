#!/bin/sh

# ~/.profile: executed by the command interpreter for login shells.
# This file is not read by bash(1), if ~/.bash_profile or ~/.bash_login
# exists.
# see /usr/share/doc/bash/examples/startup-files for examples.
# the files are located in the bash-doc package.

# the default umask is set in /etc/profile; for setting the umask
# for ssh logins, install and configure the libpam-umask package.
# umask 022

# if running bash
if [ -n "$BASH_VERSION" ]; then
    # include .bashrc if it exists
    if [ -f "$HOME/.bashrc" ]; then
    . "$HOME/.bashrc"
    fi
fi

# set PATH so it includes user's private bin directories
PATH="$HOME/bin:$HOME/.local/bin:$PATH"

# set aliases
alias run_prodserver="screen -S otree -m otree runprodserver --port {daphne_port}"
alias run_mail_prodserver="screen -S otree -m otree runprodserver --port {daphne_port} && mail -s 'oTree stopped' {email} <<< 'Warning your otree on port {daphne_port} has stopped.'"

# source otree_environ_config
source $HOME/otree_environ_config
