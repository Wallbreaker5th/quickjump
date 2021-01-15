#!/bin/bash
current_path=$(cd "$(dirname $0)";pwd)
python "${current_path}/py/wolframalpha.py" $@
