#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hevelius
from hevelius import EquPoint


def main():
	#show()
	#make_optimized_iau_data_file()
	#collect_cons_abbrs()
	pass

ABBRS = [ \
	'and', 'ant', 'aps', 'aqr', 'aql', 'ara', 'ari', 'aur', 'boo',
	'cae', 'cam', 'cnc', 'cvn', 'cma', 'cmi', 'cap', 'car', 'cas', 
	'cen', 'cep', 'cet', 'cha', 'cir', 'col', 'com', 'cra', 'crb',
	'crv', 'crt', 'cru', 'cyg', 'del', 'dor', 'dra', 'equ', 'eri', 
	'for', 'gem', 'gru', 'her', 'hor', 'hya', 'hyi', 'ind', 'lac', 
	'leo', 'lmi', 'lep', 'lib', 'lup', 'lyn', 'lyr', 'men', 'mic', 
	'mon', 'mus', 'nor', 'oct', 'oph', 'ori', 'pav', 'peg', 'per', 
	'phe', 'pic', 'psc', 'psa', 'pup', 'pyx', 'ret', 'sge', 'sgr', 
	'sco', 'scl', 'sct', 'ser', 'sex', 'tau', 'tel', 'tri', 'tra', 
	'tuc', 'uma', 'umi', 'vel', 'vir', 'vol', 'vul']

def show():
	cons = Constellations_IAU()
	cons.read()
	show_all(cons);
	show_bounds(cons, ['Ant'])

def show_all(cons):
	for con in enumerate(cons.Cons, 1):
		print('{0:>02} {1} {2} ({3})'.format( \
			con[0], con[1].Abbr, con[1].NameLat, len(con[1].Bounds)))
		
def show_bounds(cons, abbrs):		
	for con in cons.get(abbrs):
		print(con.NameLat)
		for point in con.Bounds:
			print(point)
		print()

def make_optimized_iau_data_file():
	cons = Constellations_IAU()
	cons.read()
	data = []
	count = 1
	segments = []
	for con in cons.Cons:
		if con.Bounds:
			for n, p2 in enumerate(con.Bounds):
				if n > 0:
					segments.append([p1, p2, con.Abbr])
				p1 = p2
			segments.append([p2, con.Bounds[0], con.Abbr])
	#save_segments(segments)
	for con in cons.Cons:
		if con.Bounds:
			for n, p2 in enumerate(con.Bounds):
				if n == 0:
					p1 = con.Bounds[-1]
				for s1, s2, abbr in segments:
					if abbr != con.Abbr:
						if (same_point(s1, p1) and same_point(s2, p2)) \
						or (same_point(s1, p2) and same_point(s2, p1)):
							neib = abbr
							break
				data.append('{0:0>4}|{1:0>7.4f}|{2:=+011.7f}|{3}|{4}\n' \
					.format(count, p2.Ra, p2.Dec, con.Abbr, neib))
				p1 = p2
				count += 1
			data.append('\n')
	with open('catalogs\~constellation_bounds_1.dat', 'w') as f: 
		f.writelines(data)
	
def save_segments(segments):	
	with open('catalogs\~constellation_bounds_seg.dat', 'w') as f: 
		f.writelines(['{0:0>7.4f} {1:0=+011.7f} | {2:0>7.4f} {3:0=+011.7f} | {4}\n' \
			.format(s1.Ra, s1.Dec, s2.Ra, s2.Dec, abbr)	for s1, s2, abbr in segments])
	
def same_point(p1, p2):
	return p1.Ra == p2.Ra and p1.Dec == p2.Dec
	#return same_ra(p1.Ra, p2.Ra) and same_dec(p1.Dec, p2.Dec)

def same_ra(v1, v2):
	return abs(v1 - v2) < 0.0001
	
def same_dec(v1, v2):
	return abs(v1 - v2) < 0.0000001


def collect_cons_abbrs():
	'''
	Makes string list of abbreviations for variable Constellations.ABBRS
	'''
	abbrs = ""
	cons = Constellations()
	cons.read()
	for con in cons.Cons:
		abbrs += "'{0}', ".format(con.AbbrLow)
	abbrs = abbrs.strip().strip(',')
	with open('catalogs/~constellation_abbrs.dat', 'w') as f:
		f.writelines(abbrs)
	print('{0}\nAbbreviations written: {1}\nOK'.format(abbrs, len(cons.Cons)))


