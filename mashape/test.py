import mashape

res = mashape.post("http://components.mashape.com/testbinary/index.php", {"echo":"AA belloo", "file":open('/tmp/p.txt')})

print res.body
print res.raw_body