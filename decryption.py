from PIL import Image
from random import randint
import numpy
import sys
from helper import *

# Load the image
im = Image.open('encrypted_images/' + sys.argv[1])
pix = im.load()

#Obtaining the RGB matrices
r = []
g = []
b = []
for i in range(im.size[0]):
	r.append([])
	g.append([])
	b.append([]) 
	for j in range(im.size[1]):
		rgbPerPixel = pix[i,j]
		r[i].append(rgbPerPixel[0])
		g[i].append(rgbPerPixel[1])
		b[i].append(rgbPerPixel[2])

# Size of image
m = im.size[0]
n = im.size[1]

Kr = []
Kc = []

# Enter the key values from keys.txt
print('Enter value of Kr')

for i in range(m):
	Kr.append(int(input()))

print('Enter value of Kc')
for i in range(n):
	Kc.append(int(input()))

print('Enter value of ITER_MAX')
ITER_MAX = int(input())


for iterations in range(ITER_MAX):
	# For each column do bitwise XOR operator with Kr
	for j in range(n):
		for i in range(m):
			if(j%2==0):
				r[i][j] = r[i][j] ^ Kr[i]
				g[i][j] = g[i][j] ^ Kr[i]
				b[i][j] = b[i][j] ^ Kr[i]
			else:
				r[i][j] = r[i][j] ^ rotate180(Kr[i])
				g[i][j] = g[i][j] ^ rotate180(Kr[i])
				b[i][j] = b[i][j] ^ rotate180(Kr[i])
	# For each row do bitwise XOR operator with Kc
	for i in range(m):
		for j in range(n):
			if(i%2==1):
				r[i][j] = r[i][j] ^ Kc[j]
				g[i][j] = g[i][j] ^ Kc[j]
				b[i][j] = b[i][j] ^ Kc[j]
			else:
				r[i][j] = r[i][j] ^ rotate180(Kc[j])
				g[i][j] = g[i][j] ^ rotate180(Kc[j])
				b[i][j] = b[i][j] ^ rotate180(Kc[j])
	# For each column
    # 1. Compute sum of all elements
    # 2. Compute modulo 2
    # 3. if modulo is 0 -> up circular shift by Kc bits
    #       modulo is 1 -> down circular shift by Kc bits 
	for i in range(n):
		rTotalSum = 0
		gTotalSum = 0
		bTotalSum = 0
		for j in range(m):
			rTotalSum += r[j][i]
			gTotalSum += g[j][i]
			bTotalSum += b[j][i]
		rModulus = rTotalSum % 2
		gModulus = gTotalSum % 2
		bModulus = bTotalSum % 2
		if(rModulus==0):
			downshift(r,i,Kc[i])
		else:
			upshift(r,i,Kc[i])
		if(gModulus==0):
			downshift(g,i,Kc[i])
		else:
			upshift(g,i,Kc[i])
		if(bModulus==0):
			downshift(b,i,Kc[i])
		else:
			upshift(b,i,Kc[i])

	# For each row
    # 1. Compute sum of all elements
    # 2. Compute modulo 2
    # 3. if modulo is 0 -> right circular shift by Kr bits
    #       modulo is 1 -> left circular shift by Kr bits  
	for i in range(m):
		rTotalSum = sum(r[i])
		gTotalSum = sum(g[i])
		bTotalSum = sum(b[i])
		rModulus = rTotalSum % 2
		gModulus = gTotalSum % 2
		bModulus = bTotalSum % 2
		if(rModulus==0):
			r[i] = numpy.roll(r[i],-Kr[i])
		else:
			r[i] = numpy.roll(r[i],Kr[i])
		if(gModulus==0):
			g[i] = numpy.roll(g[i],-Kr[i])
		else:
			g[i] = numpy.roll(g[i],Kr[i])
		if(bModulus==0):
			b[i] = numpy.roll(b[i],-Kr[i])
		else:
			b[i] = numpy.roll(b[i],Kr[i])

# Combine R,G,B values to form image
for i in range(m):
	for j in range(n):
		pix[i,j] = (r[i][j],g[i][j],b[i][j])

# Save the image
im.save('decrypted_images/' + sys.argv[1])