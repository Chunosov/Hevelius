#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from hevelius import Bsc
import constellations

def main():
	#stars = Bsc.read()

	#bsc_extract_star_names()
	bsc_extract_star_labels()
	
	#write_labels(stars)
	#write_names(stars)
	
	#Stat.count(stars)

GREEK = { \
	'alp': '', # alpha
	'bet': '', # beta
	'gam': '', # gamma
	'del': '', # delta
	'eps': '', # epsilon
	'zet': '', # zeta
	'eta': '', # eta
	'the': '', # theta
	'iot': '', # iota
	'kap': '', # kappa
	'lam': '', # lambda
	'mu':  '', # mu
	'nu':  '', # nu
	'xi':  '', # xi
	'omi': '', # omicron
	'pi':  '', # pi
	'pho': '', # rho
	'sig': '', # sigma
	'tau': '', # tau
	'ups': '', # upsilon
	'phi': '', # phi
	'chi': '', # chi
	'psi': '', # psi
	'ome': ''  # omega
	}

def bsc_extract_star_names():
	names = {}
	with open('catalogs/bsc5.notes') as data:
		for line in data:
			if line.strip():
				try:
					hr = int(line[1:5]) # Harvard Revised (HR) 
					cat = line[7:11].strip() # Remark category abbreviation: 
					if cat == 'N:': # Star names
						name = line[12:].strip()
						if name:
							if hr in names:
								names[hr] = names[hr] + '; ' + name
							else: 
								names[hr] = name
				except Exception as ex:
					print('Error reading star note:\n%s%s\n' % (line, ex))
	bsc_write_star_data(names, 'catalogs/~bsc5_names.dat')


def bsc_extract_star_labels():
	labels = {}
	with open('catalogs/bsc5.dat') as data:
		for line in data:
			if line.strip():
				hr = int(line[0:4]) # Harvard Revised Number = Bright Star Number 
				try:
					raw = line[4:14].strip() # Name, generally Bayer and/or Flamsteed name 
					if raw:
						label = bsc_process_label(hr, raw)
						if label:
							labels[hr] = label
				except Exception as ex:
					print('Error reading star %d: %s\n' % (hr, ex))
	bsc_write_star_data(labels, 'catalogs/~bsc5_labels.dat')


def bsc_process_label(hr, label):
	if len(label) <= 3:
		print('Too short label: ' + label)
		return None
	abbr = label[-3:].lower()
	if not abbr:
		print('Constellations not set for %d: %s' % (hr, label))
		return None
	if abbr not in constellations.ABBRS:
		print('Constellations not found for %d: %s' % (hr, label))
		return None
	num1 = ''
	num2 = ''
	let = ''
	num_let = label[0:-3].strip()
	if num_let:
		#r = re.compile()
		parts = re.match(r'\d*\S*\d*', num_let)
		print(num_let, ':     ', parts.group(0), parts.group(1), parts.group(2))
		
	return '|{0}'.format(abbr)
		

def bsc_write_star_data(data, file_name):
	lines = ['{0:>4} {1}\n'.format(hr, info) for hr, info in \
		[(hr, data[hr]) for hr in sorted(data.keys())]]
	with open(file_name, 'w') as f: f.writelines(lines)
	print('File written: %s\nLines: %d\nOK' % (file_name, len(lines)))

	
class Stat:	
	def count(stars):
		min_dec = -30
		print('Min declination: %d\n' % min_dec)
		Stat.count_till(stars, -1, min_dec)
		Stat.count_till(stars, 0, min_dec)
		Stat.count_till(stars, 1, min_dec)
		Stat.count_till(stars, 2, min_dec)
		Stat.count_till(stars, 3, min_dec)
		Stat.count_till(stars, 4, min_dec)
		Stat.count_till(stars, 5, min_dec)
		Stat.count_till(stars, 6, min_dec)
		Stat.count_till(stars, 7, min_dec)
		Stat.count_till(stars, 8, min_dec)
		print()
		Stat.count_between(stars, -2, -1, min_dec)
		Stat.count_between(stars, -1, 0, min_dec)
		Stat.count_between(stars, 0, 1, min_dec)
		Stat.count_between(stars, 1, 2, min_dec)
		Stat.count_between(stars, 2, 3, min_dec)
		Stat.count_between(stars, 3, 4, min_dec)
		Stat.count_between(stars, 5, 6, min_dec)
		Stat.count_between(stars, 6, 7, min_dec)
		Stat.count_between(stars, 7, 8, min_dec)
		print()
		Stat.count_between(stars, -1.5, -0.5, min_dec)
		Stat.count_between(stars, -0.5, 0.5, min_dec)
		Stat.count_between(stars, 0.5, 1.5, min_dec)
		Stat.count_between(stars, 1.5, 2.5, min_dec)
		Stat.count_between(stars, 2.5, 3.5, min_dec)
		Stat.count_between(stars, 3.5, 4.5, min_dec)
		Stat.count_between(stars, 4.5, 5.5, min_dec)
		Stat.count_between(stars, 5.5, 6.5, min_dec)
		Stat.count_between(stars, 6.5, 7.5, min_dec)
		Stat.count_between(stars, 7.5, 8.5, min_dec)
		
	def count_between(stars, max, min, dec = -90):
		c = len([s for s in stars if s.Mag > max and s.Mag <= min and s.DecD >= dec])
		print('{0:0=+4.1f}m - {1:0=+4.1f}m: {2: >4}'.format(max, min, c))
		
	def count_till(stars, min, dec = -90):
		c = len([s for s in stars if s.Mag <= min and s.DecD >= dec])
		print('{0:0=+4.1f}m: {1: >4}'.format(min, c))


if __name__ == '__main__':
	main()

