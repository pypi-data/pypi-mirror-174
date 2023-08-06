# rrrelay

Relay HTTP POST transponder passings from Race Result Decoder
and Track Box units to telegraph as timer messages:

	INDEX;SOURCE;CHANNEL;REFID;TOD;DATE

   - INDEX : passing sequence number (set by the relay)
   - SOURCE : decoder ID
   - CHANNEL : loop id or timing channel
   - REFID : transponder unique ID
   - TOD : local time of day string eg 13h27:52.4321
   - DATE : date of passing  eg 2023-02-27

Also relays HTTP GET status messages from Track Box units:

	SOURCE;CHANNEL;TOD;DATE;STATUS;TEMP;NOISE;ACCEL;BATT

   - SOURCE : decoder ID
   - CHANNEL : loop id or timing channel
   - TOD : local time of day string eg 13h27:52.4321
   - DATE : date of passing  eg 2023-02-27
   - STATUS : RR specific decoder status
   - TEMP : temperature string
   - NOISE : noise level string
   - ACCEL : decoder orientation string
   - BATT : battery level string


## HTTP Endpoints

   - POST /rrs : Race Result Decoder (passive and active)
   - POST /tbp : Track Box Ping
   - GET /tbs : Track Box Status


## Configuration

Configuration is via metarace sysconf section 'rrrelay' with the
following keys:

key		|	(type) Description [default]
---		|	---
port		|	(int) HTTP listen port [53037]
passtopic	|	(string) MQTT relay topic for passings ['timing/data']
statustopic	|	(string) MQTT relay topic for status ['timing/status']
qos		|	(int) qos value for passing messages [2]
userid		|	(string) optional RR customer ID ['']
passiveloop	|	(dict) map passive device ids to loop ids [{}] (1)

Notes:

   1. Decoders reporting passive transponder reads can have their loopid
      overridden to force a specific channel id. For example, the following
      entry for passiveloop would assign all passive reads from decoder
      "D-23678" channel id "C5".

	"passiveloop":{"D-23678":"C5"}


## Decoder Setup

### Race Result Decoder

Open the decoder web interface and select the "Configuration" link.
Under "Upload target" select the option "Custom (HTTP)",
and enter the public ip, port and path to your rrrelay instance:

![RRS Config](rrs_config.png "RRS Config")

Then enable mobile upload on the decoder panel menu.

### Track Box

Set the track box 'Status URL' and 'Track Ping URL' to be the
url of your rrrelay instance, with a question mark on the end
of the path, for example:

	http://12.34.56.78:9012/tbp?

In tag tool, connect to the track box, select the "Advanced"
button, enter the updated URLs and then select "Apply Changes".
Note that the url may be reported as not reachable, even
when correct and working.

![TB Config](tb_config.png "TB Config")



## Requirements

   - tornado
   - metarace >=2.0

## Installation

Install with pip:

	$ pip3 install rrrelay

