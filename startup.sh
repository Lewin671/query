#!/bin/bash

base_dir=$(cd "$(dirname "$0")"; pwd)

echo "base_dir=\"$base_dir\"">>~/.bashrc

echo "alias query=\"python $base_dir/main.py\"">> ~/.bashrc

python "$base_dir/init.py"

echo "finished, please restart your terminal to enjoy it."
