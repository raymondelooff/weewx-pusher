# WeeWX Pusher extension
This WeeWX extension allows sending your weather data to Pusher in realtime. You can use Pusher to send realtime weather condition updates to your web application or app.

## Requirements
This extension requires the Pusher library for Python. The installation guide of the Pusher library can be found on [the official GitHub repository](https://github.com/pusher/pusher-http-python#installation).

## Installation
This extension can be installed very easily using the WeeWX installer.

1. Make sure you are using WeeWX version 3.3 or later.
2. Download the latest release from the releases section. Or use the following command:
	```shell
	wget https://github.com/raymondelooff/weewx-pusher/archive/master.tar.gz
	```
3. Install the extension with the WeeWX's extension installer
	```shell
	wee_extension install master.tar.gz
	```
4. Edit your weewx.conf file and add the Pusher configuration to the StdRestful section.
	```ini
	[StdRestful]
	    ...
	    [[Pusher]]
	        enable = true
	        # Set to the credentials of your Pusher application.
	        app_id = YOUR_APP_ID
	        key = YOUR_APP_KEY
	        secret = YOUR_APP_SECRET
	        # Channel and event settings. The weather data is pushed
	        # to the given channel, with the specified event name.
	        channel = CHANNEL_NAME
	        event = EVENT_NAME
	        # The post interval of the weather data that is being pushed to
	        # Pusher, in seconds. The default post interval is 5 seconds.
	        post_interval = 5
	```
5. Restart WeeWX. WeeWX should then push your weather data to Pusher. You should be able to see the weather data in the [Pusher debug console](https://pusher.com/docs/debugging).
	```shell
	/etc/init.d/weewxd restart
	```

# License & Copyright
Copyright (c) 2016 Raymon de Looff <raydelooff@gmail.com>
This extension is open-source licensed under the MIT license.
