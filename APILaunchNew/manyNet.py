import requests
import json
import os
import time
from web3.contract import ContractEvent
from web3.contract import Contract
from web3._utils.events import get_event_data
from web3 import Web3
from web3.auto import w3
import functions as f
import parse_funs as parse
import networkChoose as choose
import grabAbi as grab
import guiNetAndAsk as guiNet
def isLs(ls):
    if type(ls) is list:
        return True
    return False
def chkGlobalExists(x):
    if x in globals():
        return True
    return False
def chkLocalExists(x):
    if x in locals():
        return True
    return False
def getSeconds():
    return time.time()
def homeIt():
    changeGlob('home',os.getcwd())
    slash = '//'
    if '//' not in str(home):
        slash = '/'
    changeGlob('slash',slash)
    return home,slash
def changeGlob(x,v):
    globals()[x] = v
def reqTimer():
    if chkGlobalExists('lastRequest') ==False:
        changeGlob('lastRequest',getSeconds())
    while (getSeconds()-lastRequest)<float(1/5):
        time.sleep(float(1/5) - (getSeconds()-lastRequest))
    return 
def stripWeb(x):
    if 'http' in x:
        x = x.replace('https','').replace('http','')
        while x[0] in [':',slash] and len(x)>1:
            x = x[1:]
    return x.split(slash)[0]
def getRPCNick(x):
    if 'http' in x:
        x = x.replace('https','').replace('http','')
        while x[0] in [':',slash] and len(x)>1:
            x = x[1:]
    return x.replace(slash,'_').replace('.','_')
def sites(A):
    U = [A]
    reqTimer()
    for url in U:
        X = str(U[0])
        r = requests.get(X)
        PS = r.text
        JS = json.loads(PS)['result']
        changeGlob('lastRequest',time.time())
    return JS
def apiKey(scanner):
    if scanner == 'bscscan.com':
        x = 'JYVRVFFC32H2ZSKDY1JZKNY7XV1Y5MCJHM'
    elif scanner == 'polygonscan.com':
        x = 'S6X6NY29X4ARWRVSIZJTG1PJS4IG86B3WJ'
    elif scanner == 'ftmscan.com':
        x = 'WU2C3NZAQC9QT299HU5BF7P8QCYX39W327'
    elif scanner == 'moonbeam.moonscan.io':
        x = '5WVKC1UGJ3JMWQZQAT8471ZXT3UJVFDF4N'
    else:
        x = '4VK8PEWQN4TU4T5AV5ZRZGGPFD52N2HTM1'
    return x
def checkSum(x):
    return w3.toChecksumAddress(x)
def getSource(add,scanner):
    try:
        result = sites('https://api.'+str(scanner)+'/api?module=contract&action=getsourcecode&address='+checkSum(str(add))+'&apikey='+str(apiKey(scanner)))
        return result
    except:
        try:
            result = sites('https://api-'+str(scanner)+'/api?module=contract&action=getsourcecode&address='+checkSum(str(add))+'&apikey='+str(apiKey(scanner)))
            return result
        except:

            return False
def getAbi(add):
    try:
        result = sites('https://api.'+str(scanner)+'/api?module=contract&action=getabi&address='+checkSum(str(add))+'&apikey='+str(apiKey(scanner)))
        return result
    except:
        return False
def getKeys(js):
    lsN = []
    for key, value in js.items():
        lsN.append(key)
    pen(lsN,'rpckeys.txt')
def tryCheckSum(x):
    try:
        y = w3.toChecksumAddress(x)
        return y
    except:
        return False
def checkIfDud(x):
    if  x != None:
        if len(x)>0:
            if len(x) >1:
                  return x
    return False
def eatX(x):
    if checkIfDud(x) != False:
        while x[-1] == slash and len(x)>1:
            x = x[:-1]
    return x
def eatY(y):
    if checkIfDud(y) != False:
        while y[0] == slash and len(y) >1:
            y[1:]
    return y
def createPath(x,y):
    return eatX(x)+'/'+eatY(y)
def ifNoInLsApp(ls,x):
    if x not in ls:
        ls.append(x)
    return ls
def ifNoInJSaddJs(js,x,y):
    if x not in js:
        js[x] = y
    return js
def derivePath():
    varFold = 'variables/'
    varisJs = f.jsIt(f.reader(createPath(varFold,'varis.json')))
    netNameFold = f.mkDirLs([createPath(varFold,networkName)])
    netWrkFold = f.mkDirLs([createPath(netNameFold,network)])
    chainIdFold = f.mkDirLs([createPath(netWrkFold,chainId)])
    addFold = f.mkDirLs([createPath(chainIdFold,add)])
    rpcShortFold = f.mkDirLs([createPath(addFold,getRPCNick(RPC))])
    varisJs['adds'] = ifNoInJSaddJs(varisJs['adds'],add,{'netNames':networkName,'chainId':chainId,'network':network,"rpcNick":getRPCNick(RPC),'path':rpcShortFold})
    f.pen(varisJs,createPath(varFold,'varis.json'))
    return rpcShortFold
def saveSoureces(add,sourceCode,rpc):
        changeGlob('networkName',rpc['networkName'])
        saveAllSources(sourceCode)
        js,funSheet = extractAllVars(add,{'path':derivePath(),'add':add,'name':sourceCode['ContractName'],'RPC':rpc})
        f.pen(js,createPath(derivePath(),'allCalls.json'))
        f.pen(funSheet,createPath(derivePath(),'funcSheet.py'))
        f.pen(jsInfo,createPath(derivePath(),'manyNet.pyjson'))
        return derivePath()
