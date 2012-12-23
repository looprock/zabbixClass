#!/usr/bin/env python
import json
import urllib2
import re
import sys

# DOCS:
# http://www.zabbix.com/documentation/1.8/api/getting_started
# http://www.zabbix.com/documentation/1.8/api/host/create

class api(object):
	def __init__(self,zurl,zauthid,zauthhash):
		global url
		global authid
		global authhash
		global getallhosts
		global getallgroups
		global getalltemplates
		url = zurl
		authid = zauthid
		authhash = zauthhash
		getallhosts = """{
			"jsonrpc": "2.0",
			"method": "host.get",
			"params": {
				"output": "extend"
			},
			"id": %s,
			"auth": "%s"
		}""" % (authid,authhash)	
		getallgroups = """{ 
			"jsonrpc": "2.0", 
			"method": "hostgroup.get", 
			"params": { 
				"output": "extend", 
				"sortfield": "name" 
			}, 
			"id": %s, 
			"auth": "%s" 
		}""" % (authid,authhash)
		getalltemplates = """{ 
			"jsonrpc": "2.0", 
			"method": "template.get", 
			"params": { 
				"output": "extend", 
				"sortfield": "name" 
			}, 
			"id": %s, 
			"auth": "%s" 
		}""" % (authid,authhash)
	def getoutput(self,data):
		req = urllib2.Request(url)
		req.add_header('Content-Type', 'application/json')
		params = json.dumps(json.loads(data))
		resp = urllib2.urlopen(req, params).read()
		output = json.loads(resp)
		return output
	def printid(self,s,data,name,id):
		list = []
		r = self.getoutput(data)
		for i in range(0,len(r['result'])):
			rs = re.compile(s, re.IGNORECASE)
			j = re.search(rs, r['result'][i][name])
			if j != None:
				list.append(str(r['result'][i][id]))
		if len(list) > 1:
			print "Too many ids (%s) returned for '%s', please refine your search" % (str(len(list)),s)
			sys.exit(1)
		if len(list) == 0:
			print "No id returned for: %s" % s
			sys.exit(1)
		return list[0]
	def addhost(self,hostname,ip,rgroups,rtemplates):
		groups = ""	
		for i in rgroups.split(","):
			rg = unicode(i)
			groups += "{ \"groupid\": %s }," % str(self.printid(rg,getallgroups,'name','groupid'))
		groups = groups[:-1]
		templates = ""
		for i in rtemplates.split(","):
			rt = unicode(i)
			templates += "{ \"templateid\": %s }," % str(self.printid(rt,getalltemplates,'host','hostid'))
		templates = templates[:-1]
		makehost = """{
			"jsonrpc": "2.0",
			"method": "host.create",
			"params": {
				"host": "%s",
				"ip": "%s",
				"port": 10050,
				"useip": 1,
				"groups": [
					%s
				],
				"templates":[
					%s
				]
			},
			"id": %s,
			"auth": "%s"
		}""" % (hostname,ip,groups,templates,authid,authhash)
		return self.getoutput(makehost)
	def delhost(self,rhosts):
		hostid = ""
		for i in rhosts.split(","):
			h = unicode(i)
			hostid += "{ \"hostid\": %s }," % str(self.printid(h,getallhosts,'host','hostid'))
		hostid = hostid[:-1]
		delhost = """{
			"jsonrpc":"2.0",
			"method":"host.delete",
			"params":[
				%s
			],
			"id":%s,
			"auth":"%s"
		}""" % (hostid,authid,authhash)
		return self.getoutput(delhost)
	def listhosts(self):
		r = self.getoutput(getallhosts)
		for i in range(0,len(r['result'])):
			print "%s: %s" % (str(r['result'][i]['host']),str(r['result'][i]['hostid']))
	def listhostgroups(self):
		r = self.getoutput(getallgroups)
		for i in range(0,len(r['result'])):
			print "%s: %s" % (str(r['result'][i]['name']),str(r['result'][i]['groupid']))
	def listtemplates(self):
		r = self.getoutput(getalltemplates)
		for i in range(0,len(r['result'])):
			print "%s: %s" % (str(r['result'][i]['host']),str(r['result'][i]['hostid']))
	def gethostid(self,h):
		s = unicode(h)
		return self.printid(s,getallhosts,'name','hostid')
	def gethostgroupid(self,hg):
		s = unicode(hg)
		return self.printid(s,getallgroups,'name','groupid')
	def gettemplateid(self,t):
		s = unicode(t)
		return self.printid(s,getalltemplates,'name','hostid')
	def addhostgroup(self,name):
		makegroup = """{
			"jsonrpc":"2.0",
			"method":"hostgroup.create",
			"params":[ {"name":"%s"} ],
			"id":%s,
			"auth":"%s"
		}""" % (name,authid,authhash)
		return self.getoutput(makegroup)
	def delhostgroup(self,hg):
		g = unicode(hg)
		groupid = self.printid(g,getallgroups,'name','groupid')
		delgroup = """{
			"jsonrpc":"2.0",
			"method":"hostgroup.delete",
			"params":[
				{
				"groupid":"%s"
				}
			],
			"id":%s,
			"auth":"%s"
		}""" % (groupid,authid,authhash)
		return getoutput(delgroup)
	def help(self):
		print """		Example Usage: 
		z = zabbix.api(url,authid,authhash)
		z.listhosts()
		
		Functions:
		addhost(hostname,ip,[list of hostgroup],[list of templates]) - Add a new zabbix host, and include it in the hostgroups and templates
		delhost(hostname) - Delete delete host from zabbix
		listhosts() - List all hosts and their associated IDs
		listhostgroups() - List all hostgroups and their IDs
		listtemplates() - List templates and their IDs
		gethostid(hostname) - return a host ID by it's name
		gethostgroupid(hostgroup) - return a hostgroup ID by it's name
		gettemplateid(template) - return a template ID by it's name
		addhostgroup(name) - add a hostgroup with the specified name
		delhostgroup(hostgroup) - delete a hostgroup with the specified name"""