from datetime import date, datetime

def repr(classname,self,args):
    ret=f"{classname}("
    for v in args.split(","):
        try:ret += f'{v}={eval(f"self.{v}")},'
        except:pass
    ret += "\b)"
    return ret
def getUnix(lst:list): return datetime(*lst).timestamp()
def isint(txt:str):
    try:int(txt)
    except ValueError:return False
    else:return True

class Seq:
    def __init__(self,username,seq,date:tuple,hms:tuple) -> None:
        self.username=username
        self.seq=seq
        self.date=date
        self.hms=hms
        self.unixtime=getUnix(list(date+hms))
    def plus(self,new:str):
        self.seq+="\n"+new
    def __repr__(self) -> str:
        return repr("Seq",self,"date,hms,username,seq")

class Linetxt:
    def isDate(self,oneLine:str,options):
        return oneLine.count(options["dateSplit"])==options["dateSplitCount"] and\
            options["dateMM"][0]<=len(oneLine) and len(oneLine)<=options["dateMM"][1]
    def dateParse(self,oneLine:str,options):
        sp=oneLine.split(options["dateSplit"])
        last=sp[2]
        ls=""
        for v in last:
            ls+=v
            if not isint(ls):break
        sp[2]=ls[:-1]
        sp[0]=int(sp[0]);sp[1]=int(sp[1]);sp[2]=int(sp[2])
        return tuple(sp)
    def seqParse(self,oneLine:str,options):
        sp=oneLine.split(options["split"])
        time=tuple(sp[0].split(":"))
        username=sp[1]
        seq=options["split"].join(sp[1:])
        return [tuple([int(_) for _ in time]),username,seq]
    def isSeq(self,oneLine:str,options):
        sp=oneLine.split(options["split"])
        tes=sp[0].split(":")
        return len(tes)==2 and isint(tes[0]) and isint(tes[1])


    def __init__(self,txt,options:dict={}) -> None:
        txt=txt.replace("\ufeff","")
        sptxt=txt.split("\n")
        seqs=[]
        for oneLine in sptxt:
            
            if self.isDate(oneLine,options):
                now=self.dateParse(oneLine,options)
            elif self.isSeq(oneLine,options):
                n=self.seqParse(oneLine,options)
                seqs.append(Seq(n[1],n[2],now,n[0]))
            else:
                seqs[-1].plus(oneLine)
                #print(oneLine)
        self.seqs=seqs

    def search(self,getDate:tuple=None,username:str=""):
        answer=[]
        if getDate:
            if len(getDate)!=2:
                raise TypeError("getDate argument length must be 2")
            fromUnix=getUnix(getDate[0])
            toUnix=getUnix(getDate[1])
        else:
            fromUnix=0;toUnix=99999999999999999999999999999999999999
        for talk in self.seqs:
            unixtime=talk.unixtime
            if bool(username):
                if talk.username==username:
                    if fromUnix<=unixtime and unixtime<=toUnix:
                        answer.append(talk)
            else:
                if fromUnix<=unixtime and unixtime<=toUnix:
                    answer.append(talk)
        return answer

if __name__=="__main__":
    with open("[LINE] 中野中1年(2022-04~2023-03)のトーク.txt",encoding="utf-8") as f:
        e=Linetxt(f.read(),options={
            "dateSplit":"/",
            "dateSplitCount":2,
            "dateMM":(10,15),
            "split":"\t"
            
        })
        print(e.search(username="しょうたろう"))