class Constellation:
	Processed = []
	
	def make_bound_decart(self, min_dec, id_prefix):
		if not self.Bounds: return ''
		path = ''
		for point in self.Bounds:
			path += '{0[0]},{0[1]} L '.format(point.to_screen())
		return '<path id="bound_{0}_{1}" d="M {2} Z"/>\n' \
			.format(id_prefix, self.AbbrLow, path.strip(' L'))
			
	def make_bound_polar(self, min_dec, id_prefix, fuzzy = None):
		if not self.Bounds: return ''
		p1 = self.Bounds[0]
		path = 'M {0[0]},{0[1]}'.format(p1.to_screen())
		for i, p2 in enumerate(self.Bounds): 
			if i > 0:
				path += self.make_bound_polar_section_1(p1, p2, fuzzy, min_dec)
				p1 = p2
		path += self.make_bound_polar_section_1(p1, self.Bounds[0], fuzzy, min_dec)
		return '<path id="bound_{0}_{1}" d="{2}"/>\n' \
			.format(id_prefix, self.AbbrLow, path)
			
	def make_bound_polar_section_1(self, p1, p2, fuzzy, min_dec):
		if p2.Neib and p2.Neib in Constellation.Processed:
			return ''
		if self.need_polar_arc(p1, p2, fuzzy):
			if p1.Dec > min_dec and p2.Dec > min_dec:
				return 'M {0[0]},{0[1]} {1}'.format( \
					p1.to_screen(), self.make_polar_arc(p1, p2))
		else:
			if p1.Dec > min_dec or p2.Dec > min_dec:
				dr, dd = p2.Ra - p1.Ra, abs(p2.Dec - p1.Dec)
				if p1.Dec < min_dec and p2.Dec > min_dec:
					ra1, dec1 = p1.Ra + dr*(min_dec - p1.Dec)/dd, min_dec
				else:
					ra1, dec1 = p1.Ra, p1.Dec
				if p1.Dec > min_dec and p2.Dec < min_dec:
					ra2, dec2 = p2.Ra + dr*(p2.Dec - min_dec)/dd, min_dec
				else:
					ra2, dec2 = p2.Ra, p2.Dec
				return 'M {0[0]},{0[1]} L {1[0]},{1[1]}'.format( \
					hevelius.coord_equ_to_xy(ra1, dec1), \
					hevelius.coord_equ_to_xy(ra2, dec2))
		return ''

	def make_bound_polar_section_2(self, p1, p2, fuzzy, min_dec):
		if self.need_polar_arc(p1, p2, fuzzy):
			return self.make_polar_arc(p1, p2)
		else:
			return 'L {1[0]},{1[1]}'.format(p1.to_screen(), p2.to_screen())
				
	def need_polar_arc(self, p1, p2, fuzzy):
		return p2.Arc or abs(p2.Dec - p1.Dec) < (fuzzy if fuzzy else 0.0001)
				
	def make_polar_arc(self, p1, p2):
		direction = 1 if (p1.Ra > p2.Ra) else 0
		if abs(p1.Ra - p2.Ra) > 12: # simple check for crossing 0h line
			direction = 0 if direction == 1 else 1
		r = p2.ArcR if p2.ArcR else (90 - (p1.Dec + p2.Dec) / 2.0)
		return 'A {1},{1} 0 0,{2} {0[0]},{0[1]}'.format( \
			p2.to_screen(), r * hevelius.MAP_SCALE_DEC, direction)


