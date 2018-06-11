#!/usr/bin/env python3

try:
	import av
except ImportError:
	PyAV = False
else:
	PyAV = True

import numpy as np
import os
import sys
import tkinter as tk
from tkinter import messagebox as tkmb
import time

if 'GI_TYPELIB_PATH' in os.environ:
	os.environ['GI_TYPELIB_PATH'] += ':/usr/local/lib/girepository-1.0:/usr/local/lib64/girepository-1.0'
else:
	os.environ['GI_TYPELIB_PATH'] = '/usr/local/lib/girepository-1.0:/usr/local/lib64/girepository-1.0'

import gi
gi.require_version('Aravis', '0.6')
from gi.repository import Aravis

import cm

#from IPython.terminal.debugger import set_trace

fps_to_dev = { 50: 0, 25: 1, 12: 2, 6: 4, 3: 5 }	# WHY ISN'T 6:3?
dev_to_fps = [ 50, 25, 12, 12, 6, 3 ]
def update_fps(newval):
	dev.set_integer_feature_value('IRFrameRate', fps_to_dev[newval])

format_to_dev = { 'Radiometric': 0, 'Linear 100mK': 1, 'Linear 10mK': 2 }
dev_to_format = [ 'Radiometric', 'Linear 100mK', 'Linear 10mK' ]
def update_format(newval):
	dev.set_integer_feature_value('IRFormat', format_to_dev[newval])

def update_focus(newval):
	dev.set_integer_feature_value('FocusPos', int(newval))

#def update_tlower(newval):
#	print('setting lower to ' + newval)
#	dev.set_integer_feature_value('ScaleLimitLow', int(newval))
#
#def update_tupper(newval):
#	print('setting upper to ' + newval)
#	dev.set_integer_feature_value('ScaleLimitUpper', int(newval))

outflir = None
frames = 0
def toggle_record_flir():
	global outflir
	global frames

	if outflir:
		print('Stop recording')
		outflir.seek(0, os.SEEK_SET)
		outflir.write(frames.to_bytes(4, 'little'))
		outflir.close()
		outflir = None
		recf.config(image = recim)
		recm.config(state = tk.NORMAL)
	else:
		recm.config(state = tk.DISABLED)
		filename = prefix.get() + time.strftime('%Y%m%d_%H:%M:%S%z.flir')
		print('Recording to {}'.format(filename))
		recf.config(image = stopim)
		outflir = open(filename, 'wb')
		frames = 0
		outflir.write(frames.to_bytes(4, 'little'))
		outflir.write(h.to_bytes(4, 'little'))
		outflir.write(w.to_bytes(4, 'little'))

outmp4 = None
def toggle_record_mp4():
	if not PyAV:
		tkmb.showerror('No PyAV', 'PyAV must be installed for MP4 output to work')
		return

	global outmp4
	global frames

	if outmp4:
		print('Stop recording')
		while True:
			packet = outmp4.streams[0].encode()
			if not packet:
				break
			outmp4.mux(packet)
		outmp4.close()
		outmp4 = None
		recm.config(image = recim)
		recf.config(state = tk.NORMAL)
	else:
		recf.config(state = tk.DISABLED)
		filename = prefix.get() + time.strftime('%Y%m%d_%H:%M:%S%z.mp4')
		print('Recording to {}'.format(filename))
		recm.config(image = stopim)
		outmp4 = av.open(filename, 'w')
		fps = dev_to_fps[dev.get_integer_feature_value('IRFrameRate')]
		stream = outmp4.add_stream('mpeg4', str(fps))
		stream.bit_rate = 10000000
		stream.pix_fmt = 'yuv420p'
		stream.width = w
		stream.height = h
		stream.thread_count = 3
		frames = 0

def do_af():
	dev.set_integer_feature_value('FocusSpeed', 1)
	dev.execute_command('AutoFocus')

try:
	if len(sys.argv) > 1:	# IP address or hostname
		camera = Aravis.Camera.new(sys.argv[1])
	else:	# take first one found
		camera = Aravis.Camera.new(None)
except:
	print('No camera found')
	sys.exit()

dev = camera.get_device()

print('Found an {} {} at {}'.format(camera.get_vendor_name(), camera.get_model_name(), dev.get_interface_address().to_string()))

[x, y, w, h] = camera.get_region()
bpp = camera.get_pixel_format() >> 16 & 0xff
payload = camera.get_payload()
print('Region of Interest is ({}, {}) to ({}, {}), bpp is {}, frame size is {} bytes'.format(x, y, x + w, x + h, bpp, payload))

if bpp != 16:
	print('Support for modes other than Mono16 not implemented, sorry')
	sys.exit()

gui = tk.Tk()
gui.title('FLIR recorder')
ppm_header = 'P6 {} {} 255 '.format(w, h).encode('ascii')

vid_label = tk.Label(gui)
vid_label.grid(columnspan = 4)

tk.Label(gui, text='Frames per second\n(recording, not display)').grid(row = 1)
fps_var = tk.IntVar(gui)
fps_var.set(dev_to_fps[dev.get_integer_feature_value('IRFrameRate')])
fps = tk.OptionMenu(gui, fps_var, 50, 25, 12, 6, 3, command = update_fps)
fps.grid(row = 1, column = 1, sticky = tk.W)

