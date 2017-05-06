# Magnus Flora Rest Framework

This simple framework allows independant processes to be running separate rest systems.

It allows trivial implementation of the architecture described at the root with few dependancies.

## required software

Python 3.6 or better is used, to be installed with PyEnv ( below )

Supervisord

Git

This directory

Other packages required by each individual unit ( see below )

## Configuration

A global config.py is used. This is a single python object that may have state used in any of the modules.
It gets attached to the app object, and is referenced as either g_config or app["config"] in many places.
Use the examples

You may also expand the command line parameters. See the examples.

## Running in "production"

Copy all the supervisor files into the supervisor directory

You can supervisor control things

## Development

An example framework program, "template.py", is given.

### Important notes!

Please using the logging module. It'll be very useful sometimes. Please remember to use the format:

```
logging.info(" this is a message %s ",msg)
```

Logging does not support the Python3 syntax of `print(" thing1 ",m)` which makes it hard to remember sometimes

### Set the log level

Invoke any unit with the debug parameter to set the debug level of that unit.

Such as to make noisy:
```
python led.py -d DEBUG
```

or to make quiet:
```
python jarvis.py -d WARNING
```

## Starting everything

I have included a simple file `./start_all.sh` that starts all the units.

Notice this starts things in background mode. You'll probably want to debug in foreground mode, so this script may be of limited use. We will move all of this to supervisor eventually.

Remember that you can't have two copies running at the same time of a certain thing, the ports collide. You will see the following message:

```
OSError: [Errno 48] error while attempting to bind on address ('0.0.0.0', 2003): address already in use
```

and you'll need to hunt down the other process and kill it.

## Starting the Tecthulu Simulator

Note that there are many simulation files, I have included one that's long and interesting.
Feel free to make your own, please check them in.

```
cd ../sim
python portal_sim.py -f sequential_sim.json
```

