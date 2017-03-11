#!/usr/bin/env bash

set -e
cd rpi_ws281x
scons
cd ..
cd openpixelcontrol
make bin/ws281x_server
cd ..
