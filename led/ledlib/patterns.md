# Portal LED Patterns

Ignoring wiring, each petal/reso has:
Left Outer Curve (LOC/43)
Right Outer Curve (ROC/43)
Left Inner Curve (LIC/36)
Right Inner Curve (RIC/36)
Left Back (28)
Right Back (28)
Center Straight (42)

There will be two types of patterns:  finite and infinite.

Finite patterns are an event, infinite patterns are a state

## STATE VARIABLES:
* Portal faction control
* Portal level
* Reso level
* Reso decay level
* Frack active
* reso number (used by some patterns)

## ARTISTIC VARIABLES:
* default reso pattern (intended to change periodically)
* default filler color (morning, afternoon, evening, night.)

## EVENTS:
* Null Event
* Initial Portal Wakeup (Chaotic random all colors, fade to solid)
* Reso Deploy/Upgrade
* Reso Destroy
* Portal Neutralized (Red Flash)
* Portal Captured (Faction Color Flash)
* Frack End (White Flash)

Each reso will have a control thread, which will poll shared memory for
heartbeat (or poll system clock) and state changes.

Any trigger will define:
Portal State
Reso State
Finite Pattern
Infinite Pattern


## FINITE PATTERNS

(See events)

## INFINITE PATTERNS

* Spiral (single path , clockwise or CCW based on reso number)
* spiral with burst from center after a few iterations
* chase, with faction on ROC/TOP/LOC and overall level on CS
* wave, chase from base to tip with time offset based on reso number

