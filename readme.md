# WeeWX Pusher extension
This [WeeWX](https://github.com/weewx/weewx) extension allows you to send your realtime weather data to Pusher. You can use Pusher to send realtime weather condition updates to your web application or app. Find more information about Pusher on [their website](https://pusher.com).

## Requirements
This extension requires the Pusher library for Python. The installation guide of the Pusher library can be found on [the official GitHub repository](https://github.com/pusher/pusher-http-python#installation).

## Installation
This extension can be installed very easily using the WeeWX installer.

1. Download the latest release from the releases section. Or use the following command:

    ```shell
    wget https://github.com/raymondelooff/weewx-pusher/archive/master.tar.gz
    ```
2. Install the extension with the WeeWX's extension installer:

    ```shell
    wee_extension --install=master.tar.gz
    ```

3. Edit your `weewx.conf` file and add the Pusher configuration to the StdRestful section. The installer automatically adds the Pusher configuration to your `weewx.conf`. If you prefer to have some comments in the configuration, copy and paste the following configuration to your `weewx.conf` file:
    ```ini
    [StdRestful]
        ...
        [[Pusher]]
            # This section is for configuring pushes to Pusher.
            enable = true

            # Set to the credentials of your Pusher application.
            # If you are not using the main cluster of Pusher
            # you need to specify the cluster.
            app_id = replace_me
            key = replace_me
            secret = replace_me
            # cluster = eu

            # Channel and event settings. The weather data is pushed
            # to the given channel, with the specified event name.
            channel = replace_me
            event = replace_me

            # The post interval of the weather data that is being pushed to
            # Pusher, in seconds. The default post interval is 5 seconds.
            post_interval = 5
	```
4. Restart WeeWX. WeeWX should then push your weather data to Pusher. You should be able to see the weather data in the [Pusher debug console](https://pusher.com/docs/debugging).

    ```shell
    sudo /etc/init.d/weewxd restart
    ```

## Issues
If you have any issues with the extension, please let me know via the GitHub [issues section](https://github.com/raymondelooff/weewx-pusher/issues). Provide as much information as possible, including the system log, so I can try to reproduce the problem. Turn WeeWX debugging on before posting your system log. Make sure you don't post any private information like API keys or secret keys.

## License & Copyright
Copyright (c) 2016 Raymon de Looff <raydelooff@gmail.com>.
This extension is open-source software licensed under the MIT license.