class Constellations:
	'''
	General constellations data processor
	'''
	def __init__(self):
		self.BoundsDataFile = None
		
	def read(self):	
		self.read_names()
		self.read_bounds()
		print('Constellations read. Count: %d' % len(self.Cons))

	def read_names(self):
		self.Cons = []
		with open('catalogs/constellation_names.dat', encoding='utf-8-sig') as data:
			for line in data:
				self.parse_name_line(line)
				
	def read_bounds(self):
		if self.BoundsDataFile:
			with open(self.BoundsDataFile) as data:
				for line in data:
					if line.strip(): 
						try:
							self.parse_bound_line(line)
						except Exception as ex:
							print('Error reading line: %s%s\n' % (line, ex))

	def parse_name_line(self, line):
		parts = [s.strip() for s in line.split('\t') if s]
		con = Constellation()
		con.Abbr = parts[1]
		con.AbbrLow = parts[1].lower()
		con.NameLat = parts[0]
		con.NameRus = parts[4]
		con.Bounds = []
		self.Cons.append(con)
		
	def parse_bound_line(self, line):
		pass

	def make_bounds(self, abbrs, method):
		bounds = []
		Constellation.Processed = []
		for con in self.get(abbrs) if abbrs else self.Cons:
			con_bounds = method(con)
			if isinstance(con_bounds, str):
				bounds.append(con_bounds)
			else:
				for line in con_bounds:
					bounds.append(line)
			con.Processed.append(con.Abbr)
		return bounds
		
	def make_bound_point_numbers(self, abbrs, min_dec):
		processed = []
		for con in self.get(abbrs) if abbrs else self.Cons:
			if con.Bounds:
				for p in con.Bounds:
					if p.Dec < min_dec:
						continue
					found = False
					for point in processed:
						if p.Ra == point.Ra and p.Dec == point.Dec:
							point.Descr = '{0} {1}{2}'.format(point.Descr, con.AbbrLow, p.Index) 
							found = True
							break
					if not found:
						p.Descr = '{0}{1}'.format(con.AbbrLow, p.Index) 
						processed.append(p)
		for p in processed:
			x, y = p.to_screen()
			yield '''<circle id="con_bound_point_{2}" r="1" cx="{0}" cy="{1}"/>
				<text id="con_bound_number_{2}" x="{0}" y="{1}">{3}</text>\n''' \
				.format(x, -y, p.Index, p.Descr)
		
	def get(self, abbrs):
		cons = []
		if abbrs:
			for abbr in [abbr.lower() for abbr in abbrs]:
				cons.extend([c for c in self.Cons if c.AbbrLow == abbr])
		return cons


class Constellations_IAU (Constellations):
	'''
	Processor for constellation boundaries data from IAU
	http://www.iau.org/public/themes/constellations/
	'''
	def read(self):	
		self.BoundsDataFile = 'catalogs/constellation_bounds.dat'
		Constellations.read(self)

	def parse_bound_line(self, line):
		ra, dec, abbr = [s.lower().strip() for s in line.split('|')]
		point = EquPoint()
		h, m, s = ra.split(' ')
		point.set_ra(h, m, s)
		point.set_dec_deg(dec)
		con = [c for c in self.Cons if c.AbbrLow == abbr][0]
		con.Bounds.append(point)
	

class Constellations_IAU_ex (Constellations):
	'''
	Processor for preprocessed constellation boundaries data from IAU
	http://www.iau.org/public/themes/constellations/
	Preprocessor: constellations.py\make_optimized_iau_data_file()
	'''
	def read(self):	
		self.BoundsDataFile = 'catalogs/constellation_bounds_1.dat'
		Constellations.read(self)
		
	def parse_bound_line(self, line):
		p = [s.strip() for s in line.split('|') if s]
		point = EquPoint()
		point.Index = p[0]
		point.set_ra_hours(p[1])
		point.set_dec_deg(p[2])
		point.Neib = p[4] if (len(p) > 4) else None
		point.Arc = None
		point.ArcR = None
		if len(p) > 5:
			arc = p[5].split('=')
			if arc:
				point.Arc = arc[0] == 'a'
				point.ArcR = float(arc[1]) if len(arc) > 1 else None
		con = [c for c in self.Cons if c.Abbr == p[3]][0]
		con.Bounds.append(point)


class Constellations_1875 (Constellations):
	'''
	Processor for constellation boundaries data in the original 
	B1875.0 system (http://cdsarc.u-strasbg.fr/viz-bin/Cat?VI/49)
	'''
	def read(self):	
		self.BoundsDataFile = 'catalogs/constbnd.dat'
		Constellations.read(self)
		
	def parse_bound_line(self, line):
		parts = [s.strip().lower() for s in line.split(' ') if s]
		ra, dec, abbr = parts[0], parts[1], parts[2]
		point = EquPoint()
		point.set_ra_hours(ra)
		point.set_dec_deg(dec)
		con = [c for c in self.Cons if c.AbbrLow == abbr][0]
		con.Bounds.append(point)


class Constellations_2000 (Constellations_1875):
	'''
	Processor for constellation boundaries data in the  
	J2000.0 system (http://cdsarc.u-strasbg.fr/viz-bin/Cat?VI/49)
	'''
	def read(self):	
		self.BoundsDataFile = 'catalogs/bound_20.dat'
		Constellations.read(self)


if __name__ == '__main__':
	main()

