#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import csv
from core import *
import glob, os

class Change():
    def __init__(self, dependency, change, link):
        self.dependency = dependency
        self.change = change
        self.evolution = -1
        self.link = link

    def setEvolution(self, evolution):
        self.evolution = evolution

    def getEvolution(self):
        return self.evolution

    def getChanges(self):
        return self.change

    def getDependency(self):
        return self.dependency
    
    def getLink(self):
        return self.link

    def getDependencyIdentifier(self):
        a , b = self.dependency.getVariabilities()
        return a+" <<-->> "+b

class Impact():
    def __init__(self, change):
        self.change = change
        self.affectedvariability = None
        self.modifiedVariability = None
        self.setAffectedVariability()

    def setAffectedVariability(self):
        a, b = self.change.getDependency().getVariabilities()
        self.modifiedVariability = a
        self.affectedvariability = b

    def getAffectVariability(self):
        return self.affectedvariability

    def setProgramElementAffected(self):
        pass




class Parser():
    def __init__(self, line):
        self.callee = {'name':"", 'category':"",'type':"",'qualifier':"",'modifier':"", 'specifier':"",'parameters':0}
        self.caller = {'name':"", 'category':"",'type':"",'qualifier':"",'modifier':"", 'specifier':"",'parameters':0}
        self.link = {}
        self.line = line
        self.indexAct = 0
        self.parserLink()
        self.status
    
    def parserLink(self):
        if self.line[0] == '0':
            self.status = "persistent"
            self.parserCategory()

        if self.line[0] == '1':
            self.status = "new"
            self.parserCategory()

        if self.line[0] == '2':
            self.status = "dead"
            self.parserCategory()

    def parserFunction(self, startAt, parameters):
        for i in range (0, ((parameters*5) + 1)):
            index = startAt + i
        self.indexAct = index+1
        

    def parserVariable(self, startAt):
        print (self.line[startAt])

    def parserCategory(self):
        #qualificador, especificador, modificador, tipo, nome
        if self.line[1] == 'function':
            
            #caller
            self.caller['qualifier'] = self.line[2]
            self.caller['especifier'] = self.line[3]
            self.caller['modifier'] = self.line[4]
            self.caller['type'] = self.line[5]
            self.caller['name'] = self.line[6]
            self.caller['category'] = 'function'
            parameters = int (self.line[7])
            self.parserFunction(8, parameters)
            #index = (parameters * 5) + 1 + 8
        
            #calle

            print(self.indexAct)
            try:
                if self.line[self.indexAct] == 'function':
                    self.callee['qualifier'] = self.line[self.indexAct+1]
                    self.callee['specifier'] = self.line[self.indexAct+2]
                    self.callee['modifier'] = self.line[self.indexAct+3]
                    self.callee['type'] = self.line[self.indexAct+4]
                    self.callee['name'] = self.line[self.indexAct+5]
                    self.callee['category'] = 'function'

                if self.line[self.indexAct] == 'variable':
                    self.callee['qualifier'] = self.line[self.indexAct+1]
                    self.callee['specifier'] = self.line[self.indexAct+2]
                    self.callee['modifier'] = self.line[self.indexAct+3]
                    self.callee['type'] = self.line[self.indexAct+4]
                    self.callee['name'] = self.line[self.indexAct+5]
                    self.callee['category'] = 'variable'
                    #self.parserVariable(self.indexAct)

                self.indexAct = self.indexAct + 6
            except:
                pass

        if self.line[1] == 'variable':
            self.caller['qualifier'] = self.line[2]
            self.caller['specifier'] = self.line[3]
            self.caller['modifier'] = self.line[4]
            self.caller['type'] = self.line[5]
            self.caller['name'] = self.line[6]
            self.caller['category'] = 'variable'
            self.parserVariable(2)

            self.indexAct = 7

            #calle

            print(self.indexAct)
            try:
                if self.line[self.indexAct] == 'function':
                    self.callee['qualifier'] = self.line[self.indexAct+1]
                    self.callee['especifier'] = self.line[self.indexAct+2]
                    self.callee['modifier'] = self.line[self.indexAct+3]
                    self.callee['type'] = self.line[self.indexAct+4]
                    self.callee['name'] = self.line[self.indexAct+5]
                    self.callee['category'] = 'function'

                if self.line[self.indexAct] == 'variable':
                    self.callee['qualifier'] = self.line[self.indexAct+1]
                    self.callee['especifier'] = self.line[self.indexAct+2]
                    self.callee['modifier'] = self.line[self.indexAct+3]
                    self.callee['type'] = self.line[self.indexAct+4]
                    self.callee['name'] = self.line[self.indexAct+5]
                    self.callee['category'] = 'variable'
                    #self.parserVariable(self.indexAct)

                self.indexAct = self.indexAct + 6
            except:
                pass

    def getLink(self):
        self.link['callee'] = self.callee
        self.link['caller'] = self.caller
        self.link['status'] = self.status
        return self.link






