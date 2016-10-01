#! /usr/bin/env python
# -*- coding: utf-8 -*-

import hevelius
from hevelius import *

MAP_MIN_DEC = -30

def make_map():
	hevelius.MAP_SCALE_DEC = 3
	
	map = Map()
	map.read('classica_A4.template.svg')

	make_grid(map)
	make_stars(map)

	map.paste('{frame}', Frame.make_doublet(190, 277, 1, 1, 0.5))

	map.write('classica_A4.generated.svg')
	
	# translate(372.040515,526.18)


def make_grid(map):
	map.paste('{ra_grid}', Grid.make_hours_grid( \
		min_dec = MAP_MIN_DEC, max_dec = 75))
		
	#map.paste('{ra_ruler}', Grid.make_ra_ruler( \
	#	dec = MAP_MIN_DEC, frame_w = 1, ruler_w = 4, ticks = 360))
		
	map.paste('{dec_grid}', Grid.make_dec_grid( \
		min_dec = MAP_MIN_DEC, max_dec = 75, step = 15, skip_lines = [0]))
		
	map.paste('{dec_grid_bold}', Grid.make_dec_grid_bold([MAP_MIN_DEC]))

	map.paste('{equator}', Grid.make_equator())

	#map.paste('{dec_ruler}', Grid.make_dec_ruler( \
	#	min_dec = MAP_MIN_DEC, frame_w = 0.5, ruler_w = 3, ticks = 120))
	
	map.paste('{map_back}', Grid.make_back(MAP_MIN_DEC))
	
	
def make_stars(map):
	stars = Stars([s for s in Bsc.read() if s.DecD >= -30 and s.Mag <= 5.5])
	for star in stars.stars: star.mag_index = get_mag_index(star)
	stars.show_stat()
	
	diameters = { 
		1: 2.5, 
		2: 2.0, 
		3: 1.5, 
		4: 1.0, 
		5: 0.5 
	}
	
	map.paste('{star_circles}', stars.make_stars([1, 2, 3, 4], \
		lambda star: Stars.make_circle(star, diameters)))
		
	map.paste('{star_circles_6}', stars.make_stars([5], \
		lambda star: Stars.make_circle(star, diameters)))
	
	map.paste('{star_crosses}', stars.make_stars([], \
		lambda star: Stars.make_cross(star, 6)))


def get_mag_index(star):
	if star.Mag <= 1.5: return 1
	elif star.Mag <= 2.5: return 2
	elif star.Mag <= 3.5: return 3
	elif star.Mag <= 4.5: return 4
	else: return 5


if __name__ == '__main__':
	make_map()
