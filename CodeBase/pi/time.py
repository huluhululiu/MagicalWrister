from dataclasses import dataclass                       
from random import expovariate,seed,shuffle,random,uniform
import numpy as np
import math
from decimal import Decimal
import operator
import sys
import scipy.stats
import matplotlib.pyplot as plt
from scipy.stats import norm
import scipy.stats as stats
import matplotlib.animation as animation
@dataclass
class broker():
	indexx: int
	timeline: []
	rate: float
	invrate: float
	overloadingProb: float
	tokenRate: float
	bucket: int
	variance: float
	numPub: int
	originalT: []
	originalR: float
	originalV: float
	start: int
	end: int

@dataclass
class publisher():
	timeline:[]
	rate: float
	invrate:float
	minID: int
	variance: float
	start: int
	end: int

pubNum=1000
target=1
# brokerNum=50
# pub=[]
# bro=[]
profileNum=400
# theta=320
# standard=220
# p=0.98
# trial=1
# accumul=60
def getVar(timeline):
	#timeline is array here
	diff=np.diff(timeline)
	return np.var(diff)

def generateTimeline(lambdaa):
	time=[]
	aa=[]
	t=0
	print("pubnum is",pubNum)
	for i in range(10000):
		a=expovariate(lambdaa)
		t=t+a
		aa.append(a)
		time.append(t)
	rate=10000/(time[9999]-time[0])
	print("rate",rate)
	# print("true mean",np.mean(aa),"true var",np.var(aa),"end",aa[-1])
	return time,aa
def partialSync(lambdaa):
	interval=1/lambdaa
	time=[]
	aa=[]
	seed()
	t=random()*interval
	print(t)
	print(interval)
	for i in range(pubnum):	
		t=t+interval
		print("t is " ,t)
		time.append(t)
		aa.append(interval)
	return time,aa
# def tokenBucket(bucket,rate,timeline):
# 	# bucketNow=bucket
# 	bucketNow=0
# 	queueLength=0
# 	if len(timeline)==0:
# 		# print("notva")
# 		return 0
# 	lastUpdate=timeline[0]
# 	waitingTime=0
# 	for i in range(len(timeline)):
# 		newToken=math.floor((timeline[i]-lastUpdate)*rate)
# 		# print("new token: ", newToken)
# 		situation=newToken+bucketNow-queueLength-1
# 		if situation<0:
# 			bucketNow=0
# 			# if -situation>bucket:
# 			# 	print("errrororor")
# 			queueLength= -situation
# 		else:
# 			queueLength=0
# 			bucketNow=situation
# 		# bucketNow=min(bucket,bucketNow)
# 		lastUpdate=min(timeline[i],lastUpdate+newToken/rate)
# 		#print("end queue ", queueLength)
# 		# print("bucketnow is ", bucketNow)
# 		waitingTime+=queueLength/rate 
# 	# return waitingTime/(len(timeline)-1)
# 	return waitingTime

# time,aa=partialSync(lambdaa)
t=0
# minWT=float("inf")

pub=[]
i=0
fig, ax = plt.subplots()
# fig.set_tight_layout(True)

def tokenBucket(bucket,rate,timeline):
	# bucketNow=bucket
	queue=[]
	arrive=[]
	refil=[]
	bucketNow=bucket
	queueLength=0
	# newTokenTime=1.0/rate
	lastOne=len(timeline)-1
	if len(timeline)==0:
		# print("notva")
		return 0
	lastUpdate=timeline[0]
	waitingTime=0
	ratepub=round(len(timeline)/(timeline[lastOne]-timeline[0]),2)
	# print("rate is",ratepub)
	for i in range(len(timeline)):
		# if(timeline[i]-lastUpdate)>=newTokenTime:
		# 	refill=math.floor((timeline[i]-lastUpdate)*rate)
		# 	bucketNow=min(bucket,bucketNow+refill-queueLength-1)
		# 	lastUpdate+=refill
		# else:
		# 	bucketNow=0
		# 	queueLength+=1
		refill=math.floor((timeline[i]-lastUpdate)*rate)
		refil.append(refill)
		bucketNow=min(bucket,bucketNow+refill-queueLength)

		if bucketNow>=0:
			queueLength=0
		else: 
			queueLength=-bucketNow
			bucketNow=0
		
			
		# print("refill is %d bucket now is %d queueLength is %d"%(refill,bucketNow,queueLength))

		# print("end queue ", queueLength)
		arrive.append(bucketNow)
		if(bucketNow>0):
			bucketNow-=1
		else:
			queueLength+=1
		queue.append(queueLength/rate)	
		
		waitingTime+=queueLength/rate
		lastUpdate=min(timeline[i],lastUpdate+Decimal(refill)/Decimal(rate))

	return queue
	# return ratepub,queue,arrive,refil
