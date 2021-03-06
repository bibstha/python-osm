#! env python
#
# Original version by Rory McCann (http://blog.technomancy.org/)
# Modifications by Christoph Lupprich (http://www.stopbeingcarbon.com)
#
import xml.sax
import logging
log = logging.getLogger("pyosm")

class Node(object):
    ATTRIBUTES = ['id', 'timestamp', 'uid', 'user', 'visible', 'version', 'lat', 'lon', 'changeset']
    def __init__(self, attr, tags=None):
        self.id = int(attr['id'])
        self.lon, self.lat = attr['lon'], attr['lat']
        self.uid = int(attr.get('uid','-1'))
        self.user = attr.get('user','')
        self.version = int(attr.get('version','0'))
        self.timestamp = attr.get('timestamp','')
        self.visible = attr.get('visible','')
        self.changeset = attr.get('changeset','')
        if not tags:
            self.tags = {}
        else:
            self.tags = tags

    def __cmp__(self, other):
        cmp_ref = cmp(self.tags.get('ref',''), other.tags.get('ref',''))
        if cmp_ref:
            return cmp_ref
        cmp_name = cmp(self.tags.get('name',''), other.tags.get('name',''))
        if cmp_name:
            return cmp_name
        return cmp(self.id, other.id)

    def attributes(self):
        d = dict([(k,getattr(self,k)) for k in self.ATTRIBUTES])
        for k,v in d.items():
            if type(v) == int:
                d[k] = str(v)
        return d

    def __repr__(self):
        return "Node(attr=%r, tags=%r)" % (self.attributes(), self.tags)

class Way(object):
    ATTRIBUTES = ['id', 'timestamp', 'uid', 'user', 'visible', 'version', 'changeset']
    def __init__(self, attr, nodes=None, tags=None):
        self.id = int(attr['id'])
        self.uid = int(attr.get('uid','-1'))
        self.user = attr.get('user','')
        self.version = int(attr.get('version','0'))
        self.timestamp = attr.get('timestamp','')
        self.visible = attr.get('visible','')
        self.changeset = attr.get('changeset','')

        if not nodes:
            self.nodes = []
        else:
            self.nodes = nodes
        if not tags:
            self.tags = {}
        else:
            self.tags = tags

    def __cmp__(self, other):
        cmp_ref = cmp(self.tags.get('ref',''), other.tags.get('ref',''))
        if cmp_ref:
            return cmp_ref
        cmp_name = cmp(self.tags.get('name',''), other.tags.get('name',''))
        if cmp_name:
            return cmp_name
        return cmp(self.id, other.id)

    def attributes(self):
        d = dict([(k,getattr(self,k)) for k in self.ATTRIBUTES])
        for k,v in d.items():
            if type(v) == int:
                d[k] = str(v)
        return d

    def __repr__(self):
        return "Way(attr=%r, nodes=%r, tags=%r)" % (self.attributes(), self.nodes, self.tags)

class Relation(object):
    ATTRIBUTES = ['id', 'timestamp', 'uid', 'user', 'visible', 'version', 'changeset']
    def __init__(self, attr, members=None, tags=None):
        self.id = int(attr['id'])
        self.uid = int(attr.get('uid','-1'))
        self.user = attr.get('user','')
        self.version = int(attr.get('version','0'))
        self.timestamp = attr.get('timestamp','')
        self.visible = attr.get('visible','')
        self.changeset = attr.get('changeset','')

        if not members:
            self.members = []
        else:
            self.members = members
        if not tags:
            self.tags = {}
        else:
            self.tags = tags
      
    def __cmp__(self, other):
        cmp_ref = cmp(self.tags.get('ref',''), other.tags.get('ref',''))
        if cmp_ref:
            return cmp_ref
        cmp_name = cmp(self.tags.get('name',''), other.tags.get('name',''))
        if cmp_name:
            return cmp_name
        return cmp(self.id, other.id)

    def attributes(self):
        d = dict([(k,getattr(self,k)) for k in self.ATTRIBUTES])
        for k,v in d.items():
            if type(v) == int:
                d[k] = str(v)
        return d

    def __repr__(self):
        return "Relation(attr=%r, members=%r, tags=%r)" % (self.attributes(), self.members, self.tags)

class ObjectPlaceHolder(object):
    def __init__(self, id, type=None, role=''):
        self.id = int(id)
        self.type = type
        self.role = role

        self.tags = {}
        self.nodes = []
        self.members =[]

    def __repr__(self):
        return "ObjectPlaceHolder(id=%r, type=%r, role=%r)" % (self.id, self.type, self.role)

