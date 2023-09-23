from Grammar import *

grammar = Grammar()


grammar.addRule("start", "[<template1>; <template2>; <template3>]")
grammar.addRule("template1", "$capS$ <getMix> <getCharacter> and <getGoal>")
grammar.addRule("template2", "$capS$ <gameDisc> game about a <characterFull> who <characterInfo> and is trying to <goal>")
grammar.addRule("template3", "$capS$ game simular to <game> but you are a <character> and you have to [<goal>; <goal> and <goal>] [$eSL$;before you finally can <goal>].")

grammar.addRule("getMix", "mix between <gameGenre> and <gameGenre>")
grammar.addRule("getCharacter", "where you play as a <characterFull>")
grammar.addRule("getGoal", "your goal is to <goal>")

grammar.addRule("game", "[Minecraft; Dota 2; Brawlhalla; Warcraft3]")
grammar.addRule("gameGenre", "[sandbox; real-time strategy; battle royale; role-playing; simulation; puzzle; party game; action-adventure; survival; platformer; shooter; fighting game; stealth game; rhythm game; text adventure; visual novel; roguelike; life simulation; tower defense; turn-based strategy; wargame; racing; sports game; board game; card game; social deduction game]")
grammar.addRule("characterFull", "[<characterDisc> <character>; <character>]")
grammar.addRule("characterDisc", "[italian; hot; beautiful; short; tall; nice; cute; red; bright; dark; blue; cyan; scary; lonely; powerful; bored; stupid; little; helpless; smart; dumb]")
grammar.addRule("character", "[troll; killer; car; train; businessman; street cleaner; plumber; bee; cloud; dictator; builder; painter; dog; robot]")
grammar.addRule("goal", "[<enemyAction> a <characterDisc> <enemy>; <locationAction> a <location>]")
grammar.addRule("enemy", "[wolf; elf; warrior; soldier; robot]")
grammar.addRule("enemyAction", "[destroy; defeat; get friends with; chear up; pet; help]")

grammar.addRule("locationAction", "[get to; pass; escape from; build; explore; climb up]")
grammar.addRule("location", "[<locationDisc> <locationPlace>; <locationPlace>]")
grammar.addRule("locationDisc", "[old; scary; huge; lost; spooky; beautiful; nice; neat]")
grammar.addRule("locationPlace", "[house; maze; waterfall; city; town; village; mountain; desert; forest; sky; island; ship]")

grammar.addRule("gameDisc", "[funny; cooperative; horror; fast-pased; turn-based; hard; open-world]")
grammar.addRule("characterInfo", "[sold his soul; has a super gun; forgot to turn off iron; likes to sing; is scared of crowded places; live in a <location>]")


result = grammar.run("<start>")
print(result)