def tokenSimTimeline(interval,batch,start):
	# time=[]
	# t=start

	

	# for i in range(100):
	# 	# seed()	
	# 	t=t+interval
	# 	for _ in range(batch):
	# 		time.append(Decimal(t))

	# return time
	time=[]
	tbar=start
	deif=[]
	for i in range(int(profileNum/batch)):	
		tbar=tbar+interval
		current=Decimal(tbar)
		for _ in range(batch):
			# t=current
			seed()
			t=current+Decimal(uniform(-20, 20)/1000)
			time.append(Decimal(t))
			
	print(len(time))
	return np.sort(time)

def timeAdding(lineA,lineB):
	a=np.append(np.asarray(lineA),np.asarray(lineB))

	return a

def timeAdd(lineA,lineB,rep):
	a=[]
	a=np.append(np.asarray(lineA),np.asarray(lineB))
	rrr=rep-1
	for _ in range(rrr):
		a=np.append(a,np.asarray(lineB))

	return np.sort(a)
def tbb(bucket,tokenRate,timeline):
	queue=[]
	arrive=[]
	refil=[]
	# bucketNow=
	queueLength=0

	bucketNow=bucket
	# newTokenTime=1.0/tokenRate
	lastOne=len(timeline)-1
	if len(timeline)==0:
		# print("notva")
		return 0
	lastUpdate=timeline[0]
	waitingTime=0
	tokenRatepub=round(len(timeline)/(timeline[lastOne]-timeline[0]),2)
	j=0
	for i in range(len(timeline)):
		refill=math.floor((timeline[i]-lastUpdate)*tokenRate)
		# refill=math.floor((timeline[i]-lastUpdate)/1000*tokenRate)

		bucketNow=min(bucket,bucketNow+refill-queueLength)
		if bucketNow>=0:
			queueLength=0
		else: 
			queueLength=-bucketNow
			bucketNow=0
		
		arrive.append(bucketNow)
		if(bucketNow>0):
			bucketNow-=1
			j+=1
		else:
			queueLength+=1
		refil.append(queueLength)
		# queue.append(queueLength/tokenRate/1000)
		queue.append(queueLength/tokenRate)
		waitingTime+=queueLength/tokenRate
		# lastUpdate=min(timeline[i],lastUpdate+Decimal(refill)/(Decimal(tokenRate)/1000))
		lastUpdate=min(timeline[i],lastUpdate+Decimal(refill)/Decimal(tokenRate))
	print("len",len(refil))
	queue[:]=[x*1000000 for x in queue]
	return queue

def update(i):
	wt1=q1.copy()
	wt1[:] = [x - i/halfTokenRate for x in wt1]
	wt1=np.clip(wt1,a_min=0,a_max=None)

	wt2=q1.copy()
	wt2[:] = [x - i/halfTokenRate for x in wt2]
	wt2=np.clip(wt2,a_min=0,a_max=None)
	# print(i)
	# bucket=200
	# # time,aa=generateTimeline(100)
	# ratepub,queue,arrive,refil=tokenBucket(bucket,i,time)
	# # print(ratepub)
	# s='Poisson pattern,rate='+str(ratepub)+' msgs/sec, token bucket (r,b)=('+str(i)+' tokens/sec,'+str(bucket)+' tokens)'
	# ax.set_title(s)
	l1.set_ydata(wt1)
	l2.set_ydata(wt2)
	print(np.sum(wt1-wt2))
	# l3.set_ydata(wt1-wt2)

