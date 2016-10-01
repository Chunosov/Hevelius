#! /usr/bin/env python
# -*- coding: utf-8 -*-

import math
import random

MAP_SCALE_DEC = 10 # px/deg
	
	
class EquPoint:
	def set_ra(self, h, m, s):
		self.RaH = int(h)
		self.RaM = int(m)
		self.RaS = float(s)
		self.Ra = self.RaH + self.RaM / 60.0 + self.RaS / 3600.0
		
	def set_ra_hours(self, h):
		self.Ra = float(h)
		self.RaH = int(math.floor(self.Ra))
		m = 60.0 * (self.Ra - self.RaH)
		self.RaM = int(math.floor(m))
		self.RaS = 60 * (m - self.RaM)
		
	def set_dec(self, d, m, s):
		self.DecD = int(d)
		self.DecM = int(m)
		self.DecS = float(s)
		self.Dec = math.fabs(self.DecD) + self.DecM / 60.0 + self.DecS / 3600.0
		self.Dec = math.copysign(self.Dec, self.DecD)
		
	def set_dec_deg(self, d):
		self.Dec = float(d)
		self.DecD = int(math.floor(self.Dec) if self.Dec > 0 else math.ceil(self.Dec))
		m = 60.0 * math.fabs(self.Dec - self.DecD)
		self.DecM = int(math.floor(m))
		self.DecS = 60 * (m - self.DecM)

	def ra_str(self):
		return '{:0>2}:{:0>2}:{:0>7.4f}[{:0>7.4f}]'.format(self.RaH, self.RaM, self.RaS, self.Ra)
		
	def dec_str(self):
		return '{:0=+3}^{:0>2}\'{:0>7.4f}"[{:=+08.4f}]'.format(self.DecD, self.DecM, self.DecS, self.Dec)
		
	def __str__(self):
		return '{:0>7.4f} {:=+08.4f}'.format(self.Ra, self.Dec)
		
	def to_screen(self):
		return coord_equ_to_xy(self.Ra, self.Dec)

	
class Star(EquPoint):
	def print_out(self):
		print('{0: >4}: {1} {2} {3}m'.format(self.HR, self.ra_str(), self.dec_str(), self.Mag))


class Bsc:	
	def read():
		count = 1
		max_count = 0 # set 0 to full reading
		stars = []
		with open('catalogs/bsc5.dat') as data:
			for line in data:
				star = Star()
				try:
					Bsc.parse(star, line)
					stars.append(star)
				except ValueError as ex:
					print('Error reading star %d: %s' % (star.HR, ex))
				if count == max_count:
					break
				count = count + 1
		print ('Star catalog read. Stars: %d' % len(stars))
		return stars
		
	def parse(star, line):
		star.HR = int(line[0:4]) # Harvard Revised Number = Bright Star Number 
		star.Label = line[4:14].strip() # Name, generally Bayer and/or Flamsteed name 
		star.set_ra( \
			line[75:77], # Hours RA, equinox J2000, epoch 2000.0
			line[77:79], # Minutes RA, equinox J2000, epoch 2000.0
			line[79:83]) # Seconds RA, equinox J2000, epoch 2000.0
		star.set_dec( \
			line[83:86], # Degrees Dec, equinox J2000, epoch 2000.0
			line[86:88], # Minutes Dec, equinox J2000, epoch 2000.0
			line[88:90]) # Seconds Dec, equinox J2000, epoch 2000.0
		star.Mag = float(line[102:107]) # Visual magnitude


class Map:
	def read(self, file_name):
		with open(file_name) as f: self.map = f.readlines()
		print('Source map file read:', file_name)
	
	def write(self, file_name):
		with open(file_name, 'w') as f: f.writelines(self.map)
		print('Generated map file written:', file_name)

	def paste(self, place, what):
		map = []
		for line in self.map:
			if line.strip() == place:
				if isinstance(what, str): 
					map.append(what)
				else: 
					for line in what:	
						map.append(line)
			else:
				map.append(line)
		self.map = map


