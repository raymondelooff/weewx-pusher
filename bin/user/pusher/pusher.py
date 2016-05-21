#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Raymon de Looff <raydelooff@gmail.com>
# This extension is open-source licensed under the MIT license.

from pusher import Pusher
import Queue
import socket
import sys
import syslog

import weewx
import weewx.restx
import weeutil.weeutil

from weewx.restx import StdRESTful, RESTThread

class StdPusher(StdRESTful):
    """
    Sends WeeWX weather records to Pusher using the Pusher library.
    """

    def __init__(self, engine, config_dict):
        super(WeeWXPusher, self).__init__(engine, config_dict)

        _pusher_dict = weewx.restx.check_enable(config_dict, 'Pusher')
        if _pusher_dict is None
            return

        # This extension needs an App ID, key, secret, channel and event name
        _pusher_dict = get(
            config_dict, 'Pusher', 'app_id', 'key', 'secret', 'channel', 'event')
        if _pusher_dict is None:
            syslog.syslog(syslog.LOG_DEBUG,
                          "Pusher: Data will not be posted to Pusher. Please check if you provided the App ID, key, secret, channel and event name.")
            return

        # Get the database manager dictionary:
        _manager_dict = weewx.manager.get_manager_dict_from_config(config_dict,
                                                                   'wx_binding')
        self.loop_queue = Queue.Queue()
        self.loop_thread = PusherThread(self.loop_queue,
                                       _manager_dict,
                                       **_node_dict)
        self.loop_thread.start()
        self.bind(weewx.NEW_LOOP_PACKET, self.new_loop_packet)

        syslog.syslog(syslog.LOG_INFO, "Pusher: LOOP packets will be pushed to channel %s.", _pusher_dict['channel'])

    def new_loop_packet(self, event):
        self.loop_queue.put(event.packet)


class PusherThread(RESTThread):
    """
    Thread for sending WeeWX weather data to Pusher.
    """

    DEFAULT_APP_ID = None
    DEFAULT_KEY = None
    DEFAULT_SECRET = None
    DEFAULT_CHANNEL = None
    DEFAULT_EVENT = None
    DEFAULT_POST_INTERVAL = 5
    DEFAULT_TIMEOUT = 60
    DEFAULT_MAX_TRIES = 1
    DEFAULT_RETRY_WAIT = 5

    def __init__(self, queue,
                 manager_dict,
                 app_id=DEFAULT_HOST,
                 key=DEFAULT_KEY,
                 secret=DEFAULT_SECRET,
                 channel=DEFAULT_CHANNEL,
                 event=DEFAULT_EVENT,
                 post_interval=DEFAULT_POST_INTERVAL,
                 max_backlog=sys.maxint,
                 stale=60,
                 log_success=True,
                 log_failure=True,
                 timeout=DEFAULT_TIMEOUT,
                 max_tries=DEFAULT_MAX_TRIES,
                 retry_wait=DEFAULT_RETRY_WAIT):

        """
        Initializes an instance of PusherThread.

        :param app_id: The 'App ID' of your Pusher application.
        :param key: The 'key' of your Pusher application.
        :param secret: The 'secret' of your Pusher application.
        :param channel: The name of the channel to push the weather data to.
        :param event: The name of the event that is pushed to the channel.
        :param post_interval: The interval in seconds between posts.
        :param max_backlog: Max length of Queue before trimming. dft=sys.maxint
        :param stale: How old a record can be and still considered useful.
        :param log_success: Log a successful post in the system log.
        :param log_failure: Log an unsuccessful post in the system log.
        :param max_tries: How many times to try the post before giving up.
        :param timeout: How long to wait for the server to respond before fail.
        """
        super(PusherThread, self).__init__(queue,
                                             protocol_name='Pusher',
                                             manager_dict=manager_dict,
                                             post_interval=post_interval,
                                             max_backlog=max_backlog,
                                             stale=stale,
                                             log_success=log_success,
                                             log_failure=log_failure,
                                             timeout=timeout,
                                             max_tries=max_tries,
                                             retry_wait=retry_wait)

        self.pusher = Pusher(app_id=app_id, key=key, secret=secret)

    def process_record(self, record, dbmanager):
        _ = dbmanager