def binaryFindBucket(wtOriginal,rate,leftBucket,rightBucket):
	bucketNow=int(0.5*(leftBucket+rightBucket))
	waitingTime=wtOriginal.copy()
	print("bucket size is",bucketNow,"rate is ",rate)
	waitingTime[:] = [x - (bucketNow)/rate for x in waitingTime]
	waitingTime=np.clip(waitingTime,a_min=0,a_max=None)
	print("algo::::")
	avg=np.mean(waitingTime)
	# print(np.percentile(waitingTime, 99))
	# print(np.percentile(waitingTime, 95))
	# print(np.percentile(waitingTime, 90))
	print("variance")
	print(np.var(waitingTime))
	print("average wt is ",avg)
	avg*=1000000
	print("diff ",target-avg)
	if(math.fabs(target-avg)<0.5):
		wt=np.sort(waitingTime)
		plt.close()
		plt.xlabel("WaitingTime in token bucket (second)")
		plt.ylabel("Probability")
		# plt.title("Add-up all the publishers")
		yvals=np.arange(len(waitingTime))/float(len(waitingTime)-1)
		plt.plot(wt,yvals)
		plt.show()
		return bucketNow
	else:
		if avg>target:
			return binaryFindBucket(wtOriginal,rate,bucketNow,rightBucket)
		else:
			return binaryFindBucket(wtOriginal,rate,leftBucket,bucketNow)
def concor(x,y):
	P=0
	Q=0
	T=0
	U=0
	for i in range(1,len(x)):
		for j in range(i):
			pairA=x[i]-x[j]
			pairB=y[i]-y[j]
			if (pairA <0 and pairB<0) or (pairA>0 and pairB>0) :
				P+=1
			elif (pairA <0 and pairB>0) or (pairA>0 and pairB<0):
				Q+=1

			elif pairA==0 and pairB!=0:
				T+=1
			elif pairA!=0 and pairB==0:
				U+=1
	# print(Q)
	return (P-Q)/math.sqrt((P+Q+T)*(P+Q+U))
# t1=tokenSimTimeline(200,0.2,0)
# tokenRate=1100
# bucket=100
# q=tokenBucket(0,tokenRate,t1)
# waitingTime=q.copy()
# waitingTime[:] = [x - bucket/tokenRate for x in waitingTime]
# waitingTime=np.clip(waitingTime,a_min=0,a_max=None)
# wt=np.sort(waitingTime)
# plt.close()
# plt.xlabel("WaitingTime in token bucket (second)")
# plt.ylabel("Probability")
# plt.title("Add-up all the publishers")
# yvals=np.arange(len(waitingTime))/float(len(waitingTime)-1)
# plt.plot(wt,yvals,label="calculation")
# q2=tokenBucket(bucket,tokenRate,t1)
# wt=np.sort(q2)
# print("max",np.max(q2),np.max(q))
# yvals=np.arange(len(wt))/float(len(wt)-1)
# plt.plot(wt,yvals,label="simulation")
# plt.legend()
# plt.show()
# rate=len(t1)/(t1[-1]-t1[1])
# print(rate)
# sorted_data = np.sort(q)
# yvals=np.arange(len(sorted_data))/float(len(sorted_data)-1)
# s1="split the sync"
# s2="combine the sync"
# plt.plot(q,label="bucket=0")
# plt.plot(q2,label="bucket=100")
# plt.legend()
# plt.ylabel("WaitingTime(seconds)")
# plt.title("Partial Sync,1 pub, each pub has period=200ms, batch=200,tokenRate="+str(tokenRate)+"tokens/sec")
# plt.show()
# binaryFindBucket(tokenBucket(0,220,t1),22,0,1000)
# plt.plot(np.arange(len(t1)), q)
# plt.show()

