import ROOT
from array import array
import ConfigParser
########################################################################################
#########GLOBAL VARIABLES##############
def config(section, var):
  default = {'height':'500', 'width':'700', 'bottom_margin':'0.1', 'x':'0.0', 'y':'0.0', 'titlesize':'0.01', "cteq6l1":'1.0', "CT10":'1.0', "CT10w":'1.0', "MSTW2008lo68cl":'1.0', "MSTW2008lo90cl":'1.0', "NNPDF30_lo_as_0118":'1.0', "MMHT2014lo68cl":'1.0', 'labelsizeX':'0.05', 'labelsizeY':'0.05', 'titlesizeX':'0.1', 'titlesizeY':'0.1','color':'1', 'legendsize':'0.05'} 
  config = ConfigParser.SafeConfigParser(default)
  config.read('configfile')
  v = config.get(section, var)
  return rem_comm(v)

def rem_comm(text):
  #to remove comments
  return text.split('#')[0].strip()

def diff(h0, h, pdfindex, pdfname, scale):
  N = h0.GetNbinsX()
  h_d = ROOT.TH1F("diffmTW%s_%i"%(pdfname, pdfindex), "diffmTW%s_%i"%(pdfname, pdfindex), N, 60, 100)
  norm0 = h0.Integral()
  norm = h.Integral()
  for i in range(N):
    d = h0.GetBinContent(i+1)/norm0*1. - h.GetBinContent(i+1)/norm*1.
    h_d.SetBinContent(i+1, d)
  h_d.Scale(scale)
  return h_d

def overlaygraph(glist, legendlist, color, docname, title, xlabel, ylabel, **Range):
  ROOT.gStyle.SetOptStat(0)
  if 'canvasheight' in Range: canvasheight = Range['canvasheight']
  else: canvasheight = config('TCanvas_configs', 'height')
  canvaswidth = config('TCanvas_configs', 'width')
  c = ROOT.TCanvas( 'c1', 'c1', 200, 10, int(canvaswidth), int(canvasheight) )
  c.SetBottomMargin(float(config('TCanvas_configs', 'bottom_margin')))
  glist[0].SetTitle("")
  if ('xmin' and 'xmax') in Range: glist[0].GetXaxis().SetRangeUser(Range['xmin'], Range['xmax'])
  if ('ymin' and 'ymax') in Range: glist[0].GetYaxis().SetRangeUser(Range['ymin'], Range['ymax'])
  if 'labeltitletag' in Range: tag = Range['labeltitletag']
  else: tag = 'TH1Axis_configs'
  titlefontsizeX = float(config(tag,'titlesizeX'))
  titlefontsizeY = float(config(tag,'titlesizeY'))
  labelfontsizeX = float(config(tag,'labelsizeX'))
  labelfontsizeY = float(config(tag,'labelsizeY'))
  glist[0].SetTitle("")
  glist[0].GetXaxis().SetTitle(xlabel)
  glist[0].GetYaxis().SetTitle(ylabel)
  glist[0].GetXaxis().SetTitleSize(titlefontsizeX)
  glist[0].GetYaxis().SetTitleSize(titlefontsizeY)
  glist[0].GetXaxis().SetLabelSize(labelfontsizeX)
  glist[0].GetYaxis().SetLabelSize(labelfontsizeY)
  glist[0].SetMarkerStyle(20)
  if (color): glist[0].SetMarkerColor(2)
  else: glist[0].SetMarkerColor(1)
  glist[0].SetMarkerSize(float(config('deltaMWVSvariation','pointsize')))
  glist[0].Draw('ap')
  leg = ROOT.TLegend(0.10, 0.47, 0.25, 0.89)
  leg.SetTextFont(30)
  leg.SetTextSize(float(config('deltaMWVSvariation','legendsize')))
  leg.SetBorderSize(0)
  leg.AddEntry(glist[0], legendlist[0], "p")
  for h in range(1,len(glist)):
    leg.AddEntry(glist[h], legendlist[h], "p")
    glist[h].SetMarkerStyle(20+h)
    if (color): glist[h].SetMarkerColor(h+2)
    else: glist[h].SetMarkerColor(1)
    glist[h].SetMarkerSize(float(config('deltaMWVSvariation','pointsize')))
    glist[h].Draw('p')
  leg.Draw()
  titleX = config('PDFlabel_configs', 'x')
  titleY = config('PDFlabel_configs', 'y')
  titlefontsize = float(config('PDFlabel_configs', 'titlesize'))
  DrawText( titleX, titleY, title, titlefontsize )
  c.Print("./send/" + docname)
  return