def extractRPCdata(js):
    global nativeCurrency,network,RPC,chainId,blockExplorer,scanner,w3
    kes = ['nativeCurrency', 'network', 'RPC', 'chainId', 'blockExplorer']
    for i in range(0,len(kes)):
        if kes[i] not in js:
            js[kes[i]] = ""
    changeGlob('nativeCurrency',js['nativeCurrency'])
    changeGlob('network',js['network'])
    changeGlob('blockExplorer',js['blockExplorer'])
    changeGlob('RPC',js['RPC'])
    changeGlob('chainId',js['chainId'])
    changeGlob('scanner',stripWeb(js['blockExplorer']))
    return nativeCurrency,network,RPC,chainId,blockExplorer,scanner,Web3(Web3.HTTPProvider(js['RPC']))
def extractAllVars(add,js):
    f.pen(js,createPath(derivePath(),'Info.json'))
    names = ['funs','asks','call','funAll','funSheet']
    parse.main = json.loads(str(js).replace("'",'"'))
    allVars = parse.parse_it(add,derivePath(),js['RPC'])
    for i in range(0,len(names)-1):
        js[names[i]] = allVars[i]
    return js,allVars[i+1]
def saveAllSources(sourceCode):
    sourceCodeKeys = ['SourceCode', 'ABI', 'ContractName', 'CompilerVersion', 'OptimizationUsed', 'Runs', 'ConstructorArguments', 'EVMVersion', 'Library', 'LicenseType', 'Proxy', 'Implementation', 'SwarmSource']
    for i in range(0,len(sourceCodeKeys)):
        f.pen(sourceCode[sourceCodeKeys[i]],createPath(derivePath(),sourceCodeKeys[i]+'.json'))
def addNet(js,network,rp):
    if network not in js:
        js['networks'][network] = {'RPC':[]}
        js['networks']['netNames'].append(network)
    js['networks'][network]['RPC'].append(rp)
    return js
def allNets():
    return choose.allNets()
def seeWhichIs():
    global nativeCurrency,network,RPC,chainId,blockExplorer,w3,add,pcNets
    pcNets = {'networks':{'netNames':[]}}
    nets = allNets()
    netNames = nets['names']
    for i in range(0,len(netNames)):
        nName = netNames[i]
        nNets = nets[nName]
        for k in range(0,len(nNets)):
            nativeCurrency,network,RPC,chainId,blockExplorer,scanner,w3 = extractRPCdata(nNets[k])
            if tryCheckSum(add) != False:
                try:
                   if len(info['ContractName'])>0:
                       print(info['ContractName'])  
                       pcNets = addNet(network,nNets[k])
                      
                except:
                    print('failes')
    f.pen(pcNets,createPath(derivePath(),'RPCs.txt'))
def deriveFrom(js):
    js = ifAnyNameInAll(js)
    return js['nativeCurrency'],js['network'],js['RPC'],js['chainId'],js['blockExplorer'],js['scanner'],Web3(Web3.HTTPProvider(js['RPC']))
def jsIt(x):
    return json.loads(str(x).replace("'",'"'))
def getAllSource(add):
    changeGlob('pcNets',{'networks':{'netNames':[]}})
    changeGlob('jsInfo',{'nativeCurrency': 'AVAX', 'network': 'Mainnet', 'RPC': 'https://api.avax.network/ext/bc/C/rpc', 'chainId': '43114', 'blockExplorer': 'https://snowtrace.io'})
    nativeCurrency,network,RPC,chainId,blockExplorer,scanner,w3 = extractRPCdata(jsInfo)
    changeGlob('add',add)
    pcNets = {'names':[],'contracts':{}}
    nets = allNets()
    netNames = nets['names']
    guiNet.loading('Network Identifier',0,len(netNames),netNames[0],'checking all available RPCs for SourceCode')
    for i in range(0,len(netNames)):
        nName = netNames[i]
        nNets = nets[nName]
        for k in range(0,len(nNets)):
            currNets = jsIt(nNets[k])
            nativeCurrency,network,RPC,chainId,blockExplorer,scanner,w3 = extractRPCdata(currNets)
            if tryCheckSum(add) != False:
                info = getSource(add,scanner)
                if info != False:
                    if isLs(info):
                        info = info[0]
                        contName = info['ContractName']
                    if contName != '':
                        changeGlob('info',info)
                        if 'networkName' not in currNets:
                            currNets['networkName'] = nName
                        if contName not in pcNets['contracts']:
                            pcNets['contracts'][contName] = {'RPCs':[],'SourceCode':[]}
                            pcNets['names'].append(contName)
                        if currNets not in pcNets['contracts'][contName]['RPCs']:
                            pcNets['contracts'][contName]['RPCs'].append(currNets)
                            pcNets['contracts'][contName]['SourceCode'].append(info)
        guiNet.loading('Network Identifier',i,len(netNames),netNames[i],'checking all available RPCs for SourceCode')
    return pcNets
def grabFromSource(source):
    addLen = len('38b3fc5b0858830f20147d9f55e227c018e81214')
    parser = f.reader(source).split('0x')
    for i in range(1,len(parser)):
        add = '0x' + parser[i][:addLen]
        pcNets = getAllSource(add)
        names = pcNets['names']
        for k in range(0,len(names)):
            RpCs = pcNets['contracts'][names[k]]['RPCs']
            source = pcNets['contracts'][names[k]]['SourceCode']
            for c in range(0,len(RpCs)):
                rpcN = RpCs[c]
                souN = source[c]
                changeGlob('networkName',rpcN['networkName'])
                saveSoureces(add,souN,rpcN)
homeIt()
global nativeCurrency,network,RPC,chainId,blockExplorer,scanner,w3
allNets()

#print(grabFromSource(getAllSource('0x8732E13e0A6E82Cffff9ED19661799Ffb0FA114e')))
