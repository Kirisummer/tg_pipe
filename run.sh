#!/bin/sh

python -u filter.py me '.*' | python forwarder.py destination