tk.Label(gui, text='Image format').grid(row = 1, column = 2)
format_var = tk.StringVar(gui)
format_var.set(dev_to_format[dev.get_integer_feature_value('IRFormat')])
format = tk.OptionMenu(gui, format_var, 'Radiometric', 'Linear 100mK', 'Linear 10mK', command = update_format)
format.grid(row = 1, column = 3, sticky = tk.W)

tk.Label(gui, text='Focus').grid()
focus = tk.Scale(gui, from_ = dev.get_integer_feature_bounds('FocusPos')[0], to = dev.get_integer_feature_bounds('FocusPos')[1], orient = tk.HORIZONTAL, length = .6 * w, command = update_focus, resolution = 100)
focus.set(dev.get_integer_feature_value('FocusPos'))
focus.grid(row = 2, column = 1, columnspan = 2, sticky = tk.W)

tk.Button(gui, text = "Auto focus", command = do_af).grid(row = 2, column = 3)

tk.Label(gui, text='Output file prefix').grid()
prefix = tk.Entry(gui, background = 'white')
prefix.grid(row = 3, column = 1, sticky = tk.W + tk.E, pady = 5)

recim = tk.PhotoImage(data = "R0lGODlhGQAZAIABAP8AAP///yH5BAEKAAEALAAAAAAZABkAAAI4jI+py+0JYnxKWkvD3dPx33ziIpZVCUIop67s4aZG/M70hdx4rgOn/ruRhAzaw5VBZXiSpfPpLAAAOw==")	# base64'd GIF
stopim = tk.PhotoImage(data = "R0lGODlhGQAZAIABAAAAAP///yH5BAEKAAEALAAAAAAZABkAAAI0jI+py+0PgZy0UmWzxboD7mVgWI3kZJ5fopZsi77wisxSeuKkHvKe3wFqhCIZDIJMKpeMAgA7")
recf = tk.Button(gui, image = recim, command = toggle_record_flir, compound = tk.LEFT, text = '.flir')
recf.grid(row = 3, column = 2, sticky = tk.E)
recm = tk.Button(gui, image = recim, command = toggle_record_mp4, compound = tk.LEFT, text = '.mp4')
recm.grid(row = 3, column = 3, sticky = tk.E)

#dev.set_integer_feature_value('IRFormat', 0)
#
#tlower = tk.Scale(gui, from_ = 0, to = 5000, orient = tk.HORIZONTAL, label = 'Lower scale limit', length = w - 100, command = update_tlower)
#tlower.pack()

#tupper = tk.Scale(gui, from_ = 0, to = 5000, orient = tk.HORIZONTAL, label = 'Upper scale limit', length = w - 100, command = update_tupper)
#tupper.pack()

stream = camera.create_stream (None, None)

for i in range(0, 50):
	stream.push_buffer(Aravis.Buffer.new_allocate(payload))

camera.start_acquisition()

done = False
def finish():
	global done
	if outflir:
		toggle_record_flir()
	if outmp4:
		toggle_record_mp4()
	camera.stop_acquisition()
	done = True
	gui.destroy()

gui.protocol("WM_DELETE_WINDOW", finish)

if PyAV:
	mp4frame = av.VideoFrame(w, h, 'yuv420p')

last_frame = 0
last_render = time.time()
while not done:
	buf = stream.pop_buffer()

	if not buf:
		continue

	if buf.get_status() == Aravis.BufferStatus.TIMEOUT:
		print('Packet timeout!')
	else:
		if buf.get_frame_id() != last_frame + 1 and buf.get_frame_id() != 1 and last_frame != 65535:
			print('Dropped {} frame(s)!'.format(buf.get_frame_id() - last_frame - 1))
		last_frame = buf.get_frame_id()

		if buf.get_status() != Aravis.BufferStatus.SUCCESS:
			print(buf.get_status())
#			set_trace()

		I = np.ndarray(buffer = buf.get_data(), dtype = np.uint16, shape = (h, w)) # 16 bpp
		focus.set(dev.get_integer_feature_value('FocusPos'))

		if outflir:
			outflir.write(I.tobytes())
			frames += 1
		if outmp4:
			Y, U, V = cm.to_iron_ycbcr(I)
			mp4frame.planes[0].update(Y)
			mp4frame.planes[1].update(U)
			mp4frame.planes[2].update(V)
			packet = outmp4.streams[0].encode(mp4frame)
			if packet:
				outmp4.mux(packet)
			frames += 1

		if time.time() - last_render > .19:	# update display at 5Hz
			PI = tk.PhotoImage(data = ppm_header + cm.to_iron_rgb(I).flatten().tobytes(), width = w, height = h, format = 'PPM')
			vid_label.config(image = PI)
			vid_label._cache = PI	# fool GC
			last_render = time.time()

	stream.push_buffer(buf)

	gui.update_idletasks()
	gui.update()

# vim: ts=8 sts=8 sw=8 noexpandtab
