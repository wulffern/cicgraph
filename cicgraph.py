#!/usr/local/bin/python3
######################################################################
##        Copyright (c) 2020 Carsten Wulff Software, Norway
## ###################################################################
## Created       : wulff at 2020-11-14
## ###################################################################
##  The MIT License (MIT)
##
##  Permission is hereby granted, free of charge, to any person obtaining a copy
##  of this software and associated documentation files (the "Software"), to deal
##  in the Software without restriction, including without limitation the rights
##  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
##  copies of the Software, and to permit persons to whom the Software is
##  furnished to do so, subject to the following conditions:
##
##  The above copyright notice and this permission notice shall be included in all
##  copies or substantial portions of the Software.
##
##  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
##  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
##  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
##  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
##  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
##  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
##  SOFTWARE.
##
######################################################################

import click
import yaml
import re

colors = [
    "#03045E",
    "#023E8A",
    "#0077B6",
    "#0096C7",
    "#00B4D8",
    "#48CAE4",
    "#90E0EF",
    "#ADE8F4",
    "#CAF0F8",
]

font_colors = [
    "white",
    "white",
    "white",
    "white",
    "white",
    "black",
    "black",
    "black",
    "black"
]



gray_color = "silver"

header = """
digraph gr {


"""

footer = """
}
"""

nodedef = """\"{name}\" [ fontname=\"Helvetica\" fontsize=\"{fz}\" margin=0.2 label=\"{label}\" fontcolor="{font_color}" color="{color}" shape={shape} style=filled width={w}];"""

nr = 0

d_width = 2

relation = list()

def printElements(obj,idx,fo,par=None,shape="circle",uniq=True,edgem=True):
    global nr,d_width

    width = d_width - idx/3
    if(width < 1):
        width = 1

    fsize = 14*width

    rt = ""

    for k,v in obj.items():
        nr = nr +  1

        if(k == "_dependsOn"):
            edge_length= width*edgem
            rt += f"\"{par}\" -> \"{v}\" [len={edge_length}];\n"
            continue

        if(uniq):
            key = k + " " + str(nr)
        else:
            key = k
        nd = nodedef
        nd = nd.replace("{name}",key)
        nd = nd.replace("{label}",k)
        nd = nd.replace("{w}",str(width))
        nd = nd.replace("{fz}",str(fsize))
        nd = nd.replace("{shape}",shape)

        #- Color
        color = colors[idx % len(colors)]

        if("(N/A)" in k):
            color = gray_colon

        nd = nd.replace("{color}",color)



        font_color = font_colors[idx % len(font_colors)]
        
        nd = nd.replace("{font_color}",font_color)

        print(nd,file=fo)
        if(isinstance(v,dict)):
            rt += printElements(v,idx+1,fo,key,shape=shape,uniq=uniq,edgem=edgem)
        if(par):
            edge_length= width*edgem
            rt += f"\"{par}\" -> \"{key}\" [len={edge_length}];\n"
    return rt


@click.command()
@click.argument("ifile")
@click.option("--shape",default="circle",help="Default shape")
@click.option("--uniq/--no-uniq",default=True,help="Uniqify names")
@click.option("--edgem",default=1.5,help="Edge Multiplier")
def cli(ifile,shape,uniq,edgem):
    """Turn YAML into dot file"""

    obj = {}
    with open(ifile,"r") as fi:
        obj = yaml.load(fi, Loader=yaml.FullLoader)

    idx=0

    ofile = ifile.replace(".yaml",".dot")
    with open(ofile,"w") as fo:
        print(header,file=fo)
        rt = printElements(obj,idx,fo,shape=shape,uniq=uniq,edgem=edgem)
        print(rt,file=fo)
        print(footer,file=fo)



if(__name__ == "__main__"):
    cli()
