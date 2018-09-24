#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import csv
from core import *
from pdps import Parser
import glob, os


def readDead():
    ROOT = os.getcwd()
    os.chdir(ROOT+'/csv/deads/')

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
            print(">>>>> i == ", i)
            if i == 0:
                print ("Analise ", line[0],"DEPENDENCIAS MORTAS", line[1], "Variabilidades: ", line[2] )
                version.setVersion(line[0])
                version.setVariabilitiesNumber(line[2])
                version.setDeadDependencies(line[1])
            if i > 0:
                if ( int(version.getDeadDependencies()) > 0):
                    #print (linha)
                    print("<<<<< i == ", i)
                    if "Dependency" in line:
                        if (dp):
                            version.addDeadDependency(lastDependency)
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

                    lastDependency = dependencie
            i+=1
            project.addVersion(version, i)

    process(project)


def process(project):
    allVersions = project.getVersion()
    analyzedLinks = list()   
    with open("DeadDependenciesReport.csv", "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for i in range (0, len(allVersions) - 1):
            for dp in allVersions[i].getDeadDependency():
                for link in dp.getDeadLinks():
                    print("PROJETC PROCESS >>>")
                    print (link)
                    if (matchRepeat(link, analyzedLinks)):
                        analyzedLinks.append(link)
                        writer.writerow([i, dp.getVariabilities(), link['callee']['name'], link['callee']['category']])


def matchRepeat(link, links):
    for lk in links:
        if link['callee']['name'] == lk['callee']['name']:
            return False

    return True
def main():
    #readFile()
    readDead()

if __name__ == '__main__':
    main()