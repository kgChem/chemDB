#!/C:/Python27/python.exe

import os
import requests
import xml.etree.ElementTree as ET

class PUGif(object):
    """A class for interaction with the PubChem PUG server"""    
    def __init__(self):
        self.host ="http://pubchem.ncbi.nlm.nih.gov/pug/pug.cgi"
        self.status="unsubmitted"
        self.response=None #an xml.etree.ElementTree
        self.url=None
        self.reqID=None
        self.poll=None

    def __str__(self):
        return("--->Connection to the Pubchem PUG server. Query status = {0}".format(self.status))

    def sendQuery(self,queryXML):
        req = requests.post(self.host,data=queryXML)
        self.status = "submitted"
        self.response = ET.fromstring(req.text)

    def _parseReply(self):
        root = self.response.getroot()
        for child in root.iter("PCT-Download-URL_url"):
            self.url = child.text
        self.status="done"
        if (self.url == None): #If request not done
            for child in root.iter("PCT-Waiting_reqid"):           
               self.reqID = child.text
            self.status="waiting"
  
    def pollServer(self):
        if self.status == "waiting":
            if self.poll == None:
                self.poll = self._buildPoll(self.reqID)
            req = requests.post(self.host,data = poll)
            self.response = ET.fromstring(req.txt)
            self._parseReply()
            
    def _buildPoll(requestID):
        top = ET.Element('PCT-Data')
        L1 = ET.SubElement(top,'PCT-Data_input')
        L2 = ET.SubElement(L1, 'PCT-InputData')
        L3 = ET.SubElement(L2,'PCT-InputData_request')
        L4 = ET.SubElement(L3,'PCT-Request')
        L5 = ET.SubElement(L4, 'PCT-Request_reqid')
        L5.text = requestID
        L5a = ET.SubElement(L4, 'PCT-Request_type',{"value":"status"})
        return(top)
   
# Build an XML query string for a download by PubChem CID
# See https://pubchem.ncbi.nlm.nih.gov/pug/pughelp.html for requirements
def buildDQuery(CID,fileType,compress):
    top = ET.Element('PCT-Data')
    L1 = ET.SubElement(top,'PCT-Data_input')
    L2 = ET.SubElement(L1,'PCT-InputData')
    L3 = ET.SubElement(L2,'PCT-InputData_download')
    L4 = ET.SubElement(L3,'PCT-Download')
    L5 = ET.SubElement(L4,'PCT-Download_uids')
    L6 = ET.SubElement(L5,'PCT-QueryUids')
    L7 = ET.SubElement(L6, 'PCT-QueryUids_ids')
    L8 = ET.SubElement(L7,'PCT-ID-List')
    L9 = ET.SubElement(L8, 'PCT-ID-List_db')
    L9.text = "pccompound"
    L9a = ET.SubElement(L8,'PCT-ID-List_uids')
    for uid in CID:
        L10 = ET.SubElement(L9a,"PCT-ID-List_uids_E")
        L10.text = uid
    L5a = ET.SubElement(L4,"PCT-Download_format",{'value':fileType})
    L5b = ET.SubElement(L4,"PCT-Download_compression",{'value':compress})
    return(ET.tostring(top))

#Testing code below
print('=> Making Query')
testq1 = buildDQuery(['1','99'],"sdf","gzip")
print(testq1)
print('~'*50)
print('==> Contacting Server')
testcon1 = PUGif()
print(testcon1)
testcon1.sendQuery(testq1)
print('*** Sent to server. Got this reply ***')
print(ET.tostring(testcon1.response,'utf-8'))
#print('*** *** Polling server for status *** ***')
#testcon1.pollServer()
#print('*** *** Server response *** ***')
#testcon1.response
#print(testcon1)


