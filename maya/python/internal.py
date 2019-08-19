import maya.cmds
import os
import re

import pathCorrector

def remapFileTexture(verbose=False):
  allFileNodes = cmds.ls(et="file")

  for each in allFileNodes:
    fileTx     = "%s.fileTextureName" % (each)
    attrFileTx = cmds.getAttr(fileTx)

    try:
      mp = cmds.dirmap(cd=(attrFileTx))

      if not os.path.exists(mp):
        remapped = pathCorrector.pathCorrector(mp, verbose=verbose)
        if mp != remapped:
          cmds.setAttr(fileTx, remapped, type="string")

          if verbose:
            msg_fileTx = "%s --> %s"%(mp, remapped)
            print("[remapFileTexture] %s" % (msg_fileTx))
      except Exception as e:
        print("[Err remapFileTexture] %s %s %s" % (fileTx, attrFileTx, e))

def _filteredReferenceNode():
  newRefNodes = []
  refNodes = cmds.ls(type="reference")
  for refNode in refNodes:
    if re.match(refNode, "\w+:sharedReferenceNode"):
      continue
    if re.match(refNode, "sharedReferenceNode"):
      continue
    if re.match(refNode, "_UNKNOWN_REF_NODE_"):
      continue

    newRefNode = cmds.referenceQuery(refNode, referenceNode=True)
    newRefNodes.append(newRefNode)

  return newRefNodes
  
def getReferencePath(nodes=[]):
  pathlist = []

  for node in nodes:
    try:
      path = cmds.referenceQuery(node, f=1).replace("\\", "/")
      pathlist.append(path)
    except Exception as e:
      print("[Err getReferencePath] %s" % e)

  return pathlist

def replaceReferencePath(pathlist=[], isWindows=None, verbose=False):
  if isWindows is None:
    isWindows= _checkOS()

  for path in pathlist:
    nodeName  = cmds.referenceQuery(path, referenceNode=True)
    oldPath   = cmds.referenceQuery(nodeName, f=1).split("{")[0]
    remapPath = remapSingleCaseSensitivePath(oldPath, verbose=verbose)

    matchPath = re.match(oldPath, remapPath)
    if not matchPath:
      if verbose:
        notmatch_msg = "%s --> %s" % (oldPath, remapPath)
        print("[remapReference] %s" % (notmatch_msg))
      cmds.file(remapPath, options="v=0;p=17", loadReference=nodeName)

def runReplaceRefPath():
  pathlist = getReferencePath(_filteredReferenceNode())
  replaceReferencePath(pathlist=pathlist)