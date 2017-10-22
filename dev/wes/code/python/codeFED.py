#!/usr/bin/python3

#import packages
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
import shapefile as shp
import colormaps as cmaps



#parameters
figpath = '/home/wes/Personal/FED/2015/figs/'
rawdatapath = '/home/wes/Personal/FED/2015/rawdata/'
datapath = '/home/wes/Personal/FED/2015/data/'
shapefilepath = '/home/wes/Personal/FED/2015/shapefiles/'



#functions

def norm_dicvals(dic):
    """
    given a dictionary, will normalize the values
    returns a dictionary with normalized values
    """

    vals = [j for i,j in dic.items()]
    spread = max(vals) - min(vals)
    for key, val in dic.items():
        dic[key] = (val-min(vals)) / spread
    return dic




def mk_entropy():

    """
    read raw data and produce data for entropy by FED
    returns dictionary:
    key=FED ID; value=entropy
    """

    datafile = rawdatapath + 'FEDCandidateShares.csv'

    data = pd.read_csv(datafile, delimiter=",", skiprows=0, quotechar='"', usecols=(2,7))
    ids = [int(i) for i in data.T.ix[0]]
    vote = [float(i)/100 for i in data.T.ix[1]]
    data = [[i,j] for i,j in zip(ids,vote)]
    dic = {}
    idlist = list(set(ids))
    for idn in idlist:
        dic[idn] = -sum([i[1]*np.log(i[1]) for i in data if i[0]==idn])
    return dic



def mk_turnout():

    """
    read raw data and produce data for voter turnout by FED
    returns dictionary:
    key=FED ID; value=turnout (fraction)
    """

    datafile = rawdatapath + 'FEDResults.csv'

    data = pd.read_csv(datafile, delimiter=",", skiprows=0, quotechar='"', usecols=(2,11))

    ids = [int(i) for i in data.T.ix[0]]
    turnout = [float(i)/100 for i in data.T.ix[1]]
    data = [[i,j] for i,j in zip(ids,turnout)]
    dic = {}
    for i in data:
        dic[i[0]] = i[1]
    return dic



def mk_map(FED338dic, append, region='Canada'):

    """
    give it a dictionary of FED numbers and the data of interest
    give also a province or region (default is all of Canada)
    returns nothing, outputs PNG file.
    """


    nameconv = {'Canada' : ['AB', 'BC', 'SK', 'MB', 'ON', 'QC', 'NB', 'NS', 'NL', 'PE', 'YT', 'NT', 'NU'],
                'Alberta' : ['AB'],
                'BC' : ['BC'],
                'Manitoba' : ['MB'],
                'Saskatchewan' : ['SK'],
                'Ontario' : ['ON'],
                'Quebec' : 'QC',
                'Maritimes' : ['NB', 'NS', 'PE', 'NL']}

    dic = FED338dic
    shapefile = shapefilepath + region + '/' + region.lower() + '.shp'
    sf = shp.Reader(shapefile)
    records = []
    shapes = []
    idns = []
    for i,j in zip(sf.records(),sf.shapeRecords()):
        idns.append(str(i[1]))
        records.append(i)
        shapes.append(j)

    subdic = {}
    for rec,shape in zip(records,shapes):
        if rec[4] in nameconv[region]:
            subdic[rec[1]] = dic[rec[1]]
    mean = sum([i[1] for i in subdic.items()])/len(subdic)
    var = np.var([i[1] for i in subdic.items()])
    subdic = norm_dicvals(subdic)


    #set color bar
    cmap = cmaps.web
    Z = [[0,0],[0,0]]
    levels = list(np.linspace(0,1,100))
    CS3 = plt.contourf(Z, levels, cmap=cmap)
    plt.clf()

    fig = plt.figure()
    for rec,shape in zip(records,shapes):
        if rec[4] in nameconv[region]:
            if len(shape.shape.parts) == 1:
                x = [i[0] for i in shape.shape.points]
                y = [i[1] for i in shape.shape.points]
                plt.fill(x, y, lw=0.15, edgecolor='white', facecolor=cmap(subdic[rec[1]]))
            else:
                for index in range(len(shape.shape.parts)):
                    try:
                        x = [i[0] for i in shape.shape.points[shape.shape.parts[index]:shape.shape.parts[index+1]]]
                        y = [i[1] for i in shape.shape.points[shape.shape.parts[index]:shape.shape.parts[index+1]]]
                    except:
                        x = [i[0] for i in shape.shape.points[shape.shape.parts[index]:]]
                        y = [i[1] for i in shape.shape.points[shape.shape.parts[index]:]]
                    plt.fill(x, y, lw=0.15, edgecolor='white', facecolor=cmap(subdic[rec[1]]))
    plt.axis('off')
    plt.axis('equal')

    #fig.text(.65, .7, append + '\nRegion: ' + region + '\nAverage: ' + str(mean)[:4] + '\nVariation: ' + str(np.sqrt(var))[:4], fontsize=10, ha='left')
    #fig.text(.95,0.1, r'$\copyright$ Wes Kyle''\nwrkyle.com', ha='right', va='bottom', alpha=.2, fontsize=6)
    #cbar = plt.colorbar(CS3, ticks=[0.0,.5,1.0], orientation='horizontal', fraction=0.046, pad=0.04, shrink=.4)
    #cbar.set_ticklabels(['Low', 'Medium', 'High'])
    plt.savefig(figpath + region + '-' + append + '-title.png', dpi=1000, transparent=False)
        


def mk_corr(dic1, dic2):
    """
    takes two dictionaries holding districts and some data
    returns list of triples holding ID, dic1 data, and dic2 data
    """

    triples = []
    for i in dic1.items():
        for j in dic2.items():
            if i[0] == j[0]:
                triples.append([i[0], i[1], j[1]])
    return triples






dic1 = mk_entropy()
dic2 = mk_turnout()

#mk_map(dic1, 'Competitiveness', 'Canada')
#mk_map(dic2, 'Turnout', 'Maritimes')


#data = mk_corr(dic1,dic2)
#print(stats.pearsonr([i[1] for i in data], [i[2] for i in data]))

'''
plt.style.use('ggplot')
data = mk_corr(dic1,dic2)
plt.scatter([i[1] for i in data], [i[2] for i in data], facecolor='orangered', alpha=.7, s=70)
plt.xlabel('competitiveness', color='black')
plt.ylabel('voter turnout', color='black')
plt.xticks(color='black')
plt.yticks(color='black')
plt.savefig('correlation.png', dpi=1000)
'''