def readFile():
    ROOT = os.getcwd()
    os.chdir(ROOT+'/csv/permanents')

    project = Project()

    for file in glob.glob("*.csv"):
        version = Version()
        print(file)
        reader = open(file, "r")

        i = 0
        dp = False
        lastDependency =  None
        dependencie = None
        for point in reader:
            line = point.split(',')
            if i == 0:
                print ("Analise ", line[0],"De ", line[1], "Variabilidades: ", line[2] )
                version.setVersion(line[0])
                version.setVariabilitiesNumber(line[2])
            else:
                #print (linha)
                if "Dependency" in line:
                    if (dp):
                        version.addPermanentDependency(lastDependency)
                    dependencie = Dependency(line[1], line[2])
                    print(dependencie.getVariabilities())
                    dp = True
                else:
                    #print ("last Dependency ", dependencie.getVariabilities())
                    print (line)
                    parser = Parser(line)
                    link = parser.getLink()
                    print("Link status ", link['status'])
                    if link['status'] == 'persistent':
                        dependencie.addPersistentLink(link)
                    if link['status'] == 'dead':
                        dependencie.addDeadLinks(link)
                    if link['status'] == 'new':
                        dependencie.addNewLink(link)

                    print("links ", len(dependencie.getPersistentLink()))
                lastDependency = dependencie
                    

                
            i+=1
        project.addVersion(version, i)

    processProject(project)

def matchDependency(depA, depB):
    variability1A, variability2A = depA.getVariabilities()
    variability1B, variability2B = depB.getVariabilities()
    if (variability1A == variability1B and variability2A == variability2B):
        return True
    else:
        return False

def matchLink(link1, link2):
    if ((link1['callee']['name'] == link2['callee']['name']) and (link1['caller']['name'] == link2['caller']['name'])):
        return True
    else:
        return False

def processProject(project):

    	
    allVersions = project.getVersion()
    listChanges = list()
    for i in range (0, len(allVersions) - 1):
        change = {'tipo':0, 'qtdFunction':0, 'qtdVariable':0, 'return':0, 'Fqualificador':0, 'Fespecificador':0, 'Fmodificador':0,  'Vqualificador':0, 'Vespecificador':0, 'Vmodificador':0, 'callee':0, 'caller':0, 'function':0, 'variable':0, 'Frmv':0 ,'Vrmv':0,'Fadc':0,'Vadc':0, 'parametros':0 }
        for dp0 in allVersions[i].getPermanentDependency():
            for dp1 in allVersions[i+1].getPermanentDependency():
                if(matchDependency(dp0, dp1)):
                    for link0 in dp0.getPersistentLink():
                        for link1 in dp1.getPersistentLink():
                            if (matchLink(link0, link1)):
                                if (compareChanges(link0, link1, change)):
                                    saveChanges = Change(dp1, change, link1)
                                    searchImpact(link0, link1, change)#if contains change, so search for possible impacts
                                    saveChanges.setEvolution(i)
                                    listChanges.append(saveChanges)

    print(len(listChanges))

    with open("FineGrainedDependenciesChangesReport.csv", "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for ch in listChanges:
            change = ch.getChanges()
            ev = str(ch.getEvolution())
            print(ev)
            writer.writerow([ch.getEvolution(), ch.getDependencyIdentifier(), change['function'], change['variable'] , change['Vmodificador'], change['Vespecificador'], change['Vqualificador'], change['tipo'], change['return'],change['Fmodificador'], change['Fespecificador'], change['Fqualificador'], change['parametros']])
  
def compareCaller(link1, link2):
    r = False
    if (link1['caller']['parameters'] != link2['caller']['parameters']):
        r = True
    if (link1['caller']['type'] != link2['caller']['type']):
        r = True
    if (link1['caller']['qualifier'] != link2['caller']['qualifier']):
        r = True
    if (link1['caller']['specifier'] != link2['caller']['specifier']):
        r = True
    if (link1['caller']['modifier'] != link2['caller']['modifier']):
        r = True
        
    return r


def searchImpact(link1, link2, change):
    print ("search impacts")
    if (compareCaller(link1, link2)):
        saveImpact = Impact(change)
        print ("impact at ", link2['caller'])

def compareChanges(link1, link2, change):
	r = False
	if (link1['callee']['parameters'] != link2['callee']['parameters']):
		change['parameters'] +=1
		if link1['callee']['category'] == "function":
			change['function'] += 1
		change['callee'] += 1
		r = True

	if (link1['callee']['type'] != link2['callee']['type']):
		if link1['callee']['category'] == "function":
			change['function'] += 1
			change['return'] += 1
		if link1['callee']['category'] == "variable":
			change['variable'] += 1
			change['type'] +=1
		change['callee'] += 1
		r = True
	if (link1['callee']['qualifier'] != link2['callee']['qualifier']):
		change['callee'] += 1
		if link1['callee']['category'] == "function":
			change['Fqualificador'] +=1
			change['function'] += 1
		if link1['callee']['category'] == "variable":
			change['Vqualificador'] +=1
			change['variable'] += 1
		r = True
	if (link1['callee']['specifier'] != link2['callee']['specifier']):
		change['callee'] += 1
		if link1['callee']['category'] == "function":
			change['Fespecificador'] +=1
			change['function'] += 1
		if link1['callee']['category'] == "variable":
			change['Vespecificador'] +=1
			change['variable'] += 1
		r = True
	if (link1['callee']['modifier'] != link2['callee']['modifier']):
		change['callee'] += 1
		if link1['callee']['category'] == "function":
			change['Fmodificador'] +=1
			change['function'] += 1
		if link1['callee']['category'] == "variable":
			change['Vmodificador'] +=1
			change['variable'] += 1
		r = True

	return r


def main():
    readFile()
    #readDead()

if __name__ == '__main__':
    main()