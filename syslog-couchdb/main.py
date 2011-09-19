#!/usr/bin/python2

from pyparsing import Word, alphas, Suppress, Combine, nums, string, Optional, Regex
import couchdb
import sys

month = Word(string.uppercase, string.lowercase, exact=3)
integer = Word(nums)

serverDateTime = Combine(month + " " + integer + " " + integer + ":" + integer + ":" + integer)
hostname = Word(alphas + nums + "_" + "-")
daemon = Word(alphas + "/" + "-" + "_")
pid = Combine(Optional(Suppress("[") + integer + Suppress("]")) + Suppress(":"))
message = Regex(".*")

bnf = serverDateTime('datetime') + hostname('hostname') + daemon('daemon') + pid('pid') + message('message')

couch = couchdb.Server('http://localhost:5984/')
db = couch['syslog']
log = dict()

while True:
    #line = 'Feb 18 00:05:08 cr48 kernel: lo: Disabled Privacy Extensions'
    line = sys.stdin.readline()

    try:    
        fields = bnf.parseString(line)
    except:
        # because of the syslog --MARK-- stuff, I don't care to log those
        continue

    if fields['pid'] == "":
        del fields['pid']

    print db.create(fields.asDict())
