# Running without pixels

There is a cute project called "openpixelcontrol" which allows easily 
running and visualizaing on Mac using OpenGL.

Catch is you have to build a model. The model isn't really easy
to build, but once you have it you go faster.

http://github.com/zestyping/openpixelcontrol

## Warning !

The Petal generator I wrote makes a bigger petal than zestyping 
shows by default. You can easily scroll around using a standard
click-drag motion, but you'll need to SHIFT-drag to zoom !!!

## Generate a petal

Since these are impossible to do by hand, I have written a little
python program to generate a single petal. This is a simple program 
to draw a curve, then has the 8 hardcoded curves.

```
python make_petal.py > petal.json
```

## Generate many petals

The `make_petals.py`  does even more, and wraps the previous function

It puts the petals all in a row, instead of a nice circle

## A single petal

[ the 43 on the left side ]
[ the 21 on the center bottom ]

[ the 36 on the left inside ]
[ the 28 on the left back ]

[ the 36 on the right inside ]
[ the 28 on the right back ]

[ the 43 on the right side ]
[ the 21 on the center top ]

## Format JSON

[
 {"point": [ 1.32, 0.00, 1.32]},
 {"point": [ 1.32, 0.00, 1.21]}
]

 