offset=[0.1727125620034772,0.12179062431053983,0.1931270681439736,0.17485226433352397,0.032416681301482696]
# offset=[0.15, 0.19, 0.17, 0.152, 0.5]
# t5=tokenSimTimeline(0.2,15,0.032416681301482696)

# t2=tokenSimTimeline(0.2,15,0.12179062431053983)
# t1=tokenSimTimeline(0.2,15,0.1727125620034772)
# t4=tokenSimTimeline(0.2,15,0.17485226433352397)
# t3=tokenSimTimeline(0.2,15,0.1931270681439736)

# t5[:]=[float(timeElement)*1000000000-initial for timeElement in t5]
# t3[:]=[float(timeElement)*1000000000-initial for timeElement in t3]
# mm=np.vstack((t5,t3))
pubNum=5
t=np.zeros(shape=(pubNum,390))
m=np.zeros(shape=(pubNum,390))
difff=np.zeros(shape=(pubNum,389))

zq=np.zeros(shape=(1,1))
nanoTrans=1000000000
for i in range(pubNum):
	t[i]=tokenSimTimeline(0.2,15,offset[i])
	if(i==0):
		initial=t[4][0]*nanoTrans	
	t[i][:]==[timeElement for timeElement in t[i][:]]
	if(i==0):
		zq=t[i]
	else:
		zq=np.vstack((zq,t[i]))
	m[i][:]=[timeElement-np.mean(t[i][:]) for timeElement in t[i][:]]

	difff[i][:]=np.diff(t[i][:])

# plt.plot(t5,np.arange(len(t5)))
# plt.plot(t3,np.arange(len(t5)))
# plt.show()

x=np.mean(t,axis=1)
for i in range(5):
	m[i][:]=[timeElement-np.mean(t[i][:]) for timeElement in t[i][:]]

correlation=np.zeros(shape=(pubNum,pubNum))
ccor=np.zeros(shape=(pubNum,pubNum))
for i in range(pubNum):
	ccor[i][:]=[np.dot(np.asarray(m[i][:]).T,gq)/len(m[i][:]) for gq in m[:]]
mmm=np.amin(ccor)
print(ccor)
# ccor[:]=[xxx-mmm for xxx in ccor]
# print(ccor)
	# cc=[(timee-x[i]) for timee in t[i]]
	# for j in range(5):
	# 	dd=[(timee-x[j]) for timee in t[j]]
	# 	correlation[i][j]=np.dot(np.asarray(cc).T,dd)/len(cc)
	# 	print("dif",correlation[i][j])
	# 	print("dd",ccor[i][j])

print("corr",np.argmax(ccor))
ind=np.unravel_index(np.argmax(ccor), np.shape(ccor))
print(ind)
# pp=np.dot(np.asarray(cc).T,cc)/len(cc)
# qq=np.dot(np.asarray(cc).T,dd)/len(cc)
# print(pp,qq)
# print("dif",pp-qq)
cccc=np.corrcoef(zq)
print(cccc)
print(offset)

addd=timeAdding(t[0][:],t[1][:])
mid=int((len(t[2][:])))
addd=addd[:mid]

length=len(difff[2][:])
print("kendall")
kendallMa=np.zeros(shape=(pubNum,pubNum))
for i in range(pubNum):
	
	kendallMa[i][:]=[concor(difff[i][:],gq) for gq in difff[:]]
	# kendallMa[i][:]=[stats.kendalltau(difff[i][:],gq)[0] for gq in difff[:]]
print(kendallMa)
spearr=np.zeros(shape=(pubNum,pubNum))
for i in range(pubNum):
	
	spearr[i][:]=[stats.spearmanr(difff[i][:],gq)[0] for gq in difff[:]]

print("spear",spearr)
# print("kendall",stats.kendalltau(difff))
print("0,3 kendall correlation",concor(difff[0][:],difff[3][:]))
print("0,2 kendall correlation",concor(difff[0][:],difff[2][:]))
print("kendall",np.argmax(kendallMa))
ind=np.unravel_index(np.argmax(kendallMa), np.shape(kendallMa))
print(ind)
# cooncor=np.zeros(shape=(pubNum,pubNum))
# for i in range(pubNum):
# 	cooncor[i][:]=[concor(difff[i][:],gq) for gq in difff[:]]

