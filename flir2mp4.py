#!/usr/bin/env python3

import av
import numpy as np
import sys

from cm import to_iron_ycbcr

with open(sys.argv[1], 'rb') as f:
	frames = int.from_bytes(f.read(4), 'little')
	height = int.from_bytes(f.read(4), 'little')
	width = int.from_bytes(f.read(4), 'little')

	outvid = av.open(sys.argv[1] + '.mp4', 'w')
	if len(sys.argv) > 2:
		stream = outvid.add_stream('mpeg4', sys.argv[2])
	else:
		stream = outvid.add_stream('mpeg4', '50')
	stream.bit_rate = 10000000
	stream.pix_fmt = 'yuv420p'
	stream.width = width
	stream.height = height
	stream.thread_count = 3

	outframe = av.VideoFrame(width, height, 'yuv420p')

	for frameno in range(frames):
		I = np.ndarray(buffer = f.read(width * height * 2), dtype = np.uint16, shape = (height, width))	# 16 bpp
		Y, U, V = to_iron_ycbcr(I)
		outframe.planes[0].update(Y)
		outframe.planes[1].update(U)
		outframe.planes[2].update(V)
		packet = outvid.streams[0].encode(outframe)
		if packet:
			outvid.mux(packet)

	while True:
		packet = stream.encode()
		if not packet:
			break
		outvid.mux(packet)
	outvid.close()

# vim: ts=8 sts=8 sw=8 noexpandtab
