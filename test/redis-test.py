from mysite.libs import myredis
import pickle
r = myredis.getRedis()

s = "baby123132132"


r.set("name",s,ex=60)
ret = r.get("name")
print(ret.decode())
print(s)
print(r.dbsize())