# print("cooncor",cooncor)

# print("cooncor",np.argmax(cooncor))
# ind=np.unravel_index(np.argmax(cooncor), np.shape(cooncor))


print("kendall correlation",stats.kendalltau(t[0][:],t[1][:]))
print("cov",np.cov(np.asarray(addd).T,t[2][:]))
print("kendall correlation",stats.kendalltau(addd,t[2][:]))
print("naonao",np.unravel_index(np.argmax(cccc), np.shape(cccc)))

# print(np.corrcoef(mm.astype(float)))
exit()
ta1=[]
ta2=[]

tb1=[]
tb2=[]

tc1=[]
tc2=[]
a=np.zeros(shape=(3,2,2))


# mid=50
# ta1=timeAdd(ta1,t1,mid)
# ta1=timeAdd(ta1,t2,mid)
# ta2=timeAdd(ta2,t1,mid)
# ta2=timeAdd(ta2,t2,mid)

# tb1=timeAdd(tb1,t1,mid+5)
# tb1=timeAdd(tb1,t2,mid-6)
# tb2=timeAdd(tb2,t1,mid-5)
# tb2=timeAdd(tb2,t2,mid+6)

# tc1=timeAdd(tc1,t1,mid+2)
# tc1=timeAdd(tc1,t2,mid-2)
# tc2=timeAdd(tc2,t1,mid-2)
# tc2=timeAdd(tc2,t2,mid+2)



# ta1=timeAdd(ta1,t1,7)
# ta1=timeAdd(ta1,t2,15)
# ta1=timeAdd(ta1,t3,12)
# ta1=timeAdd(ta1,t4,10)
# ta1=timeAdd(ta1,t5,16)

# ta2=timeAdd(ta2,t1,33)
# ta2=timeAdd(ta2,t2,25)
# ta2=timeAdd(ta2,t3,28)
# ta2=timeAdd(ta2,t4,30)
# ta2=timeAdd(ta2,t5,24)

# tb1=timeAdd(tb1,t1,9)
# tb1=timeAdd(tb1,t2,8)
# tb1=timeAdd(tb1,t3,14)
# tb1=timeAdd(tb1,t4,14)
# tb1=timeAdd(tb1,t5,15)

# tb2=timeAdd(tb2,t1,31)
# tb2=timeAdd(tb2,t2,32)
# tb2=timeAdd(tb2,t3,26)
# tb2=timeAdd(tb2,t4,26)
# tb2=timeAdd(tb2,t5,25)

# tc1=timeAdd(tc1,t1,12)
# tc1=timeAdd(tc1,t2,12)
# tc1=timeAdd(tc1,t3,12)
# tc1=timeAdd(tc1,t4,12)
# tc1=timeAdd(tc1,t5,12)

# tc2=timeAdd(tc2,t1,28)
# tc2=timeAdd(tc2,t2,28)
# tc2=timeAdd(tc2,t3,28)
# tc2=timeAdd(tc2,t4,28)
# tc2=timeAdd(tc2,t5,28)


ta1=timeAdd(ta1,t1,21)
ta1=timeAdd(ta1,t2,19)
ta1=timeAdd(ta1,t3,17)
ta1=timeAdd(ta1,t4,23)
ta1=timeAdd(ta1,t5,20)

ta2=timeAdd(ta2,t1,19)
ta2=timeAdd(ta2,t2,21)
ta2=timeAdd(ta2,t3,23)
ta2=timeAdd(ta2,t4,17)
ta2=timeAdd(ta2,t5,20)

tb1=timeAdd(tb1,t1,25)
tb1=timeAdd(tb1,t2,18)
tb1=timeAdd(tb1,t3,25)
tb1=timeAdd(tb1,t4,17)
tb1=timeAdd(tb1,t5,15)

