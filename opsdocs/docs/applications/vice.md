# vice
![c64.svg](/applications/icons/c64.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.ubuntu.gtk.18.04](abcdesktopio/oc.template.ubuntu.gtk.18.04.md)
## Display name
"Commodore64"
## path
"/usr/bin/x64"
## File extensions
"crt;bin"
## Pre run command

```

RUN apt-get update && apt-get install  --no-install-recommends --yes vice libmp3lame0 git wget && apt-get clean,RUN git clone https://github.com/stuartcarnie/vice-emu/ && mv vice-emu/vice/data/DRIVES/* /usr/lib/vice/C64 && cd /vice-emu/vice/data/C64 && mv chargen kernal basic /usr/lib/vice/C64,RUN mkdir /usr/lib/vice/C64/cartridge,RUN wget http://www.zimmers.net/anonftp/pub/cbm/firmware/misc/c64carts/Super_Games_1-8000.bin -O /usr/lib/vice/C64/cartridge/Super_Games_1-8000.bin,RUN wget http://www.zimmers.net/anonftp/pub/cbm/firmware/misc/c64carts/Super_Games_2-8000.bin -O /usr/lib/vice/C64/cartridge/Super_Games_2-8000.bin,RUN wget http://www.zimmers.net/anonftp/pub/cbm/firmware/misc/c64carts/Super_Games_3-8000.bin -O /usr/lib/vice/C64/cartridge/Super_Games_3-8000.bin,RUN wget http://www.zimmers.net/anonftp/pub/cbm/firmware/misc/c64carts/Super_Games_4-8000.bin -O /usr/lib/vice/C64/cartridge/Super_Games_4-8000.bin,RUN wget http://www.zimmers.net/anonftp/pub/cbm/firmware/misc/c64carts/C64638_Jack_Attack-8000.bin -O /usr/lib/vice/C64/cartridge/C64638_Jack_Attack-8000.bin,RUN wget http://www.zimmers.net/anonftp/pub/cbm/firmware/misc/c64carts/315102-01.bin -O /usr/lib/vice/C64/cartridge/315102-01.bin,RUN wget http://www.zimmers.net/anonftp/pub/cbm/firmware/misc/c64carts/315103-01.bin -O /usr/lib/vice/C64/cartridge/315103-01.bin
```
