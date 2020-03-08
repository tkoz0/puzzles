#!/bin/bash
for f in $(cat download.txt); do wget -c $f; done;
