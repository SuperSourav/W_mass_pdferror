import ROOT
from array import array
from lib_pdf_error import *
########################################################################################

def main():
  ROOT.gROOT.SetBatch()
  f = ROOT.TFile('wemcPDF-hardProcess-WpT-cut6030.root', 'READ')
  hmT = f.Get('Wmt_pdf_data_fit')
  pdfgroup =  ["cteq6l1","CT10","CT10w","MSTW2008lo68cl","MSTW2008lo90cl","NNPDF30_lo_as_0118","MMHT2014lo68cl"]
  legdiffmTW = config('Legend_labels','diffmTW').split(",")
  legErr_ = config('Legend_labels','Err_').split(",")
  legMTWscalemap_ = config('Legend_labels','MTWscalemap_').split(",")
  legMTWscaleratiomap_ = config('Legend_labels','MTWscaleratiomap_').split(",")
  legMTWVariation_ = config('Legend_labels','MTWVariation_').split(",")
  legMTWvarmap_ = config('Legend_labels','MTWvarmap_').split(",")

  pdfcenter = [1, 2, 55, 108, 149, 190, 291, hmT.GetNbinsY()+1]
  R_var = [-2.7, 3.2]
  R_scal = [-0.15, 0.18]
  R_delMW = [-16, 20]
  
  mt_bins = hmT.GetNbinsX()
  
  h = []
  for g in range(len(pdfgroup)):
    h.append([])
    for i in range(pdfcenter[g], pdfcenter[g+1]):
      hh = ROOT.TH1F("mT_%s_%i"%(pdfgroup[g], (i-pdfcenter[g])),"mT_%s_%i"%(pdfgroup[g], (i-pdfcenter[g])), mt_bins, 60, 100)
      h[-1].append(hh)
  delMWfile = "PDFmWs-lowWindow60-fitType1-errorType1.txt"
  f1 = open(delMWfile, 'r')
  MW = f1.readlines()
  f1.close()
  DMW = []
  for g in range(len(h)):
    DMW.append([])
    for pdf in range(len(h[g])):
      if (pdf != 0): 
        DMW[-1].append(float(MW[pdfcenter[g] -1 + pdf]) - float(MW[pdfcenter[g] -1]))
      for mt in range(mt_bins):
        freq = hmT.GetBinContent(mt+1, (pdf+pdfcenter[g]))
        h[g][pdf].SetBinContent(mt+1, freq)
  
  gScale = []
  gVar = []
  gScaleVar = []
  gdelMWVar = []
  gdelMWScale = []
  MTWvarmapall_legend = []
  for g in range(1,len(h)):
    PDFscale = float(config('PDFSet_scales', pdfgroup[g]))
    MTWvarmapall_legend.append(legdiffmTW[g])
    pdfindex = array("d", range(1, len(h[g])))
    delMW = array("d", [m*PDFscale for m in DMW[g]])
    gScale.append(ROOT.TGraph(len(pdfindex), pdfindex, scalef(h[g], PDFscale)))
    gVar.append(ROOT.TGraph(len(pdfindex), pdfindex, varf(h[g], PDFscale)))
    gScaleVar.append(ROOT.TGraph(len(pdfindex), varf(h[g], PDFscale), scalef(h[g], PDFscale)))
    gdelMWVar.append(ROOT.TGraph(len(pdfindex), varf(h[g], PDFscale), delMW))
    gdelMWScale.append(ROOT.TGraph(len(pdfindex), scalef(h[g], PDFscale), delMW))
   
  
    hdiff = []
    for pdf in range(1,len(h[g])):
      hdiff.append(diff(h[g][0], h[g][pdf], pdf, pdfgroup[g], PDFscale))
    plotname = "diffmTW%s"%pdfgroup[g]
    overlay(hdiff, plotname, int(config('diffMW','color')), legdiffmTW[g], "m_{T}(l#nu) [GeV]", "fractional residual / 0.5 GeV", xmin=float(config('diffMW','xmin')), xmax=float(config('diffMW','xmax')), ymin=float(config('diffMW','ymin')), ymax=float(config('diffMW','ymax')), canvasheight=int(config('diffMW', 'height')), ndiv=505, labeltitletag='diffMW')
    if (pdfgroup[g] != "NNPDF30_lo_as_0118"): 
      Plot(gScale[-1], "Err_%s.eps"%pdfgroup[g], legErr_[g], "error eigen-vector(%s)"%pdfgroup[g], "Scale factor (b(m_{T}(l#nu)))", ymin=R_scal[0], ymax=R_scal[1])
      Plot(gVar[-1], "MTWVariation_%s.eps"%pdfgroup[g], legMTWVariation_[g], "error eigen-vector(%s)"%pdfgroup[g], "Variation parameter (i(m_{T}(l#nu)))", ymin=R_var[0], ymax=R_var[1])
      Plot(gScaleVar[-1], "MTWscaleratiomap_%s.eps"%pdfgroup[g], legMTWscaleratiomap_[g], "1000 x #delta_{i}^{J}  ", "Scale factor (b(m_{T}(l#nu)))", xmin=R_var[0], xmax=R_var[1], ymin=R_scal[0], ymax=R_scal[1], ndiv=505)
      Plot(gdelMWVar[-1], "MTWvarmap_%s.eps"%pdfgroup[g], legMTWvarmap_[g], "1000 x #delta_{i}^{J}  ", "#DeltaM_{W} [MeV]", xmin=R_var[0], xmax=R_var[1], ymin=R_delMW[0], ymax=R_delMW[1])
      Plot(gdelMWScale[-1], "MTWscalemap_%s.eps"%pdfgroup[g], legMTWscalemap_[g], "Scale factor (b(m_{T}(l#nu)))", "#DeltaM_{W} [MeV]", xmin=R_scal[0], xmax=R_scal[1], ymin=R_delMW[0], ymax=R_delMW[1])
   
    else:
      Plot(gScale[-1], "Err_%s.eps"%pdfgroup[g], legErr_[g], "error eigen-vector(%s)"%pdfgroup[g], "Scale factor (b(m_{T}(l#nu)))", ymin=R_scal[0], ymax=R_scal[1])
      Plot(gVar[-1], "MTWVariation_%s.eps"%pdfgroup[g], legMTWVariation_[g], "error eigen-vector(%s)"%pdfgroup[g], "Variation parameter (i(m_{T}(l#nu)))", ymin=R_var[0], ymax=R_var[1]) 
      Plot(gScaleVar[-1], "MTWscaleratiomap_%s.eps"%pdfgroup[g], legMTWscaleratiomap_[g], "1000 x #delta_{i}^{J}  ", "Scale factor (b(m_{T}(l#nu)))", xmin=R_var[0], xmax=R_var[1], ymin=R_scal[0], ymax=R_scal[1])
      Plot(gdelMWVar[-1], "MTWvarmap_%s.eps"%pdfgroup[g], legMTWvarmap_[g], "1000 x #delta_{i}^{J}  ", "#DeltaM_{W} [MeV]", xmin=R_var[0], xmax=R_var[1], ymin=R_delMW[0], ymax=R_delMW[1]) 
      Plot(gdelMWScale[-1], "MTWscalemap_%s.eps"%pdfgroup[g], legMTWscalemap_[g], "Scale factor (b(m_{T}(l#nu)))", "#DeltaM_{W} [MeV]", xmin=R_scal[0], xmax=R_scal[1], ymin=R_delMW[0], ymax=R_delMW[1])
  overlaygraph(gdelMWVar, MTWvarmapall_legend, int(config('deltaMWVSvariation','color')), "MTWvarmap_allPDF.eps", "", "1000 x #delta_{i}^{J}  ", "#DeltaM_{W} [MeV]", xmin=float(config('deltaMWVSvariation','xmin')), xmax=float(config('deltaMWVSvariation','xmax')), ymin=float(config('deltaMWVSvariation','ymin')), ymax=float(config('deltaMWVSvariation','ymax')), canvasheight=int(config('deltaMWVSvariation', 'height')), labeltitletag='deltaMWVSvariation')

if __name__ == '__main__':
  main()