class Frame:
	def make_doublet(w, h, frame_outer_t, delta, frame_inner_t):
		frame_outer_w = w
		frame_outer_h = h
		frame_inner_w = frame_outer_w - frame_outer_t - frame_inner_t - delta
		frame_inner_h = frame_outer_h - frame_outer_t - frame_inner_t - delta
		return '''<g id="frame_triplet">
			<rect id="frame_outer" x="-{2}mm" y="-{3}mm" width="{4}mm" height="{5}mm" style="fill:none;stroke:#000000;stroke-width:{0}mm;"/>
			<rect id="frame_middle" x="-{6}mm" y="-{7}mm" width="{8}mm" height="{9}mm" style="fill:none;stroke:#000000;stroke-width:{1}mm;"/>
			</g>'''.format(frame_outer_t, frame_inner_t, \
			frame_outer_w/2.0, frame_outer_h/2.0, frame_outer_w, frame_outer_h, \
			frame_inner_w/2.0, frame_inner_h/2.0, frame_inner_w, frame_inner_h)


	def make_triplet(w, h, frame_outer_t, delta_outer_middle, frame_middle_t, delta_inner_middle, frame_inner_t):
		frame_outer_w = w
		frame_outer_h = h
		frame_middle_w = frame_outer_w - frame_outer_t - frame_middle_t - delta_outer_middle
		frame_middle_h = frame_outer_h - frame_outer_t - frame_middle_t - delta_outer_middle
		frame_inner_w = frame_middle_w - frame_inner_t - frame_middle_t - delta_inner_middle
		frame_inner_h = frame_middle_h - frame_inner_t - frame_middle_t - delta_inner_middle
		return '''<g id="frame_triplet">
			<rect id="frame_outer" x="-{3}mm" y="-{4}mm" width="{5}mm" height="{6}mm" style="fill:none;stroke:#000000;stroke-width:{0}mm;"/>
			<rect id="frame_middle" x="-{7}mm" y="-{8}mm" width="{9}mm" height="{10}mm" style="fill:none;stroke:#000000;stroke-width:{1}mm;"/>
			<rect id="frame_inner" x="-{11}mm" y="-{12}mm" width="{13}mm" height="{14}mm" style="fill:none;stroke:#000000;stroke-width:{2}mm;"/>
			</g>'''.format(frame_outer_t, frame_middle_t, frame_inner_t, \
			frame_outer_w/2.0, frame_outer_h/2.0, frame_outer_w, frame_outer_h, \
			frame_middle_w/2.0, frame_middle_h/2.0, frame_middle_w, frame_middle_h, \
			frame_inner_w/2.0, frame_inner_h/2.0, frame_inner_w, frame_inner_h)
	

