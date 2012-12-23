About:
My re-invention of the zabbix api class wheel. This was mostly to gain experience working with the zabbix 1.8 API. 
This likely won't continue to be developed unless I find all the other modules severly lacking.

Usage: 
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
delhostgroup(hostgroup) - delete a hostgroup with the specified name
