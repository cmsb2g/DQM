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

parser.add_option('--addlabel', metavar='F', type='string', action='append',
                  dest='labels',
                  help='List of labels for input files')

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

globallabel = options.coll + '_' + options.labels[0] + '_vs_' + options.labels[1]
htmlout = file( globallabel + '.html', 'w' )

htmlbuffer = \
    "<html>\n" + \
    "<head>\n" + \
    "<title>{0:s} versus {1:s}</title>\n" + \
    "<table border=1>\n".format( options.labels[0], options.labels[1] )
htmlout.write( htmlbuffer)


hists = []
canvs = []
legs = []
icanv = 0
tableline = ""
for hist in histsToPlot :
    canv = ROOT.TCanvas('c' + str(icanv), 'c' + str(icanv))
    index = 0
    leg = ROOT.TLegend( 0.5, 0.87, 0.9, 1.0 )
    leg.SetFillColor(0)
    for ifile in range(len(files)) :
        tfile = files[ifile]
        s =  options.dir + '/' + options.coll + '/' +  hist
        print 'getting ' + s
        h = tfile.Get( s )
        h.SetLineColor( colors[index] )
        h.Sumw2()
        if h.Integral() > 0 : 
            h.Scale(1.0 / h.Integral() )
        hists.append(h)
        if ifile == 0 :
            h.Draw('hist')
        else :
            h.Draw('hist same')
        index += 1
        leg.AddEntry( h, options.labels[ifile], 'l') 
    icanv += 1
    legs.append( leg )
    leg.Draw()
    canvs.append(canv)
    histname = globallabel + '_' + hist
    canv.Print(  histname + '.png')
    canv.Print(  histname + '.pdf')
    tableline = "<tr>  <a href=\"" + histname + ".pdf\"> <img src = \"" + histname + '.png' + "\" alt=\"" + histname + ".pdf\"> \n"
    htmlout.write( tableline )

htmlbuffer = \
    "</table>\n" + \
    "</head>\n" + \
    "</html>\n"
htmlout.write( htmlbuffer)

htmlout.close()
