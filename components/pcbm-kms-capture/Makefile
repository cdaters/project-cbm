CC ?= cc
CFLAGS ?= -O2 -g
CPPFLAGS += $(shell pkg-config --cflags libdrm libpng)
LDLIBS += $(shell pkg-config --libs libdrm libpng) -lcap
all: pcbm-kms-capture
pcbm-kms-capture: capture.c policy.h
	$(CC) $(CPPFLAGS) $(CFLAGS) -std=c11 -Wall -Wextra -Werror -fstack-protector-strong -D_FORTIFY_SOURCE=2 $(LDFLAGS) -Wl,-z,relro,-z,now -o $@ capture.c $(LDLIBS)
clean:
	rm -f pcbm-kms-capture
.PHONY: all clean