tb2=timeAdd(tb2,t1,15)
tb2=timeAdd(tb2,t2,22)
tb2=timeAdd(tb2,t3,15)
tb2=timeAdd(tb2,t4,23)
tb2=timeAdd(tb2,t5,25)

tc1=timeAdd(tc1,t1,20)
tc1=timeAdd(tc1,t2,20)
tc1=timeAdd(tc1,t3,20)
tc1=timeAdd(tc1,t4,20)
tc1=timeAdd(tc1,t5,20)

tc2=timeAdd(tc2,t1,20)
tc2=timeAdd(tc2,t2,20)
tc2=timeAdd(tc2,t3,20)
tc2=timeAdd(tc2,t4,20)
tc2=timeAdd(tc2,t5,20)


bucketTotal=1400
bucketHalf=int(bucketTotal/2)
print(bucketHalf)
print("length is",len(ta1))
tokenTotalRate=Decimal(15000*1.1)

halfTokenRate=int(tokenTotalRate/2)
# p1=tokenBucket(bucketTotal,tokenTotalRate,s1)
# p2=tokenBucket(bucketTotal,tokenTotalRate,s2)
# p3=tokenBucket(bucketTotal,tokenTotalRate,s3)
# p4=tokenBucket(bucketTotal,tokenTotalRate,ss)
# print(len(tc1),len(tc2))
# print(np.mean(s1),np.var(s1))
# print(np.mean(s2),np.var(s2))
# print(np.mean(s3),np.var(s3))
# print(np.mean(ss),np.var(ss))
# print("p1 mean ",np.mean(p1),"var",np.var(p1),len(p1),np.sum(p1))
# print("p2 mean ",np.mean(p2),"var",np.var(p2),len(p2),np.sum(p2))
# print("p3 mean ",np.mean(p3),"var",np.var(p3),len(p3),np.sum(p3))
# print("p4 mean ",np.mean(p4),"var",np.var(p4),len(p4),np.sum(p4))
# print("pubrate")


# print(10000/(t1[9999]-t1[0]))
# tokenBucket(20,11,time)
# time,aa=generateTimeline(100)
# q3a=tbb(bucketHalf,halfTokenRate,tc2)
# q3=tbb(bucketHalf,halfTokenRate,tc1)
var=[Decimal(getVar(ta1)),Decimal(getVar(ta2)),Decimal(getVar(tb1)),Decimal(getVar(tb2)),Decimal(getVar(tc1)),Decimal(getVar(tc2))]
dd=Decimal(1/1.1)
ther=Decimal(5/10)
sev=Decimal(5/10)
print(var)
half=Decimal(5/10)

awt=ther*var[0]*ther*15000/(2*(1-dd))+sev*var[1]*sev*15000/(2*(1-dd))
bwt=ther*var[2]*ther*15000/(2*(1-dd))+sev*var[3]*sev*15000/(2*(1-dd))
cwt=ther*var[4]*ther*15000/(2*(1-dd))+sev*var[5]*sev*15000/(2*(1-dd))
print("a b",awt,bwt,cwt)
# (brokers[i].tokenRate/(safeMargin*totalRate))*brokers[i].variance*brokers[i].rate/(2*(1-brokers[i].rate/brokers[i].tokenRate))

q1a=tbb(int(bucketTotal*ther),tokenTotalRate*ther,ta1)
q2a=tbb(int(bucketTotal*sev),tokenTotalRate*sev,ta2)
q1b=tbb(int(bucketTotal*ther),tokenTotalRate*ther,tb1)
q2b=tbb(int(bucketTotal*sev),tokenTotalRate*sev,tb2)
q1c=tbb(int(bucketTotal*ther),tokenTotalRate*ther,tc1)
q2c=tbb(int(bucketTotal*sev),tokenTotalRate*sev,tc2)

# print("tb1",np.mean(q1),np.mean(q1a))
# 

q1=timeAdding(q1a,q2a)
q2=timeAdding(q1b,q2b)
q3=timeAdding(q1c,q2c)
# q1=tbb(bucketHalf,halfTokenRate,ta1)

