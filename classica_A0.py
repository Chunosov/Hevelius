#! /usr/bin/env python
# -*- coding: utf-8 -*-

import hevelius
from hevelius import *

MIN_DEC = -30

def make_map():
	map = Map()
	map.read('classica_A0.template.svg')

	make_grid(map)
	make_stars(map)
	make_constellations(map)

	map.paste('{frame}', Frame.make_triplet(1159, 811, 0.5, 2, 2, 1, 0.5))

	map.write('classica_A0.generated.svg')


def make_grid(map):
	map.paste('{ra_grid}', Grid.make_hours_grid( \
		min_dec = MIN_DEC, max_dec = 80, skip_lines = [0, 6, 12, 18]))
		
	map.paste('{ra_ruler}', Grid.make_ra_ruler( \
		dec = MIN_DEC, frame_w = 1, ruler_w = 4, ticks = 360))
		
	map.paste('{dec_grid}', Grid.make_dec_grid( \
		min_dec = -20, max_dec = 80, step = 10, skip_lines = [0, 30, 60]))
		
	map.paste('{dec_grid_bold}', Grid.make_dec_grid_bold([30, 60]))

	map.paste('{equator}', Grid.make_equator())

	map.paste('{dec_ruler}', Grid.make_dec_ruler( \
		min_dec = MIN_DEC, frame_w = 0.5, ruler_w = 3, ticks = 120))
	
	
def make_stars(map):
	stars = Stars([s for s in Bsc.read() if s.DecD > MIN_DEC and s.Mag <= 5])
	for star in stars.stars: star.mag_index = get_mag_index(star)
	stars.show_stat()
	
	diameters = { 
		0: 6, 
		1: 5, 
		2: 4, 
		3: 3, 
		4: 2, 
		5: 1, 
		6: 0.5
	}
	
	map.paste('{star_circles}', stars.make_stars([0, 1, 2, 3, 4, 5], \
		lambda star: Stars.make_circle(star, diameters)))
		
	#map.paste('{star_circles_6}', stars.make_stars([6], \
	#	lambda star: Stars.make_circle(star, diameters)))
	
	map.paste('{star_crosses}', stars.make_stars([], \
		lambda star: Stars.make_cross(star, 6)))

	#map.paste('{star_stars}', stars.make_stars([0, 1, 2, 3, 4, 5], \
	#	lambda star: Stars.make_star(star)))
		
	#map.paste('{star_stars_6}', stars.make_stars([6], \
	#	lambda star: Stars.make_star(star)))
	
	#map.paste('{star_numbers}', stars.make_stars([0, 1, 2, 3, 4], \
	#	lambda star: Stars.make_number(star)))

	
from constellations import Constellations_IAU_ex
from constellations import Constellations_2000

def make_constellations(map):
	cons1 = Constellations_IAU_ex()
	cons1.read()
	
	#cons2 = Constellations_1875()
	#cons2.read()

	cons3 = Constellations_2000()
	cons3.read()

	#abbrs = ['Ori', 'Dra']
	#abbrs = ['UMi', 'UMa', 'Cep']
	abbrs = []

	map.paste('{constellation_boundaries_iau}', cons1.make_bounds(abbrs, \
		lambda con: con.make_bound_polar(MIN_DEC, 'iau', 0.7)))
	
	#map.paste('{constellation_boundaries_1875}', cons2.make_bounds(abbrs, \
	#	lambda con: con.make_bound_polar(MIN_DEC, '1875')))

	map.paste('{constellation_boundaries_2000}', cons3.make_bounds(abbrs, \
		lambda con: con.make_bound_decart(MIN_DEC, '2000')))
		
	map.paste('{constellation_bound_points}', cons1.make_bound_point_numbers(abbrs, MIN_DEC))

def get_mag_index(star):
	if star.Mag <= 0.5: return 0
	elif star.Mag <= 1.5: return 1
	elif star.Mag <= 2.5: return 2
	elif star.Mag <= 3.5: return 3
	elif star.Mag <= 4.5: return 4
	elif star.Mag <= 5.5: return 5
	else: return 6

def px(mm):
	return hevelius.pixel(mm)

if __name__ == '__main__':
	make_map()
