from pathlib import Path
from nsz.FileExistingChecks import CreateTargetDict
from nsz.nut import Print
import os
import re

def isOnWhitelist(args, file):
	if not args.undupe_whitelist == "" and re.match(args.undupe_whitelist, file):
		#if args.undupe_dryrun:
		#	Print.info("[DRYRUN] [WHITELISTED]: " + file)
		#else:
		#	Print.info("[WHITELISTED]: " + file)
		return True
	return False

def undupe(args):
	filesAtTarget = {}
	alreadyExists = {}
	for f_str in args.file:
		(filesAtTarget, alreadyExists) = CreateTargetDict(Path(f_str).absolute(), True, None, filesAtTarget, alreadyExists)
	Print.info("")

	for (titleID_key, titleID_value) in alreadyExists.items():
		maxVersion = max(titleID_value.keys())
		for (version_key, version_value) in titleID_value.items():

			if args.undupe_old_versions and version_key < maxVersion:
				for file in list(version_value):
					if not isOnWhitelist(args, file):
						if args.undupe_dryrun:
							Print.info("[DRYRUN] [DELETE] [OLD_VERSION]: " + file)
						else:
							os.remove(file)
							Print.info("[DELETED] [OLD_VERSION]: " + file)
				continue


			if not args.undupe_blacklist == "":
				for file in list(version_value):
					if not isOnWhitelist(args, file) and re.match(args.undupe_blacklist, file):
						version_value.remove(file)
						if args.undupe_dryrun:
							Print.info("[DRYRUN] [DELETE] [BLACKLIST]: " + file)
						else:
							os.remove(file)
							Print.info("[DRYRUN] [DELETED] [BLACKLIST]: " + file)

			if not args.undupe_prioritylist == "":
				for file in list(version_value.reverse()):
					if len(version_value) > 1 and not isOnWhitelisth(args, file) and re.match(args.undupe_prioritylist, file):
						version_value.remove(file)
						if args.undupe_dryrun:
							Print.info("[DRYRUN] [DELETE] [PRIORITYLIST]: " + file)
						else:
							os.remove(file)
							Print.info("[DRYRUN] [DELETED] [PRIORITYLIST]: " + file)

			firstDeleted = False
			for file in list(version_value[1:]):
				if not isOnWhitelist(args, file):
					if args.undupe_dryrun:
						Print.info("[DRYRUN] [DELETE] [DUPE]: " + file)
						Print.info("Keeping " + version_value[0])
					else:
						os.remove(file)
						Print.info("[DELETED] [DUPE]: " + file)
						Print.info("Keeping " + version_value[0])
				elif not firstDeleted and not isOnWhitelist(args, version_value[0]):
					firstDeleted = True
					if args.undupe_dryrun:
						Print.info("[DRYRUN] [DELETE] [DUPE]: " + version_value[0])
						Print.info("Keeping " + file)
					else:
						os.remove(version_value[0])
						Print.info("[DELETED] [DUPE]: " + version_value[0])
						Print.info("Keeping " + file)