# q2=tbb(bucketHalf,halfTokenRate,tb1)
# print("tb1")
# q2a=tbb(bucketHalf,halfTokenRate,tb2)
# q2=timeAdding(q2,q2a)


# q1=timeAdding(q1,q1a)
# print("tb1",np.mean(q1),np.mean(q3a))
# q3=timeAdding(q3,q3a)

print("q1 mean ",np.mean(q1),"var",np.var(q1),np.sum(q1))
print("q2 mean ",np.mean(q2),"var",np.var(q2),np.sum(q2))
print("q3 mean ",np.mean(q3),"var",np.var(q3),np.sum(q3))
q1=np.sort(q1)
percent=[]
print(float(np.percentile(q1,99,interpolation='higher')))
percent.append(np.percentile(q1a,99,interpolation='lower'))
percent.append(np.percentile(q1b,99,interpolation='lower'))
percent.append(np.percentile(q1c,99,interpolation='lower'))
percent.append(np.percentile(q2a,99,interpolation='lower'))
percent.append(np.percentile(q2b,99,interpolation='lower'))
percent.append(np.percentile(q2c,99,interpolation='lower'))
percent.append(np.percentile(q1,99,interpolation='lower'))
percent.append(np.percentile(q2,99,interpolation='lower'))
percent.append(np.percentile(q3,99,interpolation='lower'))
print(percent)
# plt.plot(np.arange(len(q1)),q1,label="scenario1")
# plt.plot(q1a,label="scenario1-broker2")
# plt.plot(q3,label="scenario2-broker2")
# plt.plot(q3a,label="scenario2-broker1")

fig, ax = plt.subplots()
# l1,=ax.plot(q1,label="5050")
# l2,=ax.plot(q2,label="5644")
# plt.show()
# anim=animation.FuncAnimation(fig, update, frames=np.arange(0, 500), interval=1)
# # plt.legend()
# plt.show()

# plt.plot(np.sort(q2),yvals,label="q2")
# q1[:]=[x*1000000 for x in q1]
# q2[:]=[x*1000000 for x in q2]

# # q3[:]=[x*1000000 for x in q3]
# # yvals=np.arange(len(q3))/float(len(q3)-1)
# # plt.plot(np.sort(q3),yvals,label="scenario2")

yvals=np.arange(len(q1))/float(len(q1)-1)
plt.plot(np.sort(q1),yvals,'g-',label="scenario1")
yvals=np.arange(len(q2))/float(len(q2)-1)

plt.plot(np.sort(q2),yvals,'r--',label="scenario2")
yvals=np.arange(len(q3))/float(len(q3)-1)
plt.plot(np.sort(q3),yvals,'b:',label="scenario3")
plt.xlabel("WaitingTime in Token Bucket (microsecond)")
plt.ylabel("Probability ")
plt.title("Partial Sync Period=200ms, batch=15 msgs, group=5, total 200 publishers,70-30")
plt.legend()
plt.show()
yvals=np.arange(len(q1a))/float(len(q1a)-1)
plt.plot(np.sort(q1a),yvals,'g-',label="scenario1")
yvals=np.arange(len(q1b))/float(len(q1b)-1)
plt.plot(np.sort(q1b),yvals,'r--',label="scenario2")
yvals=np.arange(len(q1c))/float(len(q1c)-1)
plt.plot(np.sort(q1c),yvals,'b:',label="scenario3")
plt.xlabel("WaitingTime in Token Bucket (microsecond)")
plt.ylabel("Probability ")
plt.title("Partial Sync Period=200ms, batch=15 msgs, group=5, total 200 publishers,30")
plt.legend()
plt.show()
yvals=np.arange(len(q2a))/float(len(q2a)-1)
plt.plot(np.sort(q2a),yvals,'g-',label="scenario1")
yvals=np.arange(len(q2b))/float(len(q2b)-1)
plt.plot(np.sort(q2b),yvals,'r--',label="scenario2")
yvals=np.arange(len(q2c))/float(len(q2c)-1)
plt.plot(np.sort(q2c),yvals,'b:',label="scenario3")
plt.xlabel("WaitingTime in Token Bucket (microsecond)")
plt.ylabel("Probability ")
plt.title("Partial Sync Period=200ms, batch=15 msgs, group=5, total 200 publishers,70")
plt.legend()

