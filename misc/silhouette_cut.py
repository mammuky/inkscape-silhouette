#! /usr/bin/python
#
# simple demo program to cut with the silhouette cameo.
# (C) 2015 juewei@fabfolk.com
#
# Requires: python-usb  # from Factory

import re,time,sys,string,argparse

sys.path.extend(['..','.'])	# make it callable from top or misc directory.
from silhouette.Graphtec import SilhouetteCameo

dev = SilhouetteCameo()

ArgParser = argparse.ArgumentParser(description='Cut a dumpfile from sendto_silhouette without using inkscape.')
ArgParser.add_argument('-P', '--pen', action='store_true', help="switch to pen mode. Default: knive mode")
ArgParser.add_argument('-b', '--bbox', action='store_true', help="Bounding box only. Default: entire design")
ArgParser.add_argument('-x', '--xoff', type=float, default=0.0, help="Horizontal offset [mm]. Positive values point rightward")
ArgParser.add_argument('-y', '--yoff', type=float, default=0.0, help="Vertical offset [mm]. Positive values point downward")
ArgParser.add_argument('-S', '--scale',type=float, default=1.0, help="Scale the design.")
ArgParser.add_argument('-p', '--pressure', type=int, default=3, help="Pressure value [1..18]")
ArgParser.add_argument('-s', '--speed', type=int, default=10, help="Speed value [1..10]")
ArgParser.add_argument('-a', '--advance-origin', action='store_true', help="Set the origin below the design. Default: return home.")
ArgParser.add_argument('dumpfile')
args = ArgParser.parse_args()

dev.setup(speed=args.speed, pressure=args.pressure, pen=args.pen, return_home=(not args.advance_origin))

# print args

dumpdata=None
for line in open(args.dumpfile,'r').readlines():
  if re.match(r'\s*\[', line):
    exec('dumpdata='+line)
    break 
  elif re.match(r'\s*<\s*svg', line):
    print line
    print("Error: xml/svg file. Please load into inkscape. Use extensions -> export -> sendto silhouette, [x] dump to file")
    sys.exit(0)
  else:
    print line,
# print dumpdata

dev.wait_for_ready()
bbox = dev.plot(pathlist=dumpdata, offset=(args.xoff,args.yoff), bboxonly=args.bbox)
dev.wait_for_ready()