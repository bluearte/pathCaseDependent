import os
import sys
import re

def _findDriveLetter(driveLetter="/"):
  if driveLetter == "":
    driveLetter = "/"
  driveName = driveLetter

  drivePattern = re.compile("[aA-zZ]:")
  driveSearch  = drivePattern.search(driveLetter)

  if driveSearch:
    upperLetter = driveSearch.group(0).upper()
    driveName   = os.path.join(upperLetter, "/").replace("\\", "/")
  return driveName

def pathCorrector(path, verbose=False):
  dirpath_split = re.compile("(/+|\+)")
  cache         = dict()

  drv, dirPath = os.path.splitdrive(path)

  driveLetter = _findDriveLetter(drv)

  uniRoot = unicode(driveLetter)
  uniPath = unicode(dirPath[:-1]) if dirPath[-1] == "/" else unicode(dirPath)

  path_parts = dirpath_split.split(uniPath)

  for n, part in enumerate(path_parts):
    uncorrected_path = os.path.join(uniRoot, *path_parts[0:len(path_parts)-n]).replace("\\", "/").lower()

    if uncorrected_path in cache:
      uniRoot    = os.path.join(uniRoot, cache[uncorrected_path]).replace("\\", "/")
      path_parts = path_parts[len(path_parts)-n:]
      break

  for n, part in enumerate(path_parts):
    if part not in os.listdir(uniRoot):
      list_dir = os.listdir(uniRoot)

      lower_path_parts = part.lower()
      lower_path       = [l.lower() for l in list_dir]

      if lower_path_parts in lower_path:
        l                = list_dir[lower_path.index(lower_path_parts)]
        cacheKeys        = os.path.join(uniRoot, part).replace("\\", "/").lower()
        uniRoot          = os.path.join(uniRoot, l).replace("\\", "/")
        cache[cacheKeys] = uniRoot

    else:
      uniRoot = os.path.join(uniRoot, part).replace("\\", "/")

  if verbose:
    if os.path.exists(uniRoot):
      if path.replace("\\", "/") != uniRoot:
        print ("[OLD] %s --> [NEW] %s" %(path, uniRoot))

  return uniRoot