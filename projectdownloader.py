#!/usr/bin/env python3
global statusCodes
statusCodes = {200: ('OK', 'Request fulfilled, document follows'), 201: ('Created', 'Document created, URL follows'), 202: ('Accepted', 'Request accepted, processing continues off-line'), 203: ('Non-Authoritative Information', 'Request fulfilled from cache'), 204: ('No Content', 'Request fulfilled, nothing follows'), 205: ('Reset Content', 'Clear input form for further input.'), 206: ('Partial Content', 'Partial content follows.'), 400: ('Bad Request', 'Bad request syntax or unsupported method'), 401: ('Unauthorized', 'No permission -- see authorization schemes'), 402: ('Payment Required', 'No payment -- see charging schemes'), 403: ('Forbidden', 'Request forbidden -- authorization will not help'), 404: ('Not Found', 'Page not found on server'), 405: ('Method Not Allowed', 'Specified method is invalid for this server.'), 406: ('Not Acceptable', 'URI not available in preferred format.'), 407: ('Proxy Authentication Required', 'You must authenticate with this proxy before proceeding.'), 408: ('Connection Failed', 'Request timed out; try again later.'), 409: ('Conflict', 'Connection Reset/Request conflict.'), 410: ('Gone', 'URI no longer exists and has been permanently removed.'), 411: ('Length Required', 'Client must specify "Content-Length".'), 412: ('Precondition Failed', 'Precondition in headers is false.'), 413: ('Request Entity Too Large', 'Entity is too large.'), 414: ('Request-URI Too Long', 'URI is too long.'), 415: ('Unsupported Media Type', 'Entity body in unsupported format.'), 416: ('Requested Range Not Satisfiable', 'Cannot satisfy request range.'), 417: ('Expectation Failed', 'Expect condition could not be satisfied.'), 100: ('Continue', 'Request received, please continue'), 101: ('Switching Protocols', 'Switching to new protocol; obey Upgrade header'), 300: ('Multiple Choices', 'Object has several resources -- see URI list'), 301: ('Moved Permanently', 'Object moved permanently -- see URI list'), 302: ('Found', 'Object moved temporarily -- see URI list'), 303: ('See Other', 'Object moved -- see Method and URL list'), 304: ('Not Modified', 'Document has not changed since given time'), 305: ('Use Proxy', 'You must use proxy specified in Location to access this resource.'), 307: ('Temporary Redirect', 'Object moved temporarily -- see URI list'), 500: ('Internal Server Error', 'An error occurred within the server'), 501: ('Not Implemented', 'Server does not support this operation'), 502: ('Bad Gateway', 'Invalid responses from another server/proxy.'), 503: ('Service Unavailable', 'The server cannot process the request due to a high server load'), 504: ('Gateway Timeout', 'The gateway server did not receive a timely response'), 505: ('HTTP Version Not Supported', 'Cannot fulfill request.')}
global error_codes
error_codes = {111:('Invalid Argument','An internal function raised exception due to invalid argument(s)'), -128: ('Non-Authoritative Information', 'Request fulfilled from cache'), -127: ('Accepted', 'Request accepted, processing continues off-line'), -126: ('Created', 'Document created, URL follows'), -125: ('OK', 'Request fulfilled, document follows'), 146: ('Malformed JSON object', 'JSON Presented is an invalid format'), -429: ('Gateway Timeout', 'The gateway server did not receive a timely response'), -428: ('Service Unavailable', 'The server cannot process the request due to a high server load'), -427: ('Bad Gateway', 'Invalid responses from another server/proxy.'), -426: ('Not Implemented', 'Server does not support this operation'), -425: ('Internal Server Error', 'An error occurred within the server'), -232: ('Temporary Redirect', 'Object moved temporarily -- see URI list'), -230: ('Use Proxy', 'You must use proxy specified in Location to access this resource.'), -229: ('Not Modified', 'Document has not changed since given time'), -228: ('See Other', 'Object moved -- see Method and URL list'), -227: ('Found', 'Object moved temporarily -- see URI list'), -226: ('Moved Permanently', 'Object moved permanently -- see URI list'), -225: ('Multiple Choices', 'Object has several resources -- see URI list'), -430: ('HTTP Version Not Supported', 'Cannot fulfill request.'), -26: ('Switching Protocols', 'Switching to new protocol; obey Upgrade header'), -25: ('Continue', 'Request received, please continue'), -342: ('Expectation Failed', 'Expect condition could not be satisfied.'), -341: ('Requested Range Not Satisfiable', 'Cannot satisfy request range.'), -340: ('Unsupported Media Type', 'Entity body in unsupported format.'), -339: ('Request-URI Too Long', 'URI is too long.'), -338: ('Request Entity Too Large', 'Entity is too large.'), -337: ('Precondition Failed', 'Precondition in headers is false.'), -336: ('Length Required', 'Client must specify "Content-Length".'), -335: ('Gone', 'URI no longer exists and has been permanently removed.'), -334: ('Conflict', 'Connection Reset/Request conflict.'), -333: ('Connection Failed', 'Request timed out; try again later.'), -332: ('Proxy Authentication Required', 'You must authenticate with this proxy before proceeding.'), -331: ('Not Acceptable', 'URI not available in preferred format.'), -330: ('Method Not Allowed', 'Specified method is invalid for this server.'), -329: ('Not Found', 'Page not found on server'), -328: ('Forbidden', 'Request forbidden -- authorization will not help'), -327: ('Payment Required', 'No payment -- see charging schemes'), -326: ('Unauthorized', 'No permission -- see authorization schemes'), -325: ('Bad Request', 'Bad request syntax or unsupported method'), -131: ('Partial Content', 'Partial content follows.'), -130: ('Reset Content', 'Clear input form for further input.'), -129: ('No Content', 'Request fulfilled, nothing follows')}
global blank_zip
blank_zip = b'PK\x05\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
global blank_svg
blank_svg = b'<svg version="1.1" width="2" height="2" viewBox="-1 -1 2 2" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"></svg>'
global error_code
error_code = None

