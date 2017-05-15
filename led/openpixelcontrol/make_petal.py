#!/usr/bin/env python

# Make an openpixelcontrol JSON file that matches a single petal

#[ the 43 on the left side ]
#[ the 21 on the center bottom ]

#[ the 36 on the left inside ]
#[ the 28 on the left back ]

#[ the 36 on the right inside ]
#[ the 28 on the right back ]

#[ the 43 on the right side ]
#[ the 21 on the center top ]

# make everything z=0 


# Makes a curve that starts at an X value, and 
# petals are all made of curves
# pass in:
# The initial point x and y
# step_x is the amount of x space between pixels
# bend is the total amount of bend ( the furthest point )

# returns the list of lines

def make_curve_y(init_x, init_y, step_y, n_points, bend):
	if n_points == 0:
		return []

	lines = []
	x = init_x
	y = init_y
	bend_per_pixel = bend / ( n_points / 2 )

	# note: int here does an implicit floor, which is what we want, but as have
	# to handle the extra odd in the middle

	for p in range(0, int(n_points / 2) ):

		lines.append('  {"point": [%.2f, %.2f, %.2f]}' % (x, y, 0.0))
		x += bend_per_pixel
		y += step_y

    # add extra for odd
	if n_points % 2 == 1:
		lines.append('  {"point": [%.2f, %.2f, %.2f]}' % (x, y, 0.0))
		y += step_y

	for p in range(0, int( n_points / 2) ):
		lines.append('  {"point": [%.2f, %.2f, %.2f]}' % (x, y, 0.0))
		x -= bend_per_pixel
		y += step_y

	return lines

lines = []

# LEFT OUTER

# extend ( not append ) adds list elements to the end of a list
lines.extend( make_curve_y( 1.0, 0.00,  0.10, 43, -1.0 ) )

# comes back, in the center, no bend, a little peculiar
lines.extend( make_curve_y( 3.0, 4.30 , -0.10, 21, 0.0 ) )

# LEFT INNER

lines.extend( make_curve_y( 2.0, 0.35 , 0.10, 36, -0.5 ) )

lines.extend( make_curve_y( 2.0, 4.50 , 0.10, 28, -0.5 ) )

# RIGHT INNER

lines.extend( make_curve_y( 4.0, 0.35 , 0.10,  36, 0.5 ) )

lines.extend( make_curve_y( 4.0, 4.50 , 0.10, 28, 0.5 ) )

# RIGHT OUTER

# extend ( not append ) adds list elements to the end of a list
lines.extend( make_curve_y( 5.0, 0.00,  0.10, 43, 1.0 ) )

# comes back, in the center, no bend
lines.extend( make_curve_y( 3.0, 2.15 , -0.10, 21, 0.0 ) )

print( '[\n' + ',\n'.join(lines) + '\n]' )
