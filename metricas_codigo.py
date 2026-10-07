import json,subprocess,glob,os,re,collections
from radon.metrics import mi_visit, h_visit, mi_compute
from radon.raw import analyze
from radon.visitors import ComplexityVisitor
import sys
D=sys.argv[1] if len(sys.argv)>1 else '../codigos'
cfg_art=["--disable=C0114,C0115,C0116","--module-naming-style=any","--disable=C0304"]
cfg_def=["--module-naming-style=any","--disable=C0304"]  # docstrings ON
rows=[]
def run(f,cfg):
    out=subprocess.run(["pylint",f,"--output-format=json2",*cfg],capture_output=True,text=True).stdout
    j=json.loads(out); s=j["statistics"]
    return max(0,s["score"]), [m["symbol"]+"|"+m["type"] for m in j["messages"]], s["modulesLinted"]
for f in sorted(glob.glob(D+'/*.py')):
    b=os.path.basename(f)[:-3]; pid,tool,ex=b.split('_')
    src=open(f,encoding='utf-8').read()
    sc,msgs,_=run(f,cfg_art); sc2,msgs2,_=run(f,cfg_def)
    raw=analyze(src)
    mi=mi_visit(src,True)
    # MI without comment term
    hv=h_visit(src).total.volume; cc=ComplexityVisitor.from_code(src).total_complexity
    mi_nc=mi_compute(hv,cc,raw.sloc,0)
    rows.append(dict(id=pid,tool=tool,ex=int(ex),pylint=round(sc,2),pylint_doc=round(sc2,2),msgs=msgs,msgs_doc=msgs2,mi=round(mi,2),mi_nc=round(mi_nc,2),cc=cc,sloc=raw.sloc,loc=raw.loc,comments=raw.comments,multi=raw.multi))
json.dump(rows,open('codemetrics.json','w'),ensure_ascii=False,indent=0)
print(len(rows))
