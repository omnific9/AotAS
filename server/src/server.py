__author__ = 'James'
import select
import socket
import sys
import threading
import xml.etree.ElementTree as elementtree
from DatabaseOps import Dbclass
from string import Template


class Storyarc:
    def __init__(self):
        self.tree = None
        self.root = None
        self.replacetree = None
        self.addtree = None
        self.pagechain = []

        self.count = 0

        self.homework = None
        self.hwmotivation = None

        self.globalvars = {'hwnum': 0, 'curhw': 'none', 'prehw': 'success', 'curhwid': 0, 'prehwid': 0, 'curhwtypeid': 0, 'totalhwsuccess': 0, 'totalhwfailure': 0, 'username': 'Soldier A', 'usergender': 'male', 'loc': 'none', 'state': 'none', 'tonyending': 'dead', 'memoryrate':10}
        #curhw and prehw can be: 'none', 'ongoing', 'rejected', 'abandoned', 'fail', 'succeed'

        self.usedfiles = []
        self.newusedfiles = []

        # following are homework manipulations

        self.socmappings = {'pc':('conscious','dramatic','environment','social-lib'),
            'c':('conscious','dramatic','environment','social-lib','self-reev'),
            'p':('self-reev','self-lib','helping','counter'),
            'a':('self-lib','helping','counter','reinforce','stimulus'),
            'm':('helping','counter','reinforce','stimulus')}

        self.hwmappings = {'conscious':(1,2,3,4,5,6),'dramatic':(7,8,9,10,11),
            'environment':(12,13,14,15),'social-lib':(16,17,18,19,20),
            'self-reev':(21,22,23,24,25),'self-lib':(26,27,28,29,30,31,32),
            'helping':(33,34,35,36,37),'counter':(38,39,40,41,42),
            'reinforce':(43,44,45,46,47),'stimulus':(48,49,50,51,52)}

        self.motivation = {'consistency':1, 'socialproof':0, 'liking':0, 'authority':2, 'scarcity':1}

    def nextInteraction(self):
        dict = {}
        if 'interactionday' in self.globalvars:
            dict = {'interactionday':int(self.globalvars.get('interactionday'))+1}
        else:
            dict = {'interactionday':1}
        self.globalvars.update(dict)
        return self.globalvars.get('interactionday')

    def homeworkstore(self,filename):
        self.homework = elementtree.parse(file(filename + ".xml")).getroot()

    def motivationstore(self,filename):
        self.hwmotivation = elementtree.parse(file(filename + ".xml")).getroot()

    def findhomeworktoassign(self):
        self.hwcategory = self.socmappings.get(self.globalvars.get('soc'))
        i = 0
        while i>-1:
            if 'hwcategory' not in self.globalvars:
                self.updatevars('hwcategory',self.hwcategory[0])
                self.hwcandidates = self.hwmappings.get(self.hwcategory[i])
                # first find a homework not assigned yet
                for j in range(0,len(self.hwcandidates)):
                    if 'hw'+str(self.hwcandidates[j]) not in self.globalvars:
                        return self.hwcandidates[j]
                # if all homework has been assigned at least once, use abandoned homework assignments
                for j in range(0,len(self.hwcandidates)):
                    if self.globalvars.get('hw'+str(self.hwcandidates[j])) == 'ongoing' or self.globalvars.get('hw'+str(self.hwcandidates[j])) == 'abandoned':
                        return self.hwcandidates[j]
            elif self.hwcategory[i] == self.globalvars.get('hwcategory'):
                i += 1
                if i >= len(self.hwcategory):
                    i = 0
                self.updatevars('hwcategory',self.hwcategory[i])
                self.hwcandidates = self.hwmappings.get(self.hwcategory[i])
                # first find a homework not assigned yet
                for j in range(0,len(self.hwcandidates)):
                    if 'hw'+str(self.hwcandidates[j]) not in self.globalvars:
                        return self.hwcandidates[j]
                # if all homework has been assigned at least once, use abandoned homework assignments
                for j in range(0,len(self.hwcandidates)):
                    if self.globalvars.get('hw'+str(self.hwcandidates[j])) == 'ongoing' or self.globalvars.get('hw'+str(self.hwcandidates[j])) == 'abandoned':
                        return self.hwcandidates[j]
            else:
                i += 1
                if i >= len(self.hwcategory):
                    i = 0

    def assignhomework(self):
        if 'curhwtypeid' not in self.globalvars:
            return
        for hws in self.homework.findall('hw'):
            if int(hws.get('id')) == int(self.globalvars.get('curhwtypeid')):
                return hws.find('assign').text

    def preparehomework(self):
        index = self.findhomeworktoassign()
        for hws in self.homework.findall('hw'):
            if int(hws.get('id')) == index:
                self.updatevars('hw'+str(hws.get('id')),'ongoing')
                self.updatevars('curhw','ongoing')
                self.updatevars('curhwtypeid',index)

    def abandonhomework(self):
        for hws in self.homework.findall('hw'):
            if int(hws.get('id')) == self.globalvars.get('curhwtypeid'):
                print 'abandoned homework: '+hws.get('id')
                self.updatevars('hw'+str(hws.get('id')),'abandoned')
                self.updatevars('curhw','abandoned')

    def preparemotivation(self):
        maxkey = None
        for key in self.motivation:
            if not maxkey or self.motivation.get(key) > self.motivation.get(maxkey):
                maxkey = key
        for hwchar in self.hwmotivation.findall('char'):
            if hwchar.get('name') == self.globalvars.get('hwchar'):
                self.updatevars('curmotivation',self.edittext(hwchar.find(maxkey).text))
                self.updatevars('curmotivationtype',maxkey)

    def motivatehomework(self):
        return self.globalvars.get('curmotivation')

    def downgrademotivation(self):
        if 'curmotivationtype' in self.globalvars:
            motname = self.globalvars.get('curmotivationtype')
            motvalue = int(self.motivation.get(motname))-3
            motdict = {motname:motvalue}
            print motname
            print motvalue
            self.motivation.update(motdict)

    def upgrademotivation(self):
        if 'curmotivationtype' in self.globalvars:
            motname = self.globalvars.get('curmotivationtype')
            motvalue = int(self.motivation.get(motname))+1
            motdict = {motname:motvalue}
            print motname
            print motvalue
            self.motivation.update(motdict)

    def clearmotivation(self):
        self.globalvars.pop('curmotivation', None)

    def gethomeworkreporttext(self):
        for hw in self.homework.findall('hw'):
            if hw.get('id') == str(self.globalvars.get('curhwtypeid')):
                return hw.find('report').text

    def succeedhomework(self):
        curhwinvars = 'hw' + str(self.globalvars.get('curhwtypeid'))
        dict = {curhwinvars:'succeed'}
        self.globalvars.update(dict)

    def gethomeworksuccesstext(self):
        for hw in self.homework.findall('hw'):
            if hw.get('id') == str(self.globalvars.get('curhwtypeid')):
                return hw.find('success').text

    def failhomework(self):
        curhwinvars = 'hw' + str(self.globalvars.get('curhwtypeid'))
        dict = {curhwinvars:'fail'}
        self.globalvars.update(dict)

    def gethomeworkfailuretext(self):
        for hw in self.homework.findall('hw'):
            if hw.get('id') == str(self.globalvars.get('curhwtypeid')):
                return hw.find('failure').text

    def gethomeworkbenefitsuccesstext(self):
        for hw in self.homework.findall('hw'):
            if hw.get('id') == str(self.globalvars.get('curhwtypeid')):
                return hw.find('benefitsuccess').text

    def gethomeworkbenefitfailuretext(self):
        for hw in self.homework.findall('hw'):
            if hw.get('id') == str(self.globalvars.get('curhwtypeid')):
                return hw.find('benefitfailure').text

    def curhwsuccess(self):
        self.updatevars('prehwid',self.globalvars.get('curhwid'))
        self.updatevars('curhwid',0)
        self.updatevars('prehw','success')
        self.updatevars('totalhwsuccess',self.globalvars.get('totalhwsuccess')+1)
        self.updatevars('curhwid',self.globalvars.get('curhwid')+1)
        if 'curmotive' in self.globalvars:
            dict = {self.globalvars.get('curmotive'): self.motivation.get(self.globalvars.get('curmotive'))+1}
            self.motivation.update(dict)
            del self.globalvars['curmotive']

    def curhwfailure(self):
        self.updatevars('prehwid',self.globalvars.get('curhwid'))
        self.updatevars('curhwid',0)
        self.updatevars('prehw','failure')
        self.updatevars('totalhwfailure',self.globalvars.get('totalhwsuccess')+1)
        self.updatevars('curhwid',self.globalvars.get('curhwid')+1)
        if 'curmotive' in self.globalvars:
            dict = {self.globalvars.get('curmotive'): self.motivation.get(self.globalvars.get('curmotive'))-1}
            self.motivation.update(dict)
            del self.globalvars['curmotive']

    def memoryinc(self):
        memoryrate = 10
        if 'memoryrate' in self.globalvars:
            memoryrate = int(self.globalvars.get('memoryrate'))
        memoryrate = memoryrate + 1
        self.updatevars('memoryrate', memoryrate)

    # following are detailed text manipulations

    def edittext(self,sentence):
        sentence = Template(sentence).substitute(hwassign=self.assignhomework(), hwmotivate=self.motivatehomework(), hwreport=self.gethomeworkreporttext(),
            hwsuccess=self.gethomeworksuccesstext(), hwfailure=self.gethomeworkfailuretext(), getusername=self.getusername(), heorshe=self.getsubject(), himorher=self.getobject(),
            hisorher=self.getpossessive(), hisorhers=self.getpossessivepronoun(), manorwoman=self.getnoun(), guyorgal=self.getnouncasual(), boyorgirl=self.getnounyoung(), sirormaam=self.getpolite(),
            connphrase=self.getConnectionPhrase(), hwbenefitsuccess=self.gethomeworkbenefitsuccesstext(), hwbenefitfailure=self.gethomeworkbenefitfailuretext())
        return sentence

    def getusername(self):
        return self.globalvars.get('username')

    def getsubject(self):
        if self.globalvars.get('usergender') == 'male':
            return 'he'
        return 'she'

    def getobject(self):
        if self.globalvars.get('usergender') == 'male':
            return 'him'
        return 'her'

    def getpossessive(self):
        if self.globalvars.get('usergender') == 'male':
            return 'his'
        return 'her'

    def getpossessivepronoun(self):
        if self.globalvars.get('usergender') == 'male':
            return 'his'
        return 'hers'

    def getnoun(self):
        if self.globalvars.get('usergender') == 'male':
            return 'man'
        return 'woman'

    def getnouncasual(self):
        if self.globalvars.get('usergender') == 'male':
            return 'guy'
        return 'gal'

    def getnounyoung(self):
        if self.globalvars.get('usergender') == 'male':
            return 'boy'
        return 'girl'

    def getpolite(self):
        if self.globalvars.get('usergender') == 'male':
            return 'Sir'
        return 'Ma\'am'

    def getConnectionPhrase(self):
        if 'connphrase' in self.globalvars:
            return self.globalvars.get('connphrase')
        return ''

    # following are page manipulations


    def naivestory(self,filename):
        self.tree = elementtree.parse(file(filename + ".xml"))
        self.root = self.tree.getroot()

    def pagesforreplace(self,filename):
        self.replacetree = elementtree.parse(file(filename + ".xml")).getroot()


    def pagesforadd(self,filename):
        self.addtree = elementtree.parse(file(filename + ".xml")).getroot()


    def shapechain(self):
        self.pagechain = []
        for child in self.root:
            self.pagechain.append(child)

    def firstfile(self):
        print 'this is run.'
        if not self.pagechain:
            return None
        filecode = self.pagechain[0].get('name')
        self.usedfiles.append(filecode)
        self.newusedfiles.append(filecode)
        return filecode

    def nextfile(self):
        self.pagechain.pop(0)
        self.root.remove(self.root[0])
        if not self.pagechain:
            return None
        filecode = self.pagechain[0].get('name')
        self.usedfiles.append(filecode)
        self.newusedfiles.append(filecode)
        if self.pagechain[0].find('change') is not None:
            for changevar in self.pagechain[0].findall('change'):
                for name in changevar.attrib:
                    self.updatevars(name, changevar.get(name))
            self.updatestory()
        return filecode


    def updatevars(self, key, val):
        if key in self.globalvars:
            if not isinstance(val,int) and val.isdigit():
                val = int(val)
        dict = {key: val}
        self.globalvars.update(dict)


    def updatestory(self):
        if self.findconflict():
            self.replacepages()
        self.addpages()
        self.shapechain()

    def initstory(self):
        self.shapechain()


    def findconflict(self):
        # index = 0
        # for files in self.tree.findall('file'):
        #     if index == 0:
        #         index += 1
        #         continue
        #     for key in self.globalvars.keys():
        #         for reqs in files.findall('req'):
        #             if reqs.get(key) and self.globalvars.get(key) != reqs.get(key):
        #                 return True
        #     index += 1
        ## this only concerns the immediate next file because it should only be triggered when a variable is changed and every placeholder succeeds a variable change.
        if len(self.root) < 2:
            return False
        for key in self.globalvars.keys():
            for reqs in self.root[1].findall('req'):
                if reqs.get(key) and self.globalvars.get(key) != reqs.get(key):
                    return True
        return False


    # def replacepages(self):
    #     index = 0
    #     for files in self.root.findall('file'):
    #         if index == 0:
    #             index += 1
    #             continue
    #         for req in files.findall('req'):
    #             for key in self.globalvars.keys():
    #                 if req.get(key) and req.get(key) != self.globalvars.get(key):
    #                     self.replacepagebyname(index, self.findreplacepage())
    #         index += 1
    #
    #
    # def replacepagebyname(self, index1, index2):
    #     self.root.remove(self.root[index1])
    #     if self.root.get('name') in self.usedfiles:
    #         self.usedfiles.remove(self.root.get('name'))
    #     if index2 > -1:
    #         self.root.insert(index1, self.replacetree[index2])
    #     elif index1>0 and 'ignore' in self.root[index1-1].attrib:
    #         self.root[index1-1].attrib.pop('ignore')

    def replacepages(self):
        cat = 'None'
        if self.root[1].find('type') is not None:
            cat = self.root[1].find('type').get('cat')
        index = self.findreplacepage(cat)
        if self.root[1].get('name') in self.usedfiles:
            self.usedfiles.remove(self.root[1].get('name'))
        self.root.remove(self.root[1])
        if index > -1:
            self.root.insert(1, self.replacetree[index])
        elif 'ignore' in self.root[0].attrib:
            self.root[0].attrib.pop('ignore')

    def findreplacepage(self, cat):
        index = 0
        for files in self.replacetree.findall('file'):
            found = True
            if files in self.usedfiles:
                found = False
            if cat != 'None':
                if files.find('type') is not None:
                    type = files.find('type')
                    if type.get('cat') != cat:
                        found = False
                else:
                    found = False
            for req in files.findall('req'):
                for key in req.attrib:
                    if str(self.globalvars.get(key)) != req.get(key):
                        found = False
            if found:
                return index
            index += 1
        return -1


    # def addpages(self):
    #     for files in self.addtree.findall('file'):
    #         if files.get('name') in self.usedfiles:
    #             continue
    #         addfile = True
    #         for f in self.root.findall('file'):
    #             if f.get('name') == files.get('name'):
    #                 addfile = False
    #         for req in files.findall('req'):
    #             for key in req.attrib:
    #                 if key == 'minhw':
    #                     if self.globalvars.get('hwnum') < int(req.get('minhw')):
    #                         addfile = False
    #                 elif key == 'maxhw':
    #                     if self.globalvars.get(key) > int(req.get('maxhw')):
    #                         addfile = False
    #                 elif key in self.globalvars:
    #                     if isinstance(self.globalvars.get(key), int):
    #                         if self.globalvars.get(key) != int(req.get(key)):
    #                             addfile = False
    #                     elif self.globalvars.get(key) != req.get(key):
    #                         addfile = False
    #         if addfile:
    #             self.addpage(files)
    #
    #
    # def addpage(self,files):
    #     insertpos = 0
    #     for f in self.root.findall('file'):
    #         insertpos += 1
    #         if files.find('type') is not None and f.find('follow') is not None:
    #             for f1 in files.findall('type'):
    #                 for f2 in f.findall('follow'):
    #                     if f1.get('cat') == f2.text:
    #                         if 'ignore' not in self.root[insertpos-1].attrib:
    #                             self.root.insert(insertpos, files)
    #                             self.root[insertpos-1].set('ignore','true')
    #                             return

    def addpages(self):
        f = self.root[0]
        if 'ignore' in self.root[0].attrib:
            return
        if f.find('follow') is None:
            return
        filetoadd = None
        priority = -1
        for files in self.addtree.findall('file'):
            print files.get('name')
            if files.get('name') in self.usedfiles:
                continue
            addfile = True
            fileFound = False
            for f in self.root.findall('file'):
                if f.get('name') == files.get('name'):
                    addfile = False
            # check that all requirements are met.
            for req in files.findall('req'):
                for key in req.attrib:
                    if key == 'minhw':
                        if self.globalvars.get('hwnum') < int(req.get('minhw')):
                            addfile = False
                    elif key == 'maxhw':
                        if self.globalvars.get(key) > int(req.get('maxhw')):
                            addfile = False
                    elif key in self.globalvars:
                        if isinstance(self.globalvars.get(key), int):
                            if self.globalvars.get(key) != int(req.get(key)):
                                addfile = False
                        elif self.globalvars.get(key) != req.get(key):
                            addfile = False
                    elif req.get(key) != '0':
                        addfile = False
            f = self.root[0]
            # each file to be added must have a type.
            if files.find('type') is None:
                continue
            # check for highest priority file to add.
            if addfile == True:
                for f1 in files.findall('type'):
                    for f2 in f.findall('follow'):
                        if f1.get('cat') == f2.text:
                            if f1.get('target') is not None:
                                if f1.get('target') in self.globalvars:
                                    if self.globalvars.get(f1.get('target')) > priority:
                                        priority = self.globalvars.get(f1.get('target'))
                                        filetoadd = files
                                    else:
                                        break
                                elif priority == -1:
                                    filetoadd = files
                            else:
                                fileFound = True
                                filetoadd = files
                if fileFound:
                    break
        if filetoadd is not None:
            self.root.insert(1, filetoadd)
            self.root[0].set('ignore','true')

