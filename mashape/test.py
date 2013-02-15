import mashape

res = mashape.get("http://components.mashape.com/sub/test/api.php?_method=getHello&name=MArcooo")

print res.body
print res.raw_body
