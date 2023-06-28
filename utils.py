import bpy

def normalize(num, lower=0, upper=360, b=False):
	"""Normalize number to range [lower, upper) or [lower, upper].

	Parameters
	----------
	num : float
		The number to be normalized.
	lower : int
		Lower limit of range. Default is 0.
	upper : int
		Upper limit of range. Default is 360.
	b : bool
		Type of normalization. Default is False. See notes.

		When b=True, the range must be symmetric about 0.
		When b=False, the range must be symmetric about 0 or ``lower`` must
		be equal to 0.

	Returns
	-------
	n : float
		A number in the range [lower, upper) or [lower, upper].

	Raises
	------
	ValueError
	  If lower >= upper.

	Notes
	-----
	If the keyword `b == False`, then the normalization is done in the
	following way. Consider the numbers to be arranged in a circle,
	with the lower and upper ends sitting on top of each other. Moving
	past one limit, takes the number into the beginning of the other
	end. For example, if range is [0 - 360), then 361 becomes 1 and 360
	becomes 0. Negative numbers move from higher to lower numbers. So,
	-1 normalized to [0 - 360) becomes 359.

	When b=False range must be symmetric about 0 or lower=0.

	If the keyword `b == True`, then the given number is considered to
	"bounce" between the two limits. So, -91 normalized to [-90, 90],
	becomes -89, instead of 89. In this case the range is [lower,
	upper]. This code is based on the function `fmt_delta` of `TPM`.

	When b=True range must be symmetric about 0.

	Examples
	--------
	>>> normalize(-270,-180,180)
	90.0
	>>> import math
	>>> math.degrees(normalize(-2*math.pi,-math.pi,math.pi))
	0.0
	>>> normalize(-180, -180, 180)
	-180.0
	>>> normalize(180, -180, 180)
	-180.0
	>>> normalize(180, -180, 180, b=True)
	180.0
	>>> normalize(181,-180,180)
	-179.0
	>>> normalize(181, -180, 180, b=True)
	179.0
	>>> normalize(-180,0,360)
	180.0
	>>> normalize(36,0,24)
	12.0
	>>> normalize(368.5,-180,180)
	8.5
	>>> normalize(-100, -90, 90)
	80.0
	>>> normalize(-100, -90, 90, b=True)
	-80.0
	>>> normalize(100, -90, 90, b=True)
	80.0
	>>> normalize(181, -90, 90, b=True)
	-1.0
	>>> normalize(270, -90, 90, b=True)
	-90.0
	>>> normalize(271, -90, 90, b=True)
	-89.0
	"""
	if lower >= upper:
		ValueError("lower must be lesser than upper")
	if not b:
		if not ((lower + upper == 0) or (lower == 0)):
			raise ValueError('When b=False lower=0 or range must be symmetric about 0.')
	else:
		if not (lower + upper == 0):
			raise ValueError('When b=True range must be symmetric about 0.')

	from math import floor, ceil
	# abs(num + upper) and abs(num - lower) are needed, instead of
	# abs(num), since the lower and upper limits need not be 0. We need
	# to add half size of the range, so that the final result is lower +
	# <value> or upper - <value>, respectively.
	res = num
	if not b:
		res = num
		if num > upper or num == lower:
			num = lower + abs(num + upper) % (abs(lower) + abs(upper))
		if num < lower or num == upper:
			num = upper - abs(num - lower) % (abs(lower) + abs(upper))

		res = lower if num == upper else num
	else:
		total_length = abs(lower) + abs(upper)
		if num < -total_length:
			num += ceil(num / (-2 * total_length)) * 2 * total_length
		if num > total_length:
			num -= floor(num / (2 * total_length)) * 2 * total_length
		if num > upper:
			num = total_length - num
		if num < lower:
			num = -total_length - num

		res = num

	res *= 1.0  # Make all numbers float, to be consistent

	return res

def float_beautify(value):
	round_val = round(value,3)
	
	s = str(round_val)
	s= s.rstrip('0').rstrip('.') if '.' in s else s
	if s == '-0':
		s='0'
	return s
	
def remove_exponent(d):
	return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()

	
def normalize_fraction(d):
	normalized = d.normalize()
	#getcontext().prec = 3
	sign, digit, exponent = normalized.as_tuple()
	to_ret=0
	if (exponent <= 0):
		to_ret = normalized
	else: 
		to_ret = normalized.quantize(1)	
	return to_ret




def blendifyname(bonename) :
	if '_L_' in bonename :
		rem = '_L_'
		ext = '.L'
	elif '_R_' in bonename :
		rem = '_R_'
		ext = '.R'
	else : return bonename
	realname = bonename
	i = realname.index(rem)
	bonename = realname[0:i]+'_'+realname[i+3:] + ext
	return bonename

def villafyname(bonename) :
    mid = ''
    ext =''
    if bonename.endswith(".L") or bonename.endswith(".l"):
        #print("ends with .L")
        ext = '.L'
        mid = '_L'   
    elif bonename.endswith(".R") or bonename.endswith(".r"):
        #print("ends with .R")
        ext = '.R'
        mid = '_R'    
    else:
        return bonename
    #
    i = bonename.index("_joint")
    if ext in ['.L','.R']:
        #print ("Left: "+bonename[0:i])
        #print ("Right: "+bonename[i:-2])
        bonename = bonename[0:i]+mid+bonename[i:-2] 
    return bonename
