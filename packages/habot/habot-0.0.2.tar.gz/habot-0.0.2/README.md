# habot
A Python package to run highly available Telegram bots

## Usage

Install habot with pip:

```
pip install -i https://test.pypi.org/simple/ habot
```

(Habot will move to proper pypi at some later date)

Then import and you have two interesting functions available for you code:

```
import habot
habot.bot.run_primary_backup_model(updater, instances)
habot.bot.run_bot_only(updater)
```

Of these the latter will only `start_polling()` and `idle()` for an `Updater` of a Telegram bot made using `python-telegram-bot` package.

`run_primary_backup_model` will in addition to the bot run a primary-backup system between the `instances`. The instance is a list of IPs or host/domain names. The workings of the primary-backup model are described in the section below.

## How the primary-backup model works

In the primary-backup model, bot code can be started for multiple instances. Primary is the instance that has _become primary_ with the lowest timestamp.

First every instance starts looking for a primary. In case ans instance can find no primary:
1. The instance becomes primary with its current timestamp
2. The instance starts broadcasting that timestamp for other instances by spawning a HTTP server thread
3. Another thread of the instance keeps looking for potential alternative primary with a lower timestamp
4. A watcher thread checks that the other two threads remain alive.
5. Bot code is started in the main thread.

In case the instance does find a primary, it just keeps periodically looking for a primary in the main thread.

If the primary instance A finds another instance B that has become primary with lower timestamp:
1. A stops all its threads.
2. And restarts the cycle by looking for a primary instance.


## Security

The instances communicate between themselves over HTTP
