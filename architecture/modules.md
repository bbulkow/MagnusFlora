Software design will be modular so that bits can be tested separately. 

Module 1:  Interface

Input:  portal state (from Techthulhu module, Intel scrape, or demo control file)
Config:  polling interval
Config:  portal ID (in case we are using Intel/IITC scrape)
Outut:  Data structure comprising complete portal state

Note:  I envision this installation to be reusable via intel scrape after the event.  Would be cool to bring it to xfac events.

Goal:  Make as much of this testable without Techthulhu as possible.  Isolate Techthulhu component

Module 2:  LED Art

1. RGB Color definitions for all portal components:
	1. Resos level 1-8
	2. Mods - common, rare, very rare, SBUL, AXA
	3. Fracker, 
	4. Faction:  Res, ENL, Neutral, Red death flash

Note:  White is very expensive on a power budget even at 70%.  

2. LED layout patterns for all supported attachments:
	1. Petal (reso)
	2. Leaf (mod slot)
	3. Pistil/Stamen (Fracker/Shard/Beacon)
	4. Simple 24 LED strip  (I envision testing software with a FadeCandy hooked to 8 simple LED strips)
	5. Simple 12 LED circle
	6. Stem (stretch goal): set of LED strips running up the stem; I envision a simple spiral chase up the stem (faction color, portal level, health percent.)

3. Animation patterns (these would need to be defined in the intersection between layout and portal component.)

Any given pair would have one or more animation patterns defined; animation zero for every pair would be a simple chase sequence.)

Base blink rate to be defined globally -- no syncopation.

Module 3:  Audio

Module 4:  Petal Servos


