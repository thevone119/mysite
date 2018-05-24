from mysite.libs import myredis
import pickle
r = myredis.getRedis()

s = "baby123132132"

#r.incr("nameidx",-1)
r.set("name",s,ex=60)
ret = r.get("name")
print(ret.decode())
print(int(r.get("incrby")))
print(r.llen("HTTPGET:POOL"))
r.delete("HTTPGET:POOL")

kquery = r.keys("HTTPGET*")
for k in kquery:
    print(k)
