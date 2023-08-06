import http.server
import logging
import re
import requests as req
import socketserver
import threading
import time

'''
Primary-backup model for HA Telegram bots:

Primary is the instance that has become primary with the lowest timestamp

First, look for primary
In case no primary is found:
1. Become primary with the current timestamp
2. Start broadcasting that timestamp for other instances
3. Keep looking for primary with a lower timestamp
4. Start the bot

In case primary is found:
Keep looking for it periodically

If primary finds an instance that has become primary with lower timestamp:
1. Stop everything
2. Restart looking for primary
'''

class PrimaryLookUpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, timestamp):
        self.timestamp=timestamp

    def __call__(self, request, client_address, server):
        h = PrimaryLookUpRequestHandler(self.timestamp)
        socketserver.StreamRequestHandler.__init__(h, request, client_address, server)

    def do_GET(self):
        timestamp_pattern = re.compile("[0-9].*\\.[0-9].*")
        if re.fullmatch(timestamp_pattern, self.path.split('/')[-1]):
            proposed_timestamp = self.path.split('/')[-1]
            if float(proposed_timestamp) <= float(self.timestamp):
                class KillThread(threading.Thread):
                    def __init__(self, server):
                        threading.Thread.__init__(self)
                        self.server = server
                    def run(self):
                        self.server.shutdown()
                self.send_response(200)
                KillThread(self.server).start()
            else:
                self.send_error(500)
        else:
            self.send_error(500)

class BotMainThread(threading.Thread):

    def __init__(self, updater):
        self.updater=updater
        threading.Thread.__init__(self)

    def run(self):
        # start your shiny new bot
        self.updater.start_polling()
        # run the bot until Ctrl-C
        self.updater.idle()

class PrimaryBroadcasterThread(threading.Thread):

    def __init__(self, timestamp):
        self.server=socketserver.TCPServer(("", 7175), PrimaryLookUpRequestHandler(timestamp))
        threading.Thread.__init__(self)

    def run(self):
        logging.info("Primary node serving primary lookup requests at port 7175.")
        self.server.serve_forever()
        logging.info("Node ceased being primary.")

class PrimaryLookupThread(threading.Thread):

    def __init__(self, instances):
        self.instances=instances
        self.shutdown_signal=threading.Event()
        threading.Thread.__init__(self)

    def run(self):
        self.look_for_primary(self.instances)

    def look_for_primary(self, instances):
        timestamp=time.time()
        become_primary=False
        while (not become_primary) & (not self.shutdown_signal.is_set()):
            except_count=0
            for instance in instances:
                logging.info("Trying to connect instance {}".format(instance))
                try:
                    addr = "http://{ins}:7175/{ts}".format(ins=instance, ts=timestamp)
                    timestamp_resp = req.get(addr, timeout=10)
                    if timestamp_resp.status_code == 200:
                        logging.info("Found instance {} with higher primary timestamp. Attempting to become primary instead.".format(instance))
                        become_primary=True
                        #Get until the previous primary has shut down
                        while True:
                            req.get(addr)
                    else:
                        logging.info("Found instance {} with lower primary timestamp. Not attempting to become primary (if not one already).".format(instance))
                        become_primary=False
                        #TODO: break here?
                except Exception as e:
                    logging.info("Could not connect to instance {}. Exception:".format(instance))
                    logging.info(e)
                    except_count += 1
            #If we failed to connect all other nodes but did not become primary, let's become primary anyway
            if (except_count == len(instances)) & (become_primary == False):
                logging.info("Attempts to reach all other instances failed. Becoming primary.")
                become_primary=True
            #Let's wait a moment before retrying to find a primary
            if become_primary == False:
                logging.info("Not becoming primary. Sleeping 10s before checking again.")
                time.sleep(10)
        if become_primary:
            logging.info("Node dedicated as primary with timestamp {}.".format(timestamp))
        if self.shutdown_signal.is_set():
            logging.info("Primary lookup received signal to shut down.")

class WatcherThread(threading.Thread):

    def __init__(self, updater, lookup_thread, broadcast_thread):
        self.updater=updater
        self.lookup_thread=lookup_thread
        self.broadcast_thread=broadcast_thread
        threading.Thread.__init__(self)

    def run(self):
        while self.lookup_thread.is_alive() & self.broadcast_thread.is_alive():
            logging.info("All threads are running. Sleeping 10s before checking again.")
            time.sleep(10)
        self.updater.stop()
        self.updater.is_idle = False
        if self.broadcast_thread.is_alive():
            self.broadcast_thread.server.shutdown()
        if self.lookup_thread.is_alive():
            self.lookup_thread.shutdown_signal.set()

def run_primary_backup_model(updater, instances):
    while True:
        logging.info("Launching a lone primary lookup thread.")
        primary_lookup_thread = PrimaryLookupThread(instances)
        primary_lookup_thread.start()
        while primary_lookup_thread.is_alive():
            logging.info("Primary lookup is ongoing. Sleeping 10s before checking again.")
            time.sleep(10)
        logging.info("This node has been dedicated as primary. Starting the relevant threads.")
        primary_broadcast_thread = PrimaryBroadcasterThread(time.time())
        primary_broadcast_thread.start()
        logging.info("Broadcasting primary status.")
        primary_primary_lookup_thread = PrimaryLookupThread(instances)
        primary_primary_lookup_thread.start()
        logging.info("Looking up for other primaries.")
        watcher_thread=WatcherThread(updater, primary_primary_lookup_thread, primary_broadcast_thread)
        watcher_thread.start()
        logging.info("Watching the lookup and broadcasting threads.")
        run_bot_only(updater)
        if primary_broadcast_thread.is_alive():
            primary_broadcast_thread.server.shutdown()
        if primary_primary_lookup_thread.is_alive():
            primary_primary_lookup_thread.shutdown_signal.set()

def run_bot_only(updater):
    updater.start_polling()
    # run the bot until Ctrl-C
    logging.info("Bot ready to answer queries!")
    updater.idle()
    logging.info("Bot stopped answering queries.")
