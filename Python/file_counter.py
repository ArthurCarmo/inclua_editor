#!/usr/bin/python3
import os

def frame_counter(d): 
	l = next(os.walk(d))[2]
	return len(l)

def ndigits(n):
	ans = 1
	while n // 10 > 0:
		ans += 1	
		n //= 10
	return ans

