#!/bin/sh
set -e

mkdir -p /home/logs /home/temp
chown -R appuser:appuser /home/logs /home/temp

exec gosu appuser "$@"
