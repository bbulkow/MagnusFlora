# Running without pixels

There is a cute project called "openpixelcontrol" which allows easily 
running and visualizaing on Mac using OpenGL.

Catch is you have to build a model. The model isn't really easy
to build, but once you have it you go faster.

http://github.com/zestyping/openpixelcontrol

## Generate a petal

Since these are impossible to do by hand, I have written a little
python program to generate a single petal. This is a simple program 
to draw a curve, then has the 8 hardcoded curves.

```
python make_petal.py > petal.json
```

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

 