class OSCXMLFile(object):
    """
    An object representing an OSM Changes file (.osc)

    Much like OSMXMLFile, but this is for dealing with an OSM changes file,
    and currently only supports extracting information about the nodes.
    """

    def __init__(self, filename=None, content=None, options={}):
        self.filename = filename
        self.create_nodes = {}
        self.modify_nodes = {}
        self.delete_nodes = {}
        self.create_ways = {}
        self.modify_ways = {}
        self.delete_ways = {}
        self.create_relations = {}
        self.modify_relations = {}
        self.delete_relations = {}
        self.osmattrs = {}
        self.options = {
            'load_nodes': True,
            'load_ways': True,
            'load_way_nodes': True,
            'load_relations': True,
            'filterfunc': False
        }
        self.options.update(options)
        if filename:
            self.__parse()
        elif content:
            self.__parse(content)

    def __parse(self, content=None):
        """Parse the given XML file"""
        handler = OSCXMLFileParser(self)
        if content:
            xml.sax.parseString(content, handler)
        else:
            xml.sax.parse(self.filename, handler)

        # now fix up all the refereneces
        # or, we would if we cared about ways/relations

    def statistic(self):
        """Print a short statistic about the osc file object"""
        log.info("filename      : %s", self.filename)
        log.info("nodes created : %i", len(self.create_nodes))
        log.info("nodes modified: %i", len(self.modify_nodes))
        log.info("nodes deleted : %i", len(self.delete_nodes))
        log.info("ways created : %i", len(self.create_ways))
        log.info("ways modified: %i", len(self.modify_ways))
        log.info("ways deleted : %i", len(self.delete_ways))
        log.info("relations created : %i", len(self.create_relations))
        log.info("relations modified: %i", len(self.modify_relations))
        log.info("relations deleted : %i", len(self.delete_relations))

class OSMXMLFile(object):
    def __init__(self, filename=None, content=None, options={}):
        self.filename = filename

        self.nodes = {}
        self.ways = {}
        self.relations = {}
        self.osmattrs = {'version':'0.6'}
        self.options = {'load_nodes': True,
                        'load_ways': True,
                        'load_relations': True,
                        'load_way_nodes': True,
                        'load_relation_members': True,
                        'filterfunc': False}
        self.options.update(options)
        if filename:
            self.__parse()
        elif content:
            self.__parse(content)
    
    def __get_member(self, id, type):
        if type == "node":
            obj = self.nodes.get(id)
            if not obj:
                obj = ObjectPlaceHolder(id, type)
                self.nodes[id] = obj
        elif type == "way":
            obj = self.ways.get(id)
            if not obj:
                obj = ObjectPlaceHolder(id, type)
                self.ways[id] = obj
        elif type == "relation":
            obj = self.relations.get(id)
            if not obj:
                obj = ObjectPlaceHolder(id, type)
                self.relations[id] = obj
        else:
            log.warn("Don't know type %r in __get_obj", type)
            return None

        return obj

    def __parse(self, content=None):
        """Parse the given XML file"""
        handler = OSMXMLFileParser(self)
        if content:
            xml.sax.parseString(content, handler)
        else:
            xml.sax.parse(self.filename, handler)

        # now fix up all the refereneces
        for way in self.ways.values():
            way.nodes = [self.__get_member(node_pl.id, 'node') for node_pl in way.nodes]
              
        for relation in self.relations.values():
            relation.members = [(self.__get_member(obj_pl.id, obj_pl.type), obj_pl.role) for obj_pl in relation.members]

    def merge(self, osmxmlfile, update=True):
        for node in osmxmlfile.nodes.values():
            self.nodes[node.id] = node
        for way in osmxmlfile.ways.values():
            self.ways[way.id] = way
        for relation in osmxmlfile.relations.values():
            self.relations[relation.id] = relation

        # now fix up all the references
        for way in self.ways.values():
            way.nodes = [self.__get_member(node_pl.id, 'node') for node_pl in way.nodes]
              
        for relation in self.relations.values():
            types = {Node: 'node', Way: 'way', Relation: 'relation'}
            l = relation.members
            relation.members = []
            for obj, role in l:
                t = types.get(type(obj))
                if not t:
                    relation.members.append((obj, role))
                else:
                    relation.members.append((self.__get_member(obj.id, t), role))
        
    def write(self, fileobj):
        if type(fileobj) == str:
            fileobj = open(fileobj, 'wt')
        handler = xml.sax.saxutils.XMLGenerator(fileobj, 'UTF-8')
        handler.startDocument()
        handler.startElement('osm', self.osmattrs)
        handler.characters('\n')

        for nodeid in sorted(self.nodes):
            node = self.nodes[nodeid]
            if type(node) == ObjectPlaceHolder:
                continue
            handler.startElement('node', node.attributes())
            for name, value in node.tags.items():
                handler.characters('  ')
                handler.startElement('tag', {'k': name, 'v': value})
                handler.endElement('tag')
                handler.characters('\n')
            handler.endElement('node')
            handler.characters('\n')

        for wayid in sorted(self.ways):
            way = self.ways[wayid]
            if type(way) == ObjectPlaceHolder:
                continue
            handler.startElement('way', way.attributes())
            handler.characters('\n')
            for node in way.nodes:
                handler.characters('  ')
                handler.startElement('nd', {'ref': str(node.id)})
                handler.endElement('nd')
                handler.characters('\n')
            for name, value in way.tags.items():
                handler.characters('  ')
                handler.startElement('tag', {'k': name, 'v': value})
                handler.endElement('tag')
                handler.characters('\n')
            handler.endElement('way')
            handler.characters('\n')
            
        for relationid in sorted(self.relations):
            relation = self.relations[relationid]
            if type(relation) == ObjectPlaceHolder:
                continue
            handler.startElement('relation', relation.attributes())
            for obj, role in relation.members:
                if type(obj) == ObjectPlaceHolder:
                    obj_type = obj.type
                else:
                    obj_type = {Node: 'node', Way: 'way', Relation: 'relation'}[type(obj)]
                handler.characters('  ')
                handler.startElement('member', {'type': obj_type, 'ref': str(obj.id), 'role': role})
                handler.endElement('member')
                handler.characters('\n')
            for name, value in relation.tags.items():
                handler.characters('  ')
                handler.startElement('tag', {'k': name, 'v': value})
                handler.endElement('tag')
                handler.characters('\n')
            handler.endElement('relation')
            handler.characters('\n')

        handler.endElement('osm')
        handler.endDocument()

    def statistic(self):
        """Print a short statistic about the osm object"""
        log.info("Filename: %s", self.filename)
        log.info("  Nodes    : %i", len(self.nodes))
        log.info("  Ways     : %i", len(self.ways))
        log.info("  Relations: %i", len(self.relations))

