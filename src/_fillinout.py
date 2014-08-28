'''
Created on Aug 28, 2014

@author: qurban.ali
'''

import pymel.core as pc

def fill():
    
    cam = pc.ls(sl=True, dag=True, type='camera')
    
    if not cam:
        pc.warning('No camera selected...')
        return
    
    if len(cam) > 1:
        pc.warning('More than one cameras selected...')
        return
    
    cam = cam[0]
    animCurves = pc.listConnections(cam.firstParent(), scn=True, d=False, s=True)
    if not animCurves:
        pc.warning('No animation found on the selected camera...')
        return
    
    frames = pc.keyframe(animCurves[0], q=True)
    if not frames:
        pc.warning('No keys found on the selected camera...')
        return
    
    start = frames[0]
    end = frames[-1]
    
    pc.playbackOptions(minTime=start)
    pc.setAttr("defaultRenderGlobals.startFrame", start)
    pc.playbackOptions(maxTime=end)
    pc.setAttr("defaultRenderGlobals.endFrame", end)