def overlay(hlist, docname, color, title, xlabel, ylabel, **Range):
  ROOT.gStyle.SetOptStat(0)
  if 'canvasheight' in Range: canvasheight = Range['canvasheight']
  else: canvasheight = config('TCanvas_configs', 'height')
  canvaswidth = config('TCanvas_configs', 'width')
  c = ROOT.TCanvas( 'c1', 'c1', 200, 10, int(canvaswidth), int(canvasheight) )
  c.SetBottomMargin(float(config('TCanvas_configs', 'bottom_margin')))
  hlist[0].SetTitle("")
  if ('xmin' and 'xmax') in Range: hlist[0].GetXaxis().SetRangeUser(Range['xmin'], Range['xmax'])
  if ('ymin' and 'ymax') in Range: hlist[0].GetYaxis().SetRangeUser(Range['ymin'], Range['ymax'])
  if 'labeltitletag' in Range: tag = Range['labeltitletag']
  else: tag = 'TH1Axis_configs'
  titlefontsizeX = float(config(tag,'titlesizeX'))
  titlefontsizeY = float(config(tag,'titlesizeY'))
  labelfontsizeX = float(config(tag,'labelsizeX'))
  labelfontsizeY = float(config(tag,'labelsizeY'))
  hlist[0].GetXaxis().SetTitle(xlabel)
  hlist[0].GetYaxis().SetTitle(ylabel)
  hlist[0].GetXaxis().SetTitleSize(titlefontsizeX)
  hlist[0].GetYaxis().SetTitleSize(titlefontsizeY)
  hlist[0].GetXaxis().SetLabelSize(labelfontsizeX)
  hlist[0].GetYaxis().SetLabelSize(labelfontsizeY)
  hlist[0].GetYaxis().SetTitleOffset(0.8)
  if (color): hlist[0].SetLineColor(2)
  else: hlist[0].SetLineColor(1)
  if 'ndiv' in Range: hlist[0].GetYaxis().SetNdivisions(Range['ndiv'])
  hlist[0].Draw('L')
  #leg = ROOT.TLegend(0.15, 0.45, 0.30, 0.90)
  #leg.SetLineColor(2)
  #leg.SetTextFont(30)
  #leg.SetBorderSize(0)
  #leg.AddEntry(hlist[0], docname+"0", "l")
  for h in range(1,len(hlist)):
    #leg.SetLineColor(h+2)
    #leg.AddEntry(hlist[h], docname + str(h), "l")
    if (color): hlist[h].SetLineColor(h+2)
    else: hlist[h].SetLineColor(1)
    hlist[h].Draw('L same')
  #leg.Draw()
  titleX = config('PDFlabel_configs', 'x')
  titleY = config('PDFlabel_configs', 'y')
  titlefontsize = float(config('PDFlabel_configs', 'titlesize'))
  DrawText( titleX, titleY, title, titlefontsize )
  c.Print("./send/" + docname + ".eps")
  return

def scalef(listh, scale):
  l = []
  for i in range(1, len(listh)):
    l.append(scale*1000*((listh[i].GetMean()*1./listh[0].GetMean())-1))
  return array("d", l)

def varf(listh, scale):
  l = []
  for i in range(1, len(listh)):
    l.append(scale*1000*((inf_ratio(listh[i])*1./inf_ratio(listh[0]))-1))
  return array("d", l)

def inf_ratio(h):
  inf_bin = 25
  N = h.GetNbinsX()
  num = 0.
  deno = 0.
  for i in range(N):
    if(i+1 < inf_bin): deno = deno + h.GetBinContent(i+1)
    else: num = num + h.GetBinContent(i+1)
  return num*1./deno

def Plot(graph, docname, title, xlabel, ylabel, **Range):
  canvasheight = config('TCanvas_configs', 'height')
  canvaswidth = config('TCanvas_configs', 'width')
  c = ROOT.TCanvas( 'c1', 'c1', 200, 10, int(canvaswidth), int(canvasheight) )
  c.SetBottomMargin(float(config('TCanvas_configs', 'bottom_margin')))
  graph.SetTitle("")
  titlefontsizeX = float(config('TH1Axis_configs','titlesizeX'))
  titlefontsizeY = float(config('TH1Axis_configs','titlesizeY'))
  labelfontsizeX = float(config('TH1Axis_configs','labelsizeX'))
  labelfontsizeY = float(config('TH1Axis_configs','labelsizeY'))
  graph.GetXaxis().SetTitle(xlabel)
  graph.GetXaxis().SetTitleSize(titlefontsizeX)
  graph.GetXaxis().SetLabelSize(labelfontsizeX)
  if ('xmin' and 'xmax') in Range: graph.GetXaxis().SetLimits(Range['xmin'], Range['xmax'])
  graph.GetYaxis().SetTitle(ylabel)
  graph.GetYaxis().SetTitleSize(titlefontsizeY)
  graph.GetYaxis().SetLabelSize(labelfontsizeY)
  if ('ymin' and 'ymax') in Range: graph.GetYaxis().SetRangeUser(Range['ymin'], Range['ymax'])
  if 'ndiv' in Range: graph.GetYaxis().SetNdivisions(Range['ndiv'])
  graph.SetMarkerStyle(20)
  graph.SetMarkerColor(2)
  graph.SetMarkerSize(1)
  graph.Draw("ap")
  titleX = config('PDFlabel_configs', 'x')
  titleY = config('PDFlabel_configs', 'y')
  titlefontsize = float(config('PDFlabel_configs', 'titlesize'))
  DrawText( titleX, titleY, title, titlefontsize )
  c.Print("./send/" + docname)
  return

def DrawText( x, y, text, size, color = 1):
  # Draw the text quite simply:
  l = ROOT.TLatex()
  l.SetNDC()
  l.SetTextColor( color )
  l.SetTextFont( 2 )
  l.SetTextSize( size )
  l.DrawLatex( float(x), float(y), text )
  return