class Grid:	
	def make_hours_grid(min_dec, max_dec, skip_lines = None):
		'''
		min_dec		Lowest position of RA-grid line
		max_dec		Highest position of RA grid line
		skip_lines	List of grid lines which should not be painted as they will
					be obscured by another top laying lines, e.g. declination rulers
		'''
		for ra in range(24):
			if not skip_lines or ra not in skip_lines:
				c1 = coord_equ_to_xy(ra, min_dec)
				c2 = coord_equ_to_xy(ra, max_dec)
				yield '<line id="ra_grid_{0}" x1="{1}" y1 ="{2}" x2="{3}" y2="{4}"/>\n' \
					.format(ra, c1[0], c1[1], c2[0], c2[1])

					
	def make_ra_ruler(dec, frame_w, ruler_w, ticks):
		'''
		dec 		Declination of inner border
		frame_w		Width of inner and outer border
		ruler_w		Width of ruler between borders
		ticks		Dashes count, ruler precision
		'''
		frame_in_r = (90 - dec) * MAP_SCALE_DEC
		frame_out_r = frame_in_r + frame_w + ruler_w
		ruler_r = frame_in_r + frame_w/2.0 + ruler_w/2.0
		dash_size = 2 * math.pi * ruler_r / float(ticks)
		return '''
			<circle id="ra_ruler_inner_frame" r="{0}" cx="0" cy="0" style="fill:none;stroke:#000000;stroke-width:{1}"/>
			<circle id="ra_ruler_ruler" r="{2}" cx="0" cy="0" style="fill:none;stroke:#000000;stroke-width:{3};stroke-dasharray:{4},{4}"/>
			<circle id="ra_ruler_outer_frame" r="{5}" cx="0" cy="0" style="fill:none;stroke:#000000;stroke-width:{1}"/>
			'''.format(frame_in_r, frame_w, ruler_r, ruler_w, dash_size, frame_out_r)
	
	
	def make_dec_grid(min_dec, max_dec, step, skip_lines = None):
		'''
		min_dec		Lowest grid line declination
		max_dec		Highest grid line declination
		step		Distance between grid lines
		skip_lines	List of grid lines which should not be painted as they will
					be obscured by another top laying lines, e.g. equator line
		'''
		for dec in range(min_dec, max_dec + step, step):
			if not skip_lines or dec not in skip_lines:
				yield '<circle id="dec_grid_{0}" r="{1}" cx="0" cy="0"/>\n' \
					.format(90 - dec, (90 - dec) * MAP_SCALE_DEC)
			
			
	def make_dec_grid_bold(lines):			
		for dec in lines:
			yield '<circle id="dec_grid_b_{0}" r="{1}" cx="0" cy="0"/>\n' \
				.format(90 - dec, (90 - dec) * MAP_SCALE_DEC)
	
	
	def make_equator():
		return '<circle id="equator" r="{0}" cx="0" cy="0"/>\n'.format(90 * MAP_SCALE_DEC)
	

	def make_dec_ruler(min_dec, frame_w, ruler_w, ticks):
		'''
		dec 		Declination of ruler end
		frame_w		Border width
		ruler_w		Width of ruler between borders
		ticks		Dashes count, ruler precision
		'''
		L = (90 - min_dec) * MAP_SCALE_DEC
		dash_size = L / 2.0 / float(ticks) 
		X = (ruler_w + frame_w)/2.0
		return '''<g id="dec_ruler_v">
			<line id="dec_ruler_v_ruler" x1="0" y1="-{0}" x2="0" y2="{0}" style="fill:none;stroke:#000000;stroke-width:{3};stroke-dasharray:{2},{2}"/>
			<line id="dec_ruler_v_frame1" x1="-{1}" y1="-{0}" x2="-{1}" y2="{0}" style="fill:none;stroke:#000000;stroke-width:{4}"/>
			<line id="dec_ruler_v_frame2" x1="{1}" y1="-{0}" x2="{1}" y2="{0}" style="fill:none;stroke:#000000;stroke-width:{4}"/></g>
			<g id="dec_ruler_h">
			<line id="dec_ruler_h_ruler" y1="0" x1="-{0}" y2="0" x2="{0}" style="fill:none;stroke:#000000;stroke-width:{3};stroke-dasharray:{2},{2}"/>
			<line id="dec_ruler_h_frame1" y1="-{1}" x1="-{0}" y2="-{1}" x2="{0}" style="fill:none;stroke:#000000;stroke-width:{4}"/>
			<line id="dec_ruler_h_frame2" y1="{1}" x1="-{0}" y2="{1}" x2="{0}" style="fill:none;stroke:#000000;stroke-width:{4}"/></g>
			'''.format(L, X, dash_size, ruler_w, frame_w)
			
	
	def make_back(min_dec):
		return '<circle r="{0}" cx="0" cy="0"/>\n'.format((90 - min_dec) * MAP_SCALE_DEC)
	

class Stars:
	def __init__(self, stars):
		self.stars = stars
		for star in self.stars:
			star.ScreenX, star.ScreenY = star.to_screen()
	
	def show_stat(self):
		counts = {}
		for star in self.stars:
			counts[star.mag_index] = counts.get(star.mag_index, 0) + 1
		print('Stars count for mapping:')
		for mag, count in counts.items():
			print('{0:0=+4.1f}m: {1: >4}'.format(mag, count))
		print('Total:', len(self.stars))
	
	def make_stars(self, mags, method):
		for star in self.stars:
			if not mags or star.mag_index in mags:
				yield method(star)
	
	def make_circle(star, diams):
		return '<circle id="star_circle_{0}" r="{1}mm" cx="{2}" cy="{3}"/>\n' \
			.format(star.HR, diams[star.mag_index]/2.0, star.ScreenX, star.ScreenY)
		
	def make_cross(star, size):	
		x, y = star.ScreenX, star.ScreenY
		return '<path id="star_cross_{0}" d="M {1},{2} L {3},{4} M {5},{6} L {7},{8}"/>\n' \
			.format(star.HR, x - size, y, x + size, y, x, y - size, x, y + size)
		
	def make_star(star):
		return '''<use id="star_star_{0}" xlink:href="#source_star_star_{1}" 
			transform="translate({2},{3}) rotate({4})"/>\n'''.format( \
			star.HR, star.mag_index, star.ScreenX, star.ScreenY, random.randint(0, 90))
			
	def make_number(star):
		return '<text x="{0}" y="{1}">{2}</text>'. \
			format(star.ScreenX, -star.ScreenY, star.HR)
		

def coord_equ_to_xy(ra, dec):
	ra = 2 * math.pi - ra * math.pi / 12.0 # RA raises CW but trigonometric angles raise CCW
	dec = 90 - dec # dist from equator -> dist from pole
	return dec * math.cos(ra) * MAP_SCALE_DEC, dec * math.sin(ra) * MAP_SCALE_DEC

	
def pixel(mm):
	return 3.54330706 * mm
