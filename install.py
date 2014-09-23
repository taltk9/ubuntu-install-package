#!/usr/bin/env python
import subprocess
import json
import sys
import os.path

def actions(filename):
	apps = json.load(open(filename))
	installedPackages = {}
	installedPackagesFile = ".installed_packages.json"
	if (os.path.isfile(installedPackagesFile)) :
		installedPackages = json.load(open(installedPackagesFile))

	# settings = [
	# 	"run root",
	#	"package manager",
	#	"apply all terminal questions",
	#	"main command"
	# ]
	settings = [
		"sudo",
		"apt-get",
		"-y",
		"install"
	]
	toRun = ' '.join([str(x) for x in settings])

	for i in xrange(len(apps)):
		appFile = '.packages/' + apps[i] + '.json'
		# ! - terminal message (Ex.: "Success intalled app!")
		# $ - free code (doesn't apply the settings before command line)
		installedApps = json.load(open(appFile))
		commands = installedApps["command"]
		if apps[i] in installedPackages :
			updates = installedPackages[apps[i]]
			for pos in xrange(len(updates)):
				command = updates[pos]
				subprocess.Popen(command, shell=True).wait()
		else :
			for pos in xrange(len(commands)):
				command = commands[pos]
				freeCode = command[0] == "$"
				update = command == "!update"
				if freeCode:
					command = command[1:]
				elif update:
					command = "sudo apt-get update -y"
				else:
					command = toRun + " " + command
					if apps[i] in installedPackages :
						installedPackages[apps[i]].append(command)
					else:
						installedPackages[apps[i]] = []
						installedPackages[apps[i]].append(command)
				subprocess.Popen(command, shell=True).wait()
	with open(installedPackagesFile, 'w') as outfile:
		json.dump(installedPackages, outfile)

def install_apps(filenameArray):
	for i in xrange(len(filenameArray)):
		filename = filenameArray[i]
		profile = 'profiles/' + filename + '.json'
		try:
			with open(profile):
				actions(profile)			
		except IOError:
			print "\"{pname}\": profile doesn't exist.".format(pname = filename)
		
if __name__ == "__main__":
	ui = raw_input('Enter profile(s) name(s): ')
	filename = ui.split( )
	install_apps(filename)
