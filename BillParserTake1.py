# -*- coding: utf-8 -*-
import requests, bs4, re, collections

class Bill_Import():
    def __init__(self):
        #needs input of str for bill number and a bool for issenate or ishouse
        self.bill_number = str
        self.issenate = True
        self.ishouse = False
        self.url = {'billurl' : ['http://www.capitol.state.tx.us/tlodocs/84R/billtext/html/','.htm'],
                    'sections' : ["http://www.capitol.state.tx.us/BillLookup/",".aspx?LegSess=84R&Bill="]}
        self.endchars = ["I", "S", "E", "H", "F"]
        self.endcharh = ["I", "H", "E", "S", "F"]
        self.rawauthors = 'string'        
        self.rawhistory = 'string'
        
        #outside vars
        self.billtext = collections.OrderedDict()
        self.subjects = list()
        self.authors = list()
        self.coauthors = list()
        self.cosponsors = list()
        self.sponsors = list()
        self.latestversion = str
    def set_bill_num(self, num):
        if not num.isalnum():
            print('error must be a number')
        else:
            self.bill_number = num
    def get_bill_num(self):
        return self.bill_number
    #function for setting if the bill is senate or house
    def set_sen_rep(self,sen,rep):
        if sen == rep:
            print('Bill must originate in either house or senate')
        elif sen:            
            self.issenate = True
        else:
            self.ishouse = True
    def pull_billtext(self):
        if self.issenate:
            chamber = 'SB'            
        else:
            chamber = 'HB'
        x = 0
        errorflag = True
        while errorflag: 
            path = self.url['billurl'][0]+  chamber + self.bill_number.zfill(5) + self.endchars[x] + self.url['billurl'][1]
            res = requests.get(path)
            errorflag = (res.status_code == requests.codes.ok)
            if not errorflag:
                print('break')    
                break
            self.billtext[self.endchars[x]] = res.text
            x += 1
        html = bs4.BeautifulSoup(self.billtext[next(reversed(self.billtext))])
        clean_text = html.get_text()
        period=clean_text.split('.')
        index=len(period)-1
        #print(index)
        span_list=[]
        i=0
        id=1
        while i<= index:
            string1=period[i].replace('\n'," ")
            string2=string1.replace('\t'," ")
            string12=string2.replace('\xa0'," ")
            string3=string12.replace('\r'," ")
            #print(string3 + ' END')
            span='<span id="' + str(id) + '">' + string3+'</span>'
        
            span_list.append(span)
        
            span='<span>'+string3+'</span>'
        
            span_list.append(span)
            i+=1
            id+=1
        stringtext = ''.join(span_list)
        self.billtext[next(reversed(self.billtext))] = stringtext
    def pull_history(self):
        if self.issenate:
            chamber = 'SB'            
        else:
            chamber = 'HB'
        path = self.url['sections'][0]+'History'+self.url['sections'][1]+chamber+self.bill_number
        rawhtml = requests.get(path)
        bhistory = bs4.BeautifulSoup(rawhtml.text)
        self.rawhistory = bhistory
        
    def set_subjects(self):
        td = self.rawhistory.find('td', {'id': 'cellSubjects'}).getText()
        regex = re.compile(".*?\((.*?)\)")
        # Find all the strings between (...) - parenthesis
        result = re.findall(regex, td)
        
        # Delete the content between the parenthesis
        for par in result:
          td = td.replace(par, "")
        
        subjects_list = td.split("()")
        # Skip last element (it's an empty string anyway)
        subjects_list = subjects_list[:len(subjects_list)-1]
        self.subjects = subjects_list
        
    def set_data(self):
        list_var = {self.authors:'cellAuthors',self.coauthors:'cellCoauthors',self.cosponsors:'cellCosponsors',self.sponsors:'cellSponsors'}
        for k,v in list_var:
            td = dict(key).find('td', {'id': #value})
            if type(td) == str:
                td= td.getText()
                 = list(td.split('|')) 
            else:
                self.coauthors =' '
    def set_sponsors(self):
        td = self.rawhistory.find('td', {'id': 'cellSponsors'}).getText()
        self.sponsors = list(td.split('|'))
    def set_cosponsors(self):
        td = self.rawhistory.find('td', {'id': 'cellCosponsors'}).getText()
        self.cosponsors = list(td.split('|'))        


billsb10 = Bill_Import()
billsb10.set_bill_num('14')
billsb10.pull_billtext()
billsb10.pull_history()
billsb10.set_authors()
billsb10.set_coauthors()
billsb10.set_subjects()
billsb10.set_cosponsors()
billsb10.set_sponsors()
print(billsb10.authors)
print(billsb10.subjects)
print(billsb10.coauthors)
print(billsb10.sponsors)
print(billsb10.cosponsors)

#to access the latest version of a bill
val = list(billsb10.billtext.values())
print(val[-1])