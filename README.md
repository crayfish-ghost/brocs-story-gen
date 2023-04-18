# brocs-story-gen
ブロッコリー星人が地球に侵略してきたあとの世界に存在する様々なコンテンツをchatGPTに捏造してもらう実験的なスクリプトです。  
登場人物などの固有名詞は `prompts/step1.txt` をご覧ください。

# sample
実行時にはOPENAI_API_KEYを`config.ini`に書いておく必要があります。
## その1
```
$ python main.py

【broc-GPTとの対談】(科学・哲学)
"ブロッコリー星人の栄養源として人類を管理栽培することしか認めない"というブロッコリー星人の信念について、broc-GPTはこう語る。
「我々は人類の知能を認める。人類が栄養源であることは認めるが、種族としての価値も持つ。共存は可能であると考える」
また、「ブロッコリー星人にとって人類の滅亡が良い結果をもたらすというのは誤りである。地球上の多様な生物や環境を維持することが宇宙全体のバランスを保つことにつながる」とも。
broc-GPTはブロッコリー星人の信念に疑問を持ち、より良い未来を見据えた提言を行っていた。
```

## その2
```
$ python main.py

【freecat.coop、暗躍手口が明るみに！】(ハッキング問題)
「この映像は、ハッカー集団freecat.coopの内部映像である。彼らは、Nosray Industryからの依頼でbroc-GPTの侵入作戦を行っていた。
しかし、その最中に突如N.O.S.T.R本部への侵入が発覚。精鋭部隊による追跡の末、freecat.coopは壊滅した。
しかし、その内部映像から、彼らの活動には密かにPazが関与していた事が明らかになった。PazとN.O.S.T.Rの内部にも潜り込む謎のハッカー。
その存在は、暗躍する勢力の影響力がますます急速に広がっていることを示唆している。」
```

## その3
```
$ python main.py

【Damasに新首脳誕生、世界の注目集める】(ニュース)
地下国家Damasに新たな首脳が誕生した。名前は明かされていないが、今回の選出により、Damasは新たなステップに進むことが期待される。
就任式にはDamas住民のみならず、世界中から注目が集まり、N.O.S.T.R首脳陣も祝意を述べた。一方、ブロッコリー星人の報復を危惧する声もあり、厳戒態勢が敷かれた。
Damas首脳は、人類を救うため、ブロッコリー星人との最後の戦いに挑むと宣言している。
```

# その他
`prompts/step1.txt`の設定を書き換えれば自分の好きな世界設定で同様のエピソード群を作れると思います。  
設定を考えるのは好きだがストーリーを考えるのは苦手、という人には良いかもしれません。