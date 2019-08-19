import os
import sys
import re
import shutil

def showUsage():
   print("USAGE")
   print("This script is to correct path inside maya")
   print("-sc/--scene      <path> : Maya File Path")
   print("-bd/--backup-dir <path> : Backup Directory")
   print("--verbose        <bool> : Show Log")
   print("-dr/--dry-run    <bool> : Do not execute")
   print("-h/--help        <bool> : Show Help")

if __name__ == "__main__":
   args = sys.argv
   nargs = len(args)
   iarg = 0

   def _exit(rv):
      val = 0
      if not rv:
         val = 1
      sys.exit(val)

   mayaScene = ""
   backupDir = ""
   verbose   = False
   dryRun    = False


   while iarg < nargs:
      arg = args[iarg]
      if arg in ("-sc", "--scene"):
         iarg += 1
         if iarg >= nargs:
            print("-sc/--scene flag expects a maya file path argument")
            _exit(1)
         mayaScene = args[iarg]
      elif arg in ("-bd", "--backup-dir"):
         iarg += 1
         if iarg >= nargs:
            print("-od/--backup-dir flag expects a path argument")
            _exit(1)
         backupDir = args[iarg]
      elif arg in ("--verbose"):
         verbose = True
      elif arg in ("-dr", "--dry-run"):
         dryRun = True
      elif arg in ("-h", "--help"):
         showUsage()
         _exit(0)
      iarg += 1

   if not backupDir:
      backupDir = os.path.join(os.path.dirname(mayaScene), "backup")
      
   if not os.path.exists(backupDir):
      os.makedirs(backupDir)

   files = os.listdir(backupDir)
   files.sort(reverse=True)

   ver = 1

   latest    = files[-1]
   findVer   = re.search("v\d{3}$", latest)

   if findVer:
      strVer = findVer.group(0).split("v")[-1]
      ver    = int(strVer) + 1

   newVer = "v%03d" % ver

   scene, ext = os.path.splitext(os.path.basename(mayaScene))
   nscene = "{name}_backup_{version}.{ext}".format(name=scene, version=newVer, ext=ext)

   backupScene = os.path.join(backupDir, nscene).replace("\\","/")

   shutil.copyfile(mayaScene, backupScene)
