#! /usr/bin/python2
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
			# log.debug(osc)
			log.debug("**********" + str(len(osc.create_nodes)) + "**********", osc.create_nodes)
			log.debug("**********" + str(len(osc.modify_nodes)) + "**********", osc.modify_nodes)
			log.debug("**********" + str(len(osc.delete_nodes)) + "**********", osc.delete_nodes)
			log.debug("**********" + str(len(osc.create_ways)) + "**********", osc.create_ways)
			log.debug("**********" + str(len(osc.modify_ways)) + "**********", osc.modify_ways)
			log.debug("**********" + str(len(osc.delete_ways)) + "**********", osc.delete_ways)
		else:
			log.warn("Unrecognised file extension (.osm or .osc): %s", filename)