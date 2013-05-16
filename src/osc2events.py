#! env python
from pyosm import *
from optparse import OptionParser
import logging
log = logging.getLogger("pyosm")

if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s - %(message)s")
	import sys

	parser = OptionParser()
	parser.add_option("-f", "--file", dest="filename",
		help="write report to FILE", metavar="FILE")
	parser.add_option("-q", "--quiet",
		action="store_false", dest="verbose", default=True,
		help="don't print status messages to stdout")

	for filename in sys.argv[1:]:
		ext = filename[-3:]
		if ext == 'osc':
			osc = OSCXMLFile(filename)
			log.debug(dir(osc))
		else:
			log.warn("Unrecognised file extension (.osm or .osc): %s", filename)