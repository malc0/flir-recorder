#!/usr/bin/python3

#import matplotlib
#matplotlib.use('tkagg')
import numpy as np
import os
import sys
import tkinter as tk
#import matplotlib.pyplot as plt
#plt.ion()
import time

if 'GI_TYPELIB_PATH' in os.environ:
	os.environ['GI_TYPELIB_PATH'] += ':/usr/local/lib/girepository-1.0:/usr/local/lib64/girepository-1.0'
else:
	os.environ['GI_TYPELIB_PATH'] = '/usr/local/lib/girepository-1.0:/usr/local/lib64/girepository-1.0'

import gi
gi.require_version('Aravis', '0.6')
from gi.repository import Aravis

#from IPython.terminal.debugger import set_trace

ironycbcr = np.array(((16, 128, 128),
		 (20, 144, 125),
		 (21, 150, 124),
		 (22, 157, 123),
		 (24, 164, 122),
		 (25, 167, 122),
		 (27, 171, 123),
		 (28, 174, 124),
		 (30, 177, 125),
		 (31, 178, 126),
		 (33, 179, 128),
		 (35, 180, 131),
		 (37, 182, 133),
		 (40, 182, 136),
		 (42, 182, 139),
		 (44, 183, 142),
		 (46, 183, 144),
		 (48, 184, 146),
		 (49, 183, 149),
		 (51, 183, 151),
		 (52, 182, 154),
		 (54, 182, 157),
		 (56, 182, 160),
		 (58, 181, 163),
		 (60, 180, 165),
		 (61, 180, 167),
		 (63, 179, 170),
		 (64, 178, 173),
		 (66, 177, 176),
		 (67, 176, 178),
		 (69, 175, 181),
		 (70, 174, 184),
		 (71, 173, 186),
		 (73, 172, 188),
		 (74, 171, 190),
		 (75, 170, 192),
		 (76, 169, 194),
		 (77, 168, 195),
		 (78, 166, 197),
		 (80, 165, 197),
		 (81, 163, 198),
		 (82, 162, 199),
		 (84, 160, 200),
		 (86, 158, 199),
		 (87, 156, 200),
		 (89, 153, 200),
		 (91, 150, 200),
		 (93, 147, 201),
		 (94, 143, 201),
		 (96, 139, 201),
		 (98, 136, 201),
		 (100, 131, 201),
		 (102, 127, 201),
		 (104, 121, 201),
		 (105, 115, 201),
		 (106, 109, 202),
		 (107, 102, 202),
		 (108, 95, 202),
		 (110, 89, 202),
		 (112, 85, 202),
		 (114, 82, 202),
		 (115, 79, 201),
		 (117, 76, 201),
		 (119, 74, 200),
		 (121, 72, 199),
		 (123, 70, 198),
		 (124, 68, 198),
		 (126, 66, 197),
		 (128, 65, 196),
		 (130, 64, 196),
		 (132, 62, 195),
		 (133, 61, 194),
		 (135, 60, 193),
		 (137, 58, 193),
		 (139, 57, 191),
		 (142, 55, 190),
		 (144, 54, 189),
		 (146, 53, 188),
		 (148, 52, 187),
		 (150, 51, 186),
		 (152, 50, 185),
		 (153, 49, 184),
		 (155, 48, 183),
		 (158, 46, 182),
		 (161, 44, 180),
		 (163, 43, 179),
		 (166, 42, 177),
		 (168, 40, 176),
		 (170, 39, 175),
		 (171, 38, 174),
		 (174, 37, 172),
		 (175, 36, 171),
		 (178, 35, 169),
		 (180, 34, 168),
		 (182, 32, 166),
		 (183, 32, 165),
		 (185, 32, 164),
		 (187, 32, 163),
		 (189, 33, 161),
		 (191, 33, 159),
		 (193, 33, 158),
		 (195, 36, 157),
		 (198, 39, 155),
		 (200, 41, 154),
		 (202, 46, 152),
		 (205, 50, 150),
		 (207, 55, 148),
		 (210, 60, 146),
		 (212, 65, 145),
		 (214, 71, 143),
		 (217, 79, 141),
		 (219, 85, 140),
		 (221, 91, 138),
		 (224, 97, 136),
		 (225, 102, 135),
		 (227, 107, 134),
		 (229, 112, 132),
		 (231, 117, 131),
		 (233, 121, 130),
		 (234, 125, 128)), np.uint8)

