psg-stl
-------

A little python script to generate STL models of the five platonic solids.

## The solids

### Dodecahedron

[This article on Wikipedia](https://en.wikipedia.org/wiki/Dodecahedron) describes the coordinates of the dodecahedron. The vertices are formed as follows:

	( ±1,   ±1,   ±1   )
	(  0,   ±1/φ, ±φ   )
	( ±1/φ, ±φ,    0   )
	( ±φ,    0,   ±1/φ )

	φ = (1 + √5) / 2 (the golden ratio)

The following image displays the vertices, as well as the indices:

![dodecahedron diagram](docs/dodecahedron_vertices.png)

### Icosahedron

[Wikipedia again describes the Icosahedron](https://en.wikipedia.org/wiki/Regular_icosahedron) and the vertices are formed as follows:

	(  0, ±1, ±φ )
	( ±1, ±φ,  0 )
	( ±φ,  0, ±1 )

	φ = (1 + √5) / 2 (the golden ratio)

Instead of calculating indices with the help of a diagram, I instead decided to ‘lift’ the calculated vertices and indices from [Andreas Kahler’s blog](http://blog.andreaskahler.com/2009/06/creating-icosphere-mesh-in-code.html). Apologies for cheating.
