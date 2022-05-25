#!/bin/zsh
rsync -rltgoDv --exclude=/.pyvenv/ --exclude='*/__pycache__/' --exclude=db.sqlite3 budenkiln@10.1.1.1:~/Code/kiln/ ./kiln
