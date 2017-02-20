WEECHATRC ?= ~/.weechat
dest_file := $(WEECHATRC)/python/autoload/teleirc.py

$(dest_file): teleirc.py
	ln -sv `readlink -f $<` $@

install: $(dest_file)