import requests
import sys
import os
import traceback
import time
import io
import zipfile
import json
import base64
import random

def write(cnt):
    sys.stdout.write(str(cnt).encode('cp850', errors='ignore').decode())
    sys.stdout.flush()
def pri(cnt):
    print(str(cnt).encode('cp850', errors='ignore').decode())
    sys.stdout.flush()

def downloadProject(pk, path):
    try:
        def updatePer(perc, fn=None):
            per10 = int(perc / 10)
            write('\rDownloading "' + str(fn).replace('None','null') + '" [' + (per10 * '#') + ((10 - per10) * ' ') + '] ' + str(perc) + '%')

        def per(num, denom, obj=str):
            try:
                return obj(int(num / denom * 100))
            except:
                return obj(0)

        def getAsset(md5, fn=None, customUrl=None):
            class ret: pass
            try:
                if not fn: fn = md5
                tb = None
                write('Downloading "' + fn + '" [          ] 0%')

                link = 'http://cdn.assets.scratch.mit.edu/internalapi/asset/' + str(md5) + '/get/'
                response = s.get(link, stream=True)
                total_length = response.headers.get('content-length')
                stCnt = b''
                if total_length is None:
                    stCnt = stCnt + (response.content)
                else:
                    dl = 0
                    total_length = int(total_length)
                    for data in response.iter_content(chunk_size=256):
                        stCnt = stCnt + data
                        dl += len(data)
                        done = dl / total_length
                        updatePer(int(done * 100), fn)
                updatePer(100, fn)
                pri(' ...Done')
                istr = io.BytesIO(stCnt)
            except BaseException as e:
                tb = e
                pri(traceback.format_exc())
                rt = {'iostream':None,'code':-1}
            else:
                rt = {'iostream':istr,'code':response.status_code}
            ret.code = rt['code']; ret.iostream = rt['iostream'].getvalue(); ret.tb = tb
            return ret
        def processAsset(fid, md5, path, tp, name=None): #j[path['node']][path['spriteIndex']][path['assetType']][path['assetIndex']]
            if path['node'] is not None:
                try:
                    bad_code = 0
                    stream = getAsset(md5, name)
                    n = int(str(stream.code)[0])
                    if ((n == 1) or (n > 3)) or (stream.tb != None):
                        bad_code = -1
                        raise RuntimeError()
                    ext = os.path.splitext(md5)[1]
                    if tp == 'imageLayer':
                        j[path['node']][path['spriteIndex']][path['assetType']][path['assetIndex']]['baseLayerID'] = int(fid)
                    elif tp == 'textLayer':
                        j[path['node']][path['spriteIndex']][path['assetType']][path['assetIndex']]['textLayerID'] = int(fid)
                    else:
                        j[path['node']][path['spriteIndex']][path['assetType']][path['assetIndex']]['soundID'] = int(fid)
                    zipf.writestr(str(fid) + ext, stream.iostream)
                except BaseException as e:
                    if stream.tb:
                        err = stream.tb
                    else:
                        err = e
                    return {'success':False, 'error':bad_code, 'statusCode':stream.code, 'err':err}
                else:
                    return {'success':True, 'error':None, 'statusCode':stream.code}
            else:
                try:
                    bad_code = 0
                    stream = getAsset(md5, name)
                    n = int(str(stream.code)[0])
                    if ((n != 1) and (n > 4)) and (stream.tb != None):
                        bad_code = 1
                        if stream.tb != None:
                            bad_code = 111
                        raise RuntimeError()
                    ext = os.path.splitext(md5)[1]
                    if tp == 'imageLayer':
                        j[path['assetType']][path['assetIndex']]['baseLayerID'] = int(fid)
                    elif tp == 'textLayer':
                        j[path['assetType']][path['assetIndex']]['textLayerID'] = int(fid)
                    else:
                        j[path['assetType']][path['assetIndex']]['soundID'] = int(fid)
                    zipf.writestr(str(fid) + ext, stream.iostream)
                except BaseException as e:
                    if stream.tb:
                        err = stream.tb
                    else:
                        err = e
                    return {'success':False, 'error':bad_code, 'statusCode':stream.code, 'err':err}
                else:
                    return {'success':True, 'error':None, 'statusCode':stream.code}
        def processAssetContent(fid, stream, path, tp, ext): #j[path['node']][path['spriteIndex']][path['assetType']][path['assetIndex']]
            if tp == 'imageLayer':
                j[path['node']][path['spriteIndex']][path['assetType']][path['assetIndex']]['baseLayerID'] = int(fid)
            elif tp == 'textLayer':
                j[path['node']][path['spriteIndex']][path['assetType']][path['assetIndex']]['textLayerID'] = int(fid)
            else:
                j[path['node']][path['spriteIndex']][path['assetType']][path['assetIndex']]['soundID'] = int(fid)
            zipf.writestr(str(fid) + ext, stream)

        
        s = requests.session()
        write('Downloading JSON...')
        pjson = s.get('http://cdn.projects.scratch.mit.edu/internalapi/project/' + str(pk) + '/get/', stream=True)
        pri('Done [' + str(pjson.status_code) + ']')
        try:
            assert pjson.status_code == 200
            j = pjson.json()
        except AssertionError:
            return {'status':'error','error':'Project JSON API returned bad status code','code':encodeStatus(pjson.status_code),'stack':False}
        except:
            return {'status':'error','error':'Malformed JSON','stack':True,'code':146}

        write('Downloading API Specs...')
        pinfo = s.get('https://scratch.mit.edu/api/v1/project/' + str(pk) + '/?format=json')  
        try:
            assert pinfo.status_code == 200
            info = info.json()
        except AssertionError:
            pri('Failed, server error [Nonfatal]')
            info = {'title':'Scratch Project'}
        except:
            pri('Failed, JSON corrupt [Nonfatal]')            
        else:
            pri('Done [' + str(pinfo.status_code) + ']')

        pri('Buffering...')
        buf = io.BytesIO(blank_zip)
        zipf = zipfile.ZipFile(buf, mode='w')
        pri('Looking for assets')
        assets = []
        imgCount = 0
        sfxCount = 0
        listIndex = -1
        if not ('costumes' in j):
            pri('WARN: Costumes tag missing in "__stage__"')
            j['costumes'] = []
            j['costumes'].append({"costumeName": "costume-1", "baseLayerID": -1,"baseLayerMD5": "cd21514d0531fdffb22204e0ec5ed84a.svg","bitmapResolution": 1,"rotationCenterX": 240,"rotationCenterY": 180})
        if len(j['costumes']) == 0:
            pri('WARN: Costumes tag empty. Fixing...')
            j['costumes'].append({"costumeName": "costume-1", "baseLayerID": -1,"baseLayerMD5": "cd21514d0531fdffb22204e0ec5ed84a.svg","bitmapResolution": 1,"rotationCenterX": 240,"rotationCenterY": 180})
        for y in j['costumes']:
            listIndex = listIndex + 1
            pri('__stage__' + ' > [c]' + y['costumeName'])
            assets.append({'id':imgCount,'md5':y['baseLayerMD5'],'route':{'node':None,'spriteIndex':None,'assetType':'costumes','assetIndex':listIndex},'type':'imageLayer','display':'__stage__' + ' > ☼' + y['costumeName']})
            imgCount = imgCount + 1
            if 'textLayerID' in y:
                assets.append({'id':imgCount,'md5':y['textLayerMD5'],'route':{'node':None,'spriteIndex':None,'assetType':'costumes','assetIndex':listIndex},'type':'textLayer', 'display':'__stage__' + ' > ☼' + y['costumeName'] + '/Old-1.4textLayer'})
                imgCount = imgCount + 1
        if 'sounds' in j:
            internalListIndex = 0
            for y in j['sounds']:
                pri('__stage__' + ' > [s]' + y['soundName'])
                assets.append({'id':sfxCount,'md5':y['md5'],'route':{'node':None,'spriteIndex':None,'assetType':'sounds','assetIndex':internalListIndex},'type':'sound','display':'__stage__' + ' > ♫' + y['soundName']})
                internalListIndex = internalListIndex + 1
                sfxCount = sfxCount + 1
        listIndex = -1
        for x in j['children']:
            listIndex = listIndex + 1
            if not ('objName' in x): # True if not a sprite. 'objName' should be in a sprite
                continue
            if not ('costumes' in x):
                pri('WARN: Costumes tag missing in "' + x['objName'] + '"')
                j['children'][listIndex]['costumes'] = []
                j['children'][listIndex]['costumes'].append({"costumeName": "costume-1", "baseLayerID": -1,"baseLayerMD5": "cd21514d0531fdffb22204e0ec5ed84a.svg","bitmapResolution": 1,"rotationCenterX": 240,"rotationCenterY": 180})
            if len(x['costumes']) == 0:
                sct.pri('WARN: Costumes tag empty in "' + x['objName'] + '"')
                j['children'][listIndex]['costumes'].append({"costumeName": "costume-1", "baseLayerID": -1,"baseLayerMD5": "cd21514d0531fdffb22204e0ec5ed84a.svg","bitmapResolution": 1,"rotationCenterX": 240,"rotationCenterY": 180})
            internalListIndex = 0
            for y in x['costumes']:
                pri(x['objName'] + ' > [c]' + y['costumeName'])
                assets.append({'id':imgCount,'md5':y['baseLayerMD5'],'route':{'node':'children','spriteIndex':listIndex,'assetType':'costumes','assetIndex':internalListIndex},'type':'imageLayer','display':x['objName'] + ' > ☼' + y['costumeName']})
                imgCount = imgCount + 1
                if 'textLayerID' in y:
                    assets.append({'id':imgCount,'md5':y['textLayerMD5'],'route':{'node':'children','spriteIndex':listIndex,'assetType':'costumes','assetIndex':internalListIndex},'type':'textLayer', 'display':x['objName'] + ' > ☼' + y['costumeName'] + '/Old-1.4textLayer'})
                    imgCount = imgCount + 1
                internalListIndex = internalListIndex + 1
            if 'sounds' in x:
                internalListIndex = 0
                for y in x['sounds']:
                    pri(x['objName'] + ' > [s]' + y['soundName'])
                    assets.append({'id':sfxCount,'md5':y['md5'],'route':{'node':'children','spriteIndex':listIndex,'assetType':'sounds','assetIndex':internalListIndex},'type':'sound','display':x['objName'] + ' > ♫' + y['soundName']})
                    internalListIndex = internalListIndex + 1
                    sfxCount = sfxCount + 1
        count = 0
        for x in assets:
            status = processAsset(x['id'],x['md5'],x['route'],x['type'],x['display'])
            if not status['success']:
                if status['statusCode'] == -1:
                    e = status['err']
                    x = traceback.format_exception(type(e), e, e.__traceback__)
                    tb = '\n'.join(x)
                else:
                    tb = ''
                if x['type'] == 'imageLayer':
                    pri('Failed to download ' + str(x['display']) + ': ' + str(status['statusCode']) + ' (' + str(x['md5']) + ') ' + str(tb) + 'Missing? Replacing with blank svg.')
                    stat = processAssetContent(x['id'],blank_svg,x['route'],x['type'],'.svg')
                elif x['type'] == 'textLayer':
                    pri('Failed to download ' + str(x['display']) + ': ' + str(status['statusCode']) + ' (' + str(x['md5']) + ') ' + str(tb) + 'Missing? Replacing with blank png.')
                    stat = processAsset(x['id'],'d36f6603ec293d2c2198d3ea05109fe0.png',x['route'],x['type'])
                else:
                    pri('Failed to download ' + str(x['display']) + ': ' + str(status['statusCode']) + ' (' + str(x['md5']) + ') ' + str(tb) + 'Missing? Replacing with blank wav.')
                    stat = processAsset(x['id'],'50dcf96f5dabc3941972f14ae6e3c103.wav',x['route'],x['type'])
                if not stat['success']:
                    return {'status':False, 'error':2, 'stack':False}
            count = count + 1


        zipf.writestr('project.json', json.dumps(j, indent=4).encode())
        zipf.close()
        f = path
        if os.path.splitext(f)[1] != '.sb2':
            f = f + '.sb2'
        fn = open(f, 'wb')
        fn.write(buf.getvalue())
        fn.close()
    except BaseException as e:
        return {'status':'error','error':'Internal function raised exception','stack':True,'code':111, 'errorID':e}
    else:
        return {'status':'success'}

def encodeStatus(sc):
    return int((100 - sc * 2 + 50) / 2)

def decodeStatus(sc):
    return int(sc - 75) + abs((-425.0 - 75) * 2)

if __name__ == "__main__":
    print(downloadProject(str(input('Enter project id: ')), 'project_' + str(random.randint(0, 10000000)) + '.sb2'))
    input()
