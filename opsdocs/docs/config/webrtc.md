

# Sound server configuration

By default abcdesktop use the ```module-http-protocol-tcp``` from pulseaudio sound server to send wav data to the web browser


## webrtc gateway disable (default)

In terminal webshell run the command : 

```bash
pactl -s /tmp/.pulse.sock list short modules
```

```
balloon@bac345323f37:/var/log/desktop$ pactl -s /tmp/.pulse.sock list short modules
0 module-augment-properties
1 module-null-sink sink_name=u8_1_11025 format=u8 channels=1 rate=11025 sink_properties="device.description='default format=u8 c=1 rate=11025'"
2 module-null-sink sink_name=s16_1_22050 format=s16be channels=1 rate=22050 sink_properties="device.description='default format=s16be c=1 rate=22050'"
3 module-null-sink sink_name=s16_1_44100 format=s16be channels=1 rate=44100 sink_properties="device.description='default format=s16be c=1 rate=44100'"
4 module-null-sink sink_name=ulaw8_1_8000 format=ulaw channels=1 rate=8000 sink_properties="device.description='default format=ulaw c=1 rate=8000'"
5 module-null-sink sink_name=rtp format=alaw channels=1 rate=8000 sink_properties="device.description='RTP Multicast Sink'"
6 module-native-protocol-unix auth-group=balloon socket=/tmp/.pulse.sock
7 module-http-protocol-tcp listen=172.21.0.5
8 module-always-sink
```

## webrtc gateway enable

To get a better sound quality, you can use a webrtc gateway and send a rtp stream to the webrtc gateway. abcdesktop update the pulseaudio configuration, and add ```module-rtp-send```. The ```module-rtp-send``` pusleaudio send to the destination_ip (in this example 1.2.3.4) 


```bash
pactl -s /tmp/.pulse.sock list short modules
```

```
balloon@414e3db9-60d8-4f92-a356-a3a74833990c:~$ pactl -s /tmp/.pulse.sock list short modules
0       module-augment-properties
1       module-null-sink        sink_name=rtp  format=alaw channels=1 rate=8000 sink_properties="device.description='RTP Multicast Sink'"
2       module-native-protocol-unix     auth-group=balloon socket=/tmp/.pulse.sock
3       module-always-sink
4       module-rtp-send source=rtp.monitor destination_ip=1.2.3.4 port=5119 channels=1 format=alaw
```

The ```sink_name``` is rtp, and the ```source``` for the ```module-rtp-send``` is rtp.monitor.


The default source is ```rtp.monitor```

```
Source #
        State: RUNNING
        Name: rtp.monitor
        Description: Monitor of RTP Multicast Sink
        Driver: module-null-sink.c
        Sample Specification: aLaw 1ch 8000Hz
        Channel Map: mono
        Owner Module: 5
        Mute: no
        Volume: mono: 65536 / 100% / 0.00 dB
                balance 0.00
        Base Volume: 65536 / 100% / 0.00 dB
        Monitor of Sink: rtp
        Latency: 0 usec, configured 160000 usec
        Flags: DECIBEL_VOLUME LATENCY 
        Properties:
                device.description = "Monitor of RTP Multicast Sink"
                device.class = "monitor"
                device.icon_name = "audio-input-microphone"
        Formats:
                pcm
```

The default output is 

```

Source Output #0
        Driver: module-rtp-send.c
        Owner Module: 9
        Client: n/a
        Source: 4
        Sample Specification: aLaw 1ch 8000Hz
        Channel Map: mono
        Format: pcm, format.sample_format = "\"aLaw\""  format.rate = "8000"  format.channels = "1"  format.channel_map = "\"mono\""
        Corked: no
        Mute: no
        Volume: mono: 65536 / 100% / 0.00 dB
                balance 0.00
        Buffer Latency: 0 usec
        Source Latency: 0 usec
        Resample method: n/a
        Properties:
                media.name = "RTP Monitor Stream"
                rtp.source = "0.0.0.0"
                rtp.destination = "1.2.3.4"
                rtp.mtu = "1280"
                rtp.port = "5119"
                rtp.ttl = "1"
```

By default, the format is ```pcm```

``` 
Format: pcm, format.sample_format = "\"aLaw\""  format.rate = "8000"  format.channels = "1"  format.channel_map = "\"mono\""
```

To change the default format update the values in od.config file.

```
 'audiopt': 8,
 'audiortpmap': 'PCMA/8000',
``` 

To get the 'audiopt' and 'audiortpmap' values, read the web pages

* [meetecho streaming plugin documentation](https://janus.conf.meetecho.com/docs/streaming.html)
* [RTP payload formats](https://en.wikipedia.org/wiki/RTP_payload_formats)



## Requirements

* a janus server  
* add webrtc configuration in od.config file


## Install a janus server

### Install janus 

Install a janus service from [meetecho.com](https://janus.conf.meetecho.com/) on a server 

```
apt-get install janus
```

### Add X509 certificats
Add X509 certificats in your janus.jcfg configuration. Certificate and key to use for DTLS (and passphrase if needed). If missing, Janus will autogenerate a self-signed certificate to use. Notice that self-signed certificates are fine for the purpose of WebRTC DTLS connectivity, for the time being, at least until Identity Providers are standardized and implemented in browsers.

```
certificates: {
	cert_pem = "/etc/ssl/certs/ssl-cert-snakeoil.pem"
	cert_key = "/etc/ssl/private/ssl-cert-snakeoil.key"
   	cert_pwd = "secretpassphrase"
}
```


## add the webrtc entry in od.config

Update the od.config file, for example :

```
# WebRTC Janus config
webrtc.enable : True
webrtc.server : {   'janus.domain.local' : { 'schema' : 'http',
                                          'host': 'janus.domain.local',
                                          'hostip': '1.2.3.4',
                                          'port': 8088,
                                          'audiopt': 8,
                                          'audiortpmap': 'PCMA/8000',
                                          'apisecret': 'janusrocks',
                                          'adminkey': 'supersecret',
                                          'startport': 5100 } }
```



### webrtc.enable 
```webrtc.enable``` is a boolean. The default value is ```False```. Set this value to ```True``` to enable webrtc services for ```pulseaudio```.


### webrtc.server
```webrtc.server``` is a dict. The default value is ```None```. 
Set all dictionnary values to enable webrtc access for ```pulseaudio``` and for the web browser client.

The ```hostip``` value, is used by pluse audio to configure the rtp stream. This value must be an ip address (do not set the fqdn). This can be an internal ip address.

```
'hostip': '1.2.3.4'
```

The ```host``` value, is used by the browser to reach the rtp stream. This value must(should) be a fqdn. This fqdn is used by the web browser.

```
webrtc.server : {   'janus.domain.local' : { 'schema' : 'http',
                                          'host': 'janus.domain.local',
                                          'hostip': '123.123.123.123',
                                          'port': 8088,
                                          'audiopt': 8,
                                          'audiortpmap': 'PCMA/8000',
                                          'apisecret': 'janusrocks',
                                          'adminkey': 'supersecret',
                                          'startport': 5100 } }
```



