# Magnus Flora work projects

In this project we will have several functional units.

- The TechThulu ( or simulator )
- The JARVIS , which maps game state to back end actions
- The output modules, one of LED, SERVO, SOUND, which cause actions in "reality"
- The web test interface, ADA, which has a web page and allows all kinds of debugging
- Maybe a JARVIS simulator?

## TechThulu Simulator

The simultor is over in the /sim directory. You invoke it with python portal_sim.py , and the defaults are 
reasonable. It will come up on port 5050, and needs no extra infrastructure. No celery, no nothing. It opens
a local port and will run through its script, doing portal state changes.

## JARVIS

Jarvis is the module which polls the Simulator, determines the changes to portal state, and translates them into the
CELERY messages which each one of the control modules supports. Depending on what each output module supports,
the JARVIS unit might be more sophisticated. The JARVIS unit might, for example, decide that nothing has happened on the
portal and decide to run a demo sequence, or flash lights, or whatever. It should have a sensible mapping between portal
state and the invidual control states.

## The output modules

Each output module has Celery tasks that can be invoked, and has background processes it can run.

Each makes sense for the module itself, and will be negotiated with the module maker.

For example, "servo" has 8 leaves, and has positions the leaves can be set. The module worker will
receive messages, almost certainly "move to position", and do the necessary tasks. "hard" questions like sensing
where the arm is will be handled in the output module. The module may have "level" in terms of 0-8, for the level
of the portal, or may have 0-100, and make JARVIS map from those levels to the 0-8, that is part of the
negotiation between the artists and the control module writer.

### Servo

PLACE SERVO DETAILS HERE

### Audio

PLACE AUDIO DETAILS HERE

### LEDs

PLACE LED DETAILS HERE

## ADA - Web test

The goal is to have a simple HTML interface which can be used via a phone for both setup, and running demo,
and for debugging. The different control modules might have some "test modes" or "setup modes" which could be
exposed over Celery ( for example, Audio might have a global LEVEL which is only changed via the ADA interface ).

ADA should certainly be able to invoke Celery messages and route them to modules without JARVIS. But is should also be
able to invoke JARVIS' methods.

The ADA interface should be able to display debugging output from everywhere, if we can manage it.

# Test infrastructure

We may want to create a seperate JARVIS for testing, although I might prefer having a single JARVIS with test modes.
