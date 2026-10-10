#発言の本文から、発言者の名前と肩書きを抜き出す。
#
#手順
#1.本文が「○」で始まらなければ、発言ではないので対象外にする
#2.先頭の「○」を取り除く
#3.最初の全角スペースより前を「発言者の表記」として切り出す
#4.表記に「（」があれば、「（」の前が肩書き、「（」と「君）」の間が名前
#5.「（」がなければ肩書きはなしとし、末尾の「君」を取り除いたものを名前とする

def extract_speaker(text): 
    #本文を受け取り、（名前, 肩書き）を返す。発言でなければ None を返す。
    if text.startswith("○"):                         # 手順１
        label = text[1:].split("\u3000")[0]          # 手順２・３
        if "（" in label:                            # 手順４
            position = label.split("（")[0]
            name = label.split("（")[1].removesuffix("君）") 
        else:                                        # 手順５
            position = None
            name = label.removesuffix("君")
        return name, position 
    else:
        return None 


    
if __name__ == "__main__":
    #このファイルを直接実行した時だけ、例でテストする。（fetch.pyからimportした時は動かない）
    examples = [
        "○議長（尾辻秀久君）　これより会議を開きます。",
        "○阿達雅志君　ただいま議題となりました両法律案につきまして",
        "令和六年三月二十九日（金曜日）",
    ] #1日目の出力から取った例（3つ目は発言でないデータ）
    for text in examples:
        print(extract_speaker(text))