class OSCXMLFileParser(xml.sax.ContentHandler):
    """
    Handles an OSM changes file, .osc, supplying three lists, of created,
    modified, and deleted nodes from the changes file.

    Based heavily on OSMXMLFileParser, but currently only supports nodes..
    """
    def __init__(self, containing_obj):
        self.containing_obj = containing_obj
        self.load_nodes = containing_obj.options['load_nodes']
        self.load_ways = containing_obj.options['load_ways']
        self.load_way_nodes = containing_obj.options['load_way_nodes']
        self.load_relations = containing_obj.options['load_relations']

        self.curr_node = None
        self.curr_way = None
        self.curr_relation = None
        self.curr_osmattrs = None
        self.mode_modify = False
        self.mode_delete = False
        self.mode_create = False

    def startElement(self, name, attrs):
        if name == 'modify':
            self.mode_modify = True
        elif name == 'delete':
            self.mode_delete = True
        elif name == 'create':
            self.mode_create = True

        elif name == 'node':
            if self.load_nodes:
                self.curr_node = Node(attr=attrs)
        elif name == 'way':
            if self.load_ways:
                self.curr_way = Way(attr=attrs)
        elif name == 'relation':
            if self.load_relations:
                self.curr_relation = Relation(attr=attrs)

        elif name == 'tag':
            if self.curr_node:
                self.curr_node.tags[attrs['k']] = attrs['v']
            elif self.curr_way:
                self.curr_way.tags[attrs['k']] = attrs['v']
            elif self.curr_relation:
                self.curr_relation.tags[attrs['k']] = attrs['v']

        elif name == "nd":
            if self.load_way_nodes:
                assert self.curr_node is None, "curr_node (%r) is non-none" % (self.curr_node)
                assert self.curr_way is not None, "curr_way is None"
                self.curr_way.nodes.append(ObjectPlaceHolder(id=attrs['ref']))

        elif name == "osmChange":
            self.curr_osmattrs = attrs

        else:
            log.warn("Unexpected element %s", name)

    def endElement(self, name):
        if name == 'modify':
            self.mode_modify = False
        elif name == 'delete':
            self.mode_delete = False
        elif name == 'create':
            self.mode_create = False

        elif name == "node":
            if self.load_nodes:
                if self.mode_modify:
                    self.containing_obj.modify_nodes[self.curr_node.id] = self.curr_node
                elif self.mode_delete:
                    self.containing_obj.delete_nodes[self.curr_node.id] = self.curr_node
                elif self.mode_create:
                    self.containing_obj.create_nodes[self.curr_node.id] = self.curr_node
                else:
                    log.warn("Finished a node without being in a valid mode?: %s", self.curr_node)
            self.curr_node = None

        elif name == "way":
            if self.load_ways:
                if self.mode_modify:
                    self.containing_obj.modify_ways[self.curr_way.id] = self.curr_way
                elif self.mode_delete:
                    self.containing_obj.delete_ways[self.curr_way.id] = self.curr_way
                elif self.mode_create:
                    self.containing_obj.create_ways[self.curr_way.id] = self.curr_way
                else:
                    log.warn("Finished a way without being in a valid mode?: %s", self.curr_way)
            self.curr_way = None

        elif name == "relation":
            if self.load_relations:
                if self.mode_modify:
                    self.containing_obj.modify_relations[self.curr_relation.id] = self.curr_relation
                elif self.mode_delete:
                    self.containing_obj.delete_relations[self.curr_relation.id] = self.curr_relation
                elif self.mode_create:
                    self.containing_obj.create_relations[self.curr_relation.id] = self.curr_relation
                else:
                    log.warn("Finished a relation without being in a valid mode?: %s", self.curr_relation)
            self.curr_relation = None

        elif name == "osmChange":
            self.containing_obj.osmattrs = self.curr_osmattrs
            self.curr_osmtags = None