class Server:
    def __init__(self):
        self.host = ''
        self.port = 8081
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []

    def open_socket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host,self.port))
            self.server.listen(5)
        except socket.error, (value,message):
            if self.server:
                self.server.close()
            print "Could not open socket: " + message
            sys.exit(1)

    def run(self):
        self.open_socket()
        input = [self.server]
        running = 1
        while running:
            inputready,outputready,exceptready = select.select(input,[],[])

            for s in inputready:

                if s == self.server:
                    # handle the server socket
                    c = Client(self.server.accept())
                    c.start()
                    self.threads.append(c)

                elif s == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = 0

        # close all threads

        self.server.close()
        for c in self.threads:
            c.join()

class Client(threading.Thread):
    def __init__(self,(client,address)):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.db = Dbclass()
        self.size = 1024
        self.storyproc = Storyarc()

    def run(self):
        running = 1
        try:
            while running:
                data = self.client.recv(self.size)
                if data:
                    datastr = repr(data).strip('\'').strip('\"')
                    print datastr
                    if datastr.startswith('firstfile'):
                        result = self.storyproc.firstfile()
                    elif datastr.startswith('nextfile'):
                        result = self.storyproc.nextfile()
                    elif datastr.startswith('updatevars'):
                        clientdata = datastr.split('##')
                        self.storyproc.updatevars(clientdata[1],clientdata[2])
                        result = 'done'
                    elif datastr.startswith('updatestory'):
                        self.storyproc.updatestory()
                        result = 'done'
                    elif datastr.startswith('edittext'):
                        clientdata = datastr.split('##')
                        result = self.storyproc.edittext(clientdata[1])
                    elif datastr.startswith('perform'):
                        clientdata = datastr.split('##')
                        funcstring = 'self.storyproc.'+clientdata[1]
                        exec(funcstring)
                    elif datastr.startswith('userid'):
                        clientdata = datastr.split('##')
                        if self.db.checkuserid(clientdata[1]) == 'FULL':
                            self.db.setuserid(clientdata[1])
                            self.storyproc.pagesforreplace('replace')
                            self.storyproc.pagesforadd('add')
                            self.storyproc.homeworkstore('homework')
                            self.storyproc.motivationstore('homework-motivate')
                            self.storyproc.usedfiles = self.db.getUsedFiles()
                            self.storyproc.globalvars = self.db.readGlobalvars()
                            self.storyproc.naivestory('day'+str(self.storyproc.nextInteraction()))
                            self.storyproc.initstory()
                            self.storyproc.motivation.update(self.db.readMotivations())
                            result = 'success'
                        elif self.db.checkuserid(clientdata[1]) == 'CONT':
                            self.db.setuserid(clientdata[1])
                            self.storyproc.pagesforreplace('cont-replace')
                            self.storyproc.pagesforadd('hwnl-add')
                            self.storyproc.homeworkstore('cont-homework')
                            self.storyproc.motivationstore('cont-homework-motivate')
                            self.storyproc.usedfiles = self.db.getUsedFiles()
                            self.storyproc.globalvars = self.db.readGlobalvars()
                            self.storyproc.naivestory('contday'+str(self.storyproc.nextInteraction()))
                            self.storyproc.initstory()
                            self.storyproc.motivation.update(self.db.readMotivations())
                            result = 'success'
                        elif self.db.checkuserid(clientdata[1]) == 'NONC':
                            self.db.setuserid(clientdata[1])
                            self.storyproc.pagesforreplace('hwnl-replace')
                            self.storyproc.pagesforadd('hwnl-add')
                            self.storyproc.homeworkstore('cont-homework')
                            self.storyproc.motivationstore('cont-homework-motivate')
                            self.storyproc.usedfiles = self.db.getUsedFiles()
                            self.storyproc.globalvars = self.db.readGlobalvars()
                            self.storyproc.naivestory('noncday'+str(self.storyproc.nextInteraction()))
                            self.storyproc.initstory()
                            self.storyproc.motivation.update(self.db.readMotivations())
                            result = 'success'
                        elif self.db.checkuserid(clientdata[1]) == 'HWNL':
                            self.db.setuserid(clientdata[1])
                            self.storyproc.pagesforreplace('hwnl-replace')
                            self.storyproc.pagesforadd('hwnl-add')
                            self.storyproc.homeworkstore('homework')
                            self.storyproc.motivationstore('homework-motivate')
                            self.storyproc.usedfiles = self.db.getUsedFiles()
                            self.storyproc.globalvars = self.db.readGlobalvars()
                            self.storyproc.naivestory('hwnlday'+str(self.storyproc.nextInteraction()))
                            self.storyproc.initstory()
                            self.storyproc.motivation.update(self.db.readMotivations())
                            result = 'success'
                        elif self.db.checkuserid(clientdata[1]) == 'tomorrow':
                            self.db.setuserid(clientdata[1])
                            self.storyproc.globalvars = self.db.readGlobalvars()
                            result = 'tomorrow'
                        else:
                            result = 'failure'
                    elif datastr.startswith('log'):
                        clientdata = datastr.split('##')
                        if clientdata[1] == 'game end':
                            self.db.setInteractionDay(self.storyproc.globalvars)
                        self.db.setLog(clientdata[1])
                    if result:
                        result = result.replace('\\t','\t')
                    else:
                        result = ' '
                    self.client.send(result.encode('ascii', 'ignore'))
                else:
                    self.client.close()
                    running = 0
                    self.db.writeGlobalvars(self.storyproc.globalvars)
                    self.db.writeMotivations(self.storyproc.motivation)
                    self.db.updateUsedFiles(self.storyproc.newusedfiles)
                    if self.db.checkuserid(self.db.user_id) != 'CONT' or self.storyproc.globalvars.get('prehw') != 'ongoing':
                        # if user is in Contingency and didn't finish homework, don't record this session.
                        self.db.updateLoginInfo()
        except socket.error as serr:
            print serr
            running = 0

if __name__ == "__main__":
    s = Server()
    s.run()