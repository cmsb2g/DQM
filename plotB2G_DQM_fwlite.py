#! /usr/bin/env python
import os
import glob
import time
import math

from optparse import OptionParser


parser = OptionParser()


parser.add_option('--addfile', metavar='F', type='string', action='append',
                  dest='files',
                  help='List of input files')

parser.add_option('--dir', metavar='F', type='string', action='store',
                  dest='dir',
                  default="DQMData/Run 1/Physics/Run summary/B2G",
                  help='Directory of B2G DQM module')

parser.add_option('--coll', metavar='F', type='string', action='store',
                  dest='coll',
                  default="cmsTopTagPFJetsCHS",
                  help='Collection to plot. Options are ak5PFJets, ak5PFJetsCHS, ca8PFJetsCHS, ca8PFJetsCHSPruned, cmsTopTagPFJetsCHS')
(options, args) = parser.parse_args()

argv = []


import ROOT
ROOT.gROOT.Macro("rootlogon.C")

files = []
for ifile in options.files :
    files.append( ROOT.TFile(ifile) )

colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen + 100 ]
histsToPlot = [
    'boostedJet_massDrop',
    'boostedJet_minMass',
    'boostedJet_subjetM',
    'boostedJet_subjetN',
    'boostedJet_subjetPhi',
    'boostedJet_subjetPt',
    'boostedJet_subjetY',
    'pfJet_pt',
    'pfJet_y',
    'pfJet_phi',
    'pfJet_m',
    'pfJet_pfcemf',
    'pfJet_pfnemf',
    'pfJet_pfchef',
    'pfJet_pfnhef'
    ]

hists = []
canvs = []
icanv = 0
for hist in histsToPlot :
    canv = ROOT.TCanvas('c' + str(icanv), 'c' + str(icanv))
    index = 0
    for ifile in range(len(files)) :
        tfile = files[ifile]
        s =  options.dir + '/' + options.coll + '/' +  hist
        print 'getting ' + s
        h = tfile.Get( s )
        h.SetLineColor( colors[index] )
        hists.append(h)
        if ifile == 0 :
            h.Draw('hist')
        else :
            h.Draw('hist same')
        index += 1
    icanv += 1
    canvs.append(canv)