plt.show()


# l1,=ax.plot(time,a,label='queue')
# l2,=ax.plot(time,b,label='bucketnow')
# l3,=ax.plot(time,c,label='refill token')
anim=animation.FuncAnimation(fig, update, frames=np.arange(95, 110), interval=300)
# anim= animation.FuncAnimation(fig, update, frames=np.arange(95, 110), interval=300)

# plt.xlabel('Profiling timeline in seconds')
# plt.legend()

# plt.show()

# queueAvg=[]
# kk=[]

# for i in range(95,110):
# 	a,b=tokenBucket(200,i,time)
# 	queueAvg.append(a)
# 	kk.append(b)
# plt.plot(np.arange(95,110),queueAvg,label="queue length")
# plt.plot(np.arange(95,110),kk,label='token bucket rate')
# rate=len(time)/(time[9999]-time[0])
# plt.ylabel('queue length')# Create the boxplot
# plt.xlabel('token bucket rate')
# s='Poisson pattern '+str(rate)+' msgs/sec, token bucket size=200, average queue length versus token bucket rate'
# plt.title(s)# basic plot
# plt.legend()
# plt.show()

# cc=[]
# for k in range(i):
# 	print(pub[k].rate)
# 	cc.append(pub[k].rate)
# print("mean is",np.mean(cc))
# # 		print("re")
# bro[0].tokenRate=tokenSumRate*0.25
# bro[1].tokenRate=tokenSumRate*0.25
# bro[2].tokenRate=tokenSumRate*0.25
# bro[3].tokenRate=tokenSumRate*0.25
# pubAssign(pub,bro[:K],K,totalRate)
# bro[0].tokenRate=tokenSumRate*0.1
# bro[1].tokenRate=tokenSumRate*0.2
# bro[2].tokenRate=tokenSumRate*0.3
# bro[3].tokenRate=tokenSumRate*0.4
# pubAssign(pub,bro[:K],K,totalRate)
# bro[0].tokenRate=tokenSumRate*0.20
# bro[1].tokenRate=tokenSumRate*0.30
# bro[2].tokenRate=tokenSumRate*0.30
# bro[3].tokenRate=tokenSumRate*0.23
# pubAssign(pub,bro[:K],K,totalRate)
# bro[0].tokenRate=tokenSumRate*0.15
# bro[1].tokenRate=tokenSumRate*0.35
# bro[2].tokenRate=tokenSumRate*0.40
# bro[3].tokenRate=tokenSumRate*0.10
# pubAssign(pub,bro[:K],K,totalRate)
# bro[0].tokenRate=tokenSumRate*0.15
# bro[1].tokenRate=tokenSumRate*0.15
# bro[2].tokenRate=tokenSumRate*0.10
# bro[3].tokenRate=tokenSumRate*0.60


# print("TBCOMPARA min wt is %.4f %.4f %.4f"%(minWT, minWT2,minWT3))
# # print("diff is ",(minWT-minWT3)/minWT3," ", (minWT2-minWT3)/minWT3)
# print("cc is %.4f %.4f"%((minWT-minWT3)/minWT3,(minWT2-minWT3)/minWT3))

# print(aa)
# print("aa mean %f var %f"%(np.mean(aa),np.var(aa)))
# print("start",time[0],"end",time[1],"total",time[pubnum-1]-time[0])
# rate=pubnum/(time[pubnum-1]-time[0])
# print(time[pubnum-1]-time[0])

# print("mean of interarrival is",np.mean(interarrival),"suppose to be ", 1/lambdaa)
# print("rate of arr",rate,"suppose to be",lambdaa)
# print("variance of arrival is",np.var(interarrival),"suppose to be ",0)