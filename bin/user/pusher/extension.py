#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Raymon de Looff <raydelooff@gmail.com>
# This extension is open-source software licensed under the GPLv3 license.

__version__ = '1.1.0'

import Queue
import sys
import syslog
import time

import weewx
import weewx.restx
import pusher

from pusher import Pusher
from pusher.errors import PusherError
from weewx.restx import StdRESTful, RESTThread

class StdPusher(StdRESTful):
    """
    Sends WeeWX weather records to Pusher using the Pusher library.
    """

    def __init__(self, engine, config_dict):
        super(StdPusher, self).__init__(engine, config_dict)

        # This extension needs an App ID, key, secret, channel and event name
        _pusher_dict = weewx.restx.check_enable(
            config_dict, 'Pusher', 'app_id', 'key', 'secret', 'channel', 'event')
        if _pusher_dict is None:
            return

        # Get the database manager dictionary:
        _manager_dict = weewx.manager.get_manager_dict_from_config(config_dict,
                                                                   'wx_binding')

        self.loop_queue = Queue.Queue()

        # Try making the Pusher thread based on the given configuration
        try:
            self.loop_thread = PusherThread(self.loop_queue,
                                           _manager_dict,
                                           **_pusher_dict)
        except ValueError, e:
            syslog.syslog(syslog.LOG_ERR,
                          "pusher: Invalid values set in configuration.")
            syslog.syslog(syslog.LOG_ERR,
                              "*****   Error: %s" % e)
            return

        self.loop_thread.start()
        self.bind(weewx.NEW_LOOP_PACKET, self.new_loop_packet)

        syslog.syslog(syslog.LOG_INFO,
                  "pusher: Starting Pusher version %s." % __version__)
        syslog.syslog(syslog.LOG_INFO,
                  "pusher: LOOP packets will be pushed to channel '%s'." % _pusher_dict['channel'])

    def new_loop_packet(self, event):
        self.loop_queue.put(event.packet)


class PusherThread(RESTThread):
    """
    Thread for sending WeeWX weather data to Pusher.
    """

    DEFAULT_APP_ID = None
    DEFAULT_KEY = None
    DEFAULT_SECRET = None
    DEFAULT_CLUSTER = None
    DEFAULT_CHANNEL = None
    DEFAULT_EVENT = None
    DEFAULT_POST_INTERVAL = 5
    DEFAULT_TIMEOUT = 10
    DEFAULT_MAX_TRIES = 3
    DEFAULT_RETRY_WAIT = 5
    DEFAULT_OBSERVATION_TYPES = ['dateTime',
                                 'barometer',
                                 'inTemp',
                                 'outTemp',
                                 'inHumidity',
                                 'outHumidity',
                                 'windSpeed',
                                 'windDir',
                                 'rain',
                                 'rainRate'];

    def __init__(self, queue,
                 manager_dict,
                 app_id=DEFAULT_APP_ID,
                 key=DEFAULT_KEY,
                 secret=DEFAULT_SECRET,
                 cluster=DEFAULT_CLUSTER,
                 channel=DEFAULT_CHANNEL,
                 event=DEFAULT_EVENT,
                 observation_types=DEFAULT_OBSERVATION_TYPES,
                 post_interval=DEFAULT_POST_INTERVAL,
                 max_backlog=sys.maxint,
                 stale=60,
                 log_success=False,
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
                                           protocol_name='pusher',
                                           manager_dict=manager_dict,
                                           post_interval=post_interval,
                                           max_backlog=max_backlog,
                                           stale=stale,
                                           log_success=log_success,
                                           log_failure=log_failure,
                                           timeout=timeout,
                                           max_tries=max_tries,
                                           retry_wait=retry_wait)

        self.pusher = Pusher(app_id=app_id, key=key, secret=secret, cluster=cluster)
        self.channel = channel;
        self.event = event;
        self.observation_types = observation_types;

    def process_record(self, record, dbmanager):
        """Specialized version of process_record that pushes a message to Pusher."""

        # Convert the record to a dictionary
        _datadict = dict(record)

        # Check if there are any observations wanted that are not in the record
        for _observation in self.observation_types:
            if _observation not in _datadict:
                # Get the full record by querying the database ...
                record = self.get_record(record, dbmanager)
                syslog.syslog(syslog.LOG_DEBUG,
                              "pusher: Observation '%s' not found in record. Filling record from database."
                              % _observation)
                break

        # ... convert to Metric if necessary ...
        metric_record = weewx.units.to_METRICWX(record)

        # Instead of sending every observation type, send only those in
        # the list obs_types
        abridged = dict((x, metric_record.get(x)) for x in self.observation_types)

        packet = {}
        for k in abridged:
            packet[k] = abridged[k]

        # Try pushing the packet to Pusher up to max_tries times:
        for _count in range(self.max_tries):
            try:
                self.pusher.trigger(self.channel, self.event, packet)
                return
            except pusher.errors.PusherError, e:
                self.handle_exception(e, _count+1)
            time.sleep(self.retry_wait)
        else:
            raise weewx.restx.FailedPost("Tried %d times to post to channel '%s'." %
                             (self.max_tries, self.channel))

    def handle_exception(self, e, count):
        syslog.syslog(syslog.LOG_DEBUG,
                      "pusher: Failed upload attempt %d: %s" %
                      (count, e))