iron = np.array(((0, 0, 0),
		 (0, 0, 36),
		 (0, 0, 51),
		 (0, 0, 66),
		 (0, 0, 81),
		 (2, 0, 90),
		 (4, 0, 99),
		 (7, 0, 106),
		 (11, 0, 115),
		 (14, 0, 119),
		 (20, 0, 123),
		 (27, 0, 128),
		 (33, 0, 133),
		 (41, 0, 137),
		 (48, 0, 140),
		 (55, 0, 143),
		 (61, 0, 146),
		 (66, 0, 149),
		 (72, 0, 150),
		 (78, 0, 151),
		 (84, 0, 152),
		 (91, 0, 153),
		 (97, 0, 155),
		 (104, 0, 155),
		 (110, 0, 156),
		 (115, 0, 157),
		 (122, 0, 157),
		 (128, 0, 157),
		 (134, 0, 157),
		 (139, 0, 157),
		 (146, 0, 156),
		 (152, 0, 155),
		 (157, 0, 155),
		 (162, 0, 155),
		 (167, 0, 154),
		 (171, 0, 153),
		 (175, 1, 152),
		 (178, 1, 151),
		 (182, 2, 149),
		 (185, 4, 149),
		 (188, 5, 147),
		 (191, 6, 146),
		 (193, 8, 144),
		 (195, 11, 142),
		 (198, 13, 139),
		 (201, 17, 135),
		 (203, 20, 132),
		 (206, 23, 127),
		 (208, 26, 121),
		 (210, 29, 116),
		 (212, 33, 111),
		 (214, 37, 103),
		 (217, 41, 97),
		 (219, 46, 89),
		 (221, 49, 78),
		 (223, 53, 66),
		 (224, 56, 54),
		 (226, 60, 42),
		 (228, 64, 30),
		 (229, 68, 25),
		 (231, 72, 20),
		 (232, 76, 16),
		 (234, 78, 12),
		 (235, 82, 10),
		 (236, 86, 8),
		 (237, 90, 7),
		 (238, 93, 5),
		 (239, 96, 4),
		 (240, 100, 3),
		 (241, 103, 3),
		 (241, 106, 2),
		 (242, 109, 1),
		 (243, 113, 1),
		 (244, 116, 0),
		 (244, 120, 0),
		 (245, 125, 0),
		 (246, 129, 0),
		 (247, 133, 0),
		 (248, 136, 0),
		 (248, 139, 0),
		 (249, 142, 0),
		 (249, 145, 0),
		 (250, 149, 0),
		 (251, 154, 0),
		 (252, 159, 0),
		 (253, 163, 0),
		 (253, 168, 0),
		 (253, 172, 0),
		 (254, 176, 0),
		 (254, 179, 0),
		 (254, 184, 0),
		 (254, 187, 0),
		 (254, 191, 0),
		 (254, 195, 0),
		 (254, 199, 0),
		 (254, 202, 1),
		 (254, 205, 2),
		 (254, 208, 5),
		 (254, 212, 9),
		 (254, 216, 12),
		 (255, 219, 15),
		 (255, 221, 23),
		 (255, 224, 32),
		 (255, 227, 39),
		 (255, 229, 50),
		 (255, 232, 63),
		 (255, 235, 75),
		 (255, 238, 88),
		 (255, 239, 102),
		 (255, 241, 116),
		 (255, 242, 134),
		 (255, 244, 149),
		 (255, 245, 164),
		 (255, 247, 179),
		 (255, 248, 192),
		 (255, 249, 203),
		 (255, 251, 216),
		 (255, 253, 228),
		 (255, 254, 239),
		 (255, 255, 249)), np.uint8)

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

