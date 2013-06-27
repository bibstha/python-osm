#! /usr/bin/python2
import os
import sys
import unittest

srcDir = os.path.abspath('../src')
sys.path.insert(1, srcDir)

import pyosm

class OSCXMLFileTests(unittest.TestCase):
	def setUp(self):
		self.create_file = open('create.osc')

	def tearDown(self):
		self.create_file.close()

	def testCreate(self):
		osc_create_file = pyosm.OSCXMLFile(self.create_file)
		
		self.assertEqual(6, len(osc_create_file.create_nodes))
		
		expectedNodeIds = [1994284785, 1994284786, 1994284787, 1994284788, 1994284789, 1994284790]
		self.assertEqual(expectedNodeIds, list(osc_create_file.create_nodes))

		expectedWayIds = {
			188810323: [1994284790, 1994284789],
			188810324: [1994284787, 1994284788, 1994284786, 1994284785, 1022704061, 1994284787]
		}
		self.assertEqual(list(expectedWayIds), list(osc_create_file.create_ways))
		self.assertEqual(2, len(osc_create_file.create_ways[188810323].nodes))
		self.assertEqual(6, len(osc_create_file.create_ways[188810324].nodes))

		for k in osc_create_file.create_nodes:
			if k == 1994284789:
				self.assertTrue('event' in osc_create_file.create_nodes[k].tags)
				self.assertEqual('yes', osc_create_file.create_nodes[k].tags['event'])
			else:
				self.assertTrue('event' not in osc_create_file.create_nodes[k].tags)

		for k in osc_create_file.create_ways:
			if k == 188810324:
				self.assertTrue('event' in osc_create_file.create_ways[k].tags)
				self.assertEqual('yes', osc_create_file.create_ways[k].tags['event'])
			else:
				self.assertFalse('event' in osc_create_file.create_ways[k].tags)

	def testModify(self):
		try:
			modify_file = open("mixed.osc")
			osc_modify_file = pyosm.OSCXMLFile(modify_file)

			self.assertEqual(1, len(osc_modify_file.modify_nodes))
			self.assertEqual(1, len(osc_modify_file.modify_ways))

			self.assertTrue(541495057 in osc_modify_file.modify_nodes)
			self.assertTrue("event" in osc_modify_file.modify_nodes[541495057].tags)
			self.assertEqual("yes", osc_modify_file.modify_nodes[541495057].tags["event"])

			self.assertTrue(43204992 in osc_modify_file.modify_ways)
			self.assertTrue("event" in osc_modify_file.modify_ways[43204992].tags)
			self.assertEqual("yes", osc_modify_file.modify_ways[43204992].tags["event"])
			self.assertEqual(5, len(osc_modify_file.modify_ways[43204992].nodes))

		finally:
			modify_file.close()

	def testDelete(self):
		try:
			del_file = open("mixed.osc")
			osc_del_file = pyosm.OSCXMLFile(del_file)

			self.assertEqual(10, len(osc_del_file.delete_nodes))
			self.assertEqual(1, len(osc_del_file.delete_ways))

		finally:
			del_file.close()

def main():
	unittest.main()

if __name__ == '__main__':
	main()