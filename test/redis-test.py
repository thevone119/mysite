from mysite.libs import myredis

r = myredis.getRedis()

s = "baby123132132"
r.set("name", s)

print(r.get("name"))
print(s)
print(r.dbsize())

