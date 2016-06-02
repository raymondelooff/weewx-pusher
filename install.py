#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Setup for the WeeWX Pusher extension.
# Source: https://github.com/raymondelooff/weewx-pusher
# Copyright (c) 2016 Raymon de Looff <raydelooff@gmail.com>
# This extension is open-source software licensed under the GPLv3 license.

__version__ = '1.1.1'

from setup import ExtensionInstaller

def loader():
    """Installs the WeeWX Pusher extension."""
    return PusherInstaller()


class PusherInstaller(ExtensionInstaller):
    """Installs the WeeWX Pusher extension."""

    def __init__(self):
        super(PusherInstaller, self).__init__(
            version=__version__,
            name='pusher',
            description='Send realtime weather data to Pusher.',
            author='Raymon de Looff',
            author_email='raydelooff@gmail.com',
            restful_services='user.pusher.extension.StdPusher',
            config={
                'StdRESTful': {
                    'Pusher': {
                        'enable': 'True',
                        'app_id': 'replace_me',
                        'key': 'replace_me',
                        'secret': 'replace_me',
                        'cluster': 'replace_me',
                        'channel': 'replace_me',
                        'event': 'replace_me',
                        'post_interval': 5
                    }
                }
            },
            files=[('bin/user/pusher', ['bin/user/pusher/__init__.py',
                                        'bin/user/pusher/extension.py'])]
        )