class OSMXMLFileParser(xml.sax.ContentHandler):
    def __init__(self, containing_obj):
        self.containing_obj = containing_obj
        self.load_nodes = containing_obj.options['load_nodes']
        self.load_ways = containing_obj.options['load_ways']
        self.load_relations = containing_obj.options['load_relations']
        self.load_way_nodes = containing_obj.options['load_way_nodes']
        self.load_relation_members = containing_obj.options['load_relation_members']
        self.filterfunc = containing_obj.options['filterfunc']

        self.curr_node = None
        self.curr_way = None
        self.curr_relation = None
        self.curr_osmattrs = None

    def startElement(self, name, attrs):
        if name == 'node':
            if self.load_nodes:
                self.curr_node = Node(attr=attrs)
            
        elif name == 'way':
            if self.load_ways:
                self.curr_way = Way(attr=attrs)
            
        elif name == "relation":
            if self.load_relations:
                assert self.curr_node is None, "curr_node (%r) is non-none" % (self.curr_node)
                assert self.curr_way is None, "curr_way (%r) is non-none" % (self.curr_way)
                assert self.curr_relation is None, "curr_relation (%r) is non-none" % (self.curr_relation)
                self.curr_relation = Relation(attr=attrs)

        elif name == 'tag':
            if self.curr_node:
                self.curr_node.tags[attrs['k']] = attrs['v']
            elif self.curr_way:
                self.curr_way.tags[attrs['k']] = attrs['v']
            elif self.curr_relation:
                self.curr_relation.tags[attrs['k']] = attrs['v']
                
        elif name == "nd":
            if self.load_way_nodes:
                assert self.curr_node is None, "curr_node (%r) is non-none" % (self.curr_node)
                assert self.curr_way is not None, "curr_way is None"
                self.curr_way.nodes.append(ObjectPlaceHolder(id=attrs['ref']))
          
        elif name == "member":
            if self.load_relation_members:
                assert self.curr_node is None, "curr_node (%r) is non-none" % (self.curr_node)
                assert self.curr_way is None, "curr_way (%r) is non-none" % (self.curr_way)
                assert self.curr_relation is not None, "curr_relation is None"
                self.curr_relation.members.append(ObjectPlaceHolder(id=attrs['ref'], type=attrs['type'], role=attrs['role']))
          
        elif name == "osm":
            self.curr_osmattrs = attrs

        elif name == "bound":
            pass

        else:
            log.warn("Don't know element %s", name)


    def endElement(self, name):
        
        if name == "node":
            if self.load_nodes:
                if self.filterfunc:
                    if not self.filterfunc(self.curr_node):
                        self.curr_node = None
                        return
                self.containing_obj.nodes[self.curr_node.id] = self.curr_node
            self.curr_node = None
 
        elif name == "way":
            if self.load_ways:
                if self.filterfunc:
                    if not self.filterfunc(self.curr_way):
                        self.curr_way = None
                        return
                self.containing_obj.ways[self.curr_way.id] = self.curr_way
            self.curr_way = None
        
        elif name == "relation":
            if self.load_relations:
                if self.filterfunc:
                    if not self.filterfunc(self.curr_relation):
                        self.curr_relation = None
                        return
                self.containing_obj.relations[self.curr_relation.id] = self.curr_relation
            self.curr_relation = None

        elif name == "osm":
            self.containing_obj.osmattrs = self.curr_osmattrs
            self.curr_osmtags = None


#################### MAIN            

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s - %(message)s")
    import sys
    for filename in sys.argv[1:]:
        ext = filename[-3:]
        if ext == 'osm':
            osm = OSMXMLFile(filename)
            osm.statistic()
        elif ext == 'osc':
            osc = OSCXMLFile(filename)
            osc.statistic()
        else:
            log.warn("Unrecognised file extension (.osm or .osc): %s", filename)


