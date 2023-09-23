from Grammar import *

grammar = Grammar()

grammar.saveLogs = True

grammar.addRule("start", "<S>")
grammar.addRule("S", "(person = <who>) | #person# <(#person#)getSpecVerb> playing all day. $capS$ let's $eS$ test it out.")
grammar.addRule("who", "[he; she; we; they]")
grammar.addRule("getSpecVerb", "(person) | [{#person# == he}is; {#person# == she}is; {#person# == we}are; {#person# == they}are]")

result = grammar.run("<start>")
print(result)