'''
Created on Aug 28, 2014

@author: qurban.ali
'''

import pymel.core as pc
import appUsageApp
import qutil

def fill():
    
    sel = pc.ls(sl=True)
    
    if not sel:
        pc.warning('Select a mesh or camera')
        return
    
    if len(sel) > 1:
        pc.warning('Select only one camera or mesh')
        return
    try:
        obj = sel[0].getShape(ni=True)
    except:
        pc.warning('Selection should be camera or mesh')
        return
    if type(obj) == pc.nt.Mesh:
        try:
            cache = obj.history(type='cacheFile')[0]
        except IndexError:
            pc.warning('No cache found on the selected object')
            return
        start = cache.sourceStart.get()
        end = cache.sourceEnd.get()
    elif type(obj) == pc.nt.Camera:
        animCurves = pc.listConnections(obj.firstParent(), scn=True, d=False, s=True)
        if not animCurves:
            pc.warning('No animation found on the selected camera...')
            return
        
        frames = pc.keyframe(animCurves[0], q=True)
        if not frames:
            pc.warning('No keys found on the selected camera...')
            return
        
        qutil.setRenderableCamera(obj)
        
        start = frames[0]
        end = frames[-1]
    else:
        pc.warning('Selection should be camera or mesh')
        return

    pc.playbackOptions(minTime=start)
    pc.setAttr("defaultRenderGlobals.startFrame", start)
    pc.playbackOptions(maxTime=end)
    pc.setAttr("defaultRenderGlobals.endFrame", end)
    
    appUsageApp.updateDatabase('fillinout')
    
    return start, end