outvid = None
frames = 0
def toggle_record():
	global outvid
	global frames

	if outvid:
		print('Stop recording')
		outvid.seek(0, os.SEEK_SET)
		outvid.write(frames.to_bytes(4, 'little'))
		outvid.close()
		outvid = None
		rec.config(image = recim)
	else:
		filename = prefix.get() + time.strftime('%Y%m%d_%H:%M:%S%z.flir')
		print('Recording to {}'.format(filename))
		rec.config(image = stopim)
		outvid = open(filename, 'wb')
		frames = 0
		outvid.write(frames.to_bytes(4, 'little'))
		outvid.write(h.to_bytes(4, 'little'))
		outvid.write(w.to_bytes(4, 'little'))

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
focus = tk.Scale(gui, from_ = dev.get_integer_feature_bounds('FocusPos')[0], to = dev.get_integer_feature_bounds('FocusPos')[1], orient = tk.HORIZONTAL, length = .7 * w, command = update_focus, resolution = 100)
focus.set(dev.get_integer_feature_value('FocusPos'))
focus.grid(row = 2, column = 1, columnspan = 3, sticky = tk.W)

tk.Label(gui, text='Output file prefix').grid()
prefix = tk.Entry(gui, background = 'white')
prefix.grid(row = 3, column = 1, sticky = tk.W + tk.E, pady = 5)

recim = tk.PhotoImage(data = "R0lGODlhSwAZAPAAAP8AAAAAACH5BAEAAAEALAAAAABLABkAAAJTjI+py+0Po5y0WglyvrwvDYLeaIXmRqbPyaquwsbvHNezW8t3mrf72NP9OEHf8FI8HYnJ0BLZFD1LUcAUGr1Ss9oKt+stgpm5cadsBkrT7LY7UAAAOw==")	# base64'd GIF
stopim = tk.PhotoImage(data = "R0lGODlhSwAZAPAAAAAAAAAAACH5BAEAAAEALAAAAABLABkAAAJQjI+py+0Po5y02ouzBrz772niA5bgiC7myqXuwa7vG5uzW5d3mp/72Pv8gMHOUFQ0HjPJ1hLTBDyhzeklarVgs5QtV+L9QsJiB7mMTqvXogIAOw==")
rec = tk.Button(gui, image = recim, command = toggle_record)
rec.grid(row = 3, column = 2, sticky = tk.E)

tk.Button(gui, text = "Auto focus", command = do_af).grid(row = 3, column = 3)

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

def to_iron(I):	# my god this is slow.  FIXME
	cmin, cmax = np.percentile(I, (1, 99))
	I = (I - cmin) * iron.shape[0] / (cmax - cmin)
	I[I < 0] = 0
	I[I > iron.shape[0] - 1] = iron.shape[0] - 1
	I = I.astype(np.uint8)

	return iron[I]

done = False
def finish():
	global done
	if outvid:
		toggle_record()
	camera.stop_acquisition()
	done = True
	gui.destroy()

gui.protocol("WM_DELETE_WINDOW", finish)

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

		if outvid:
			outvid.write(I.tobytes())
			frames += 1

		if time.time() - last_render > .19:	# update display at 5Hz
			PI = tk.PhotoImage(data = ppm_header + to_iron(I).flatten().tobytes(), width = w, height = h, format = 'PPM')
			vid_label.config(image = PI)
			vid_label._cache = PI	# fool GC
			last_render = time.time()

	stream.push_buffer(buf)

	gui.update_idletasks()
	gui.update()

# vim: ts=8 sts=8 sw=8 noexpandtab
