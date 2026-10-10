import requests #通信用のライブラリを読み込む（requestsはHTTPで通信するためのライブラリ）
from extract import extract_speaker #extract.pyから、自分で作った抜き出し関数を読み込む。

url = "https://kokkai.ndl.go.jp/api/speech" #URLの文字列をurlという名前の変数に入れてる（まだアクセスはしていない）
params = {                     #APIに渡す検索条件をまとめている(「キー（項目名）:値（条件）」を指定している。この時点ではまだなにも送っていない)
    "nameOfHouse": "参議院",    #院名。ここでは参議院
    "from": "2024-03-01",      #開会日時の始点
    "until": "2024-03-31",     #開会日時の終点
    "maximumRecords": 100,       #一回の最大取得件数。ここでは100件
    "recordPacking": "json",   #応答形式。ここではjsonで返ってくる（xmlかjsonを選べる）
}
#キーは検索用APIの仕様のところから拾ってきてる。https://kokkai.ndl.go.jp/api.html　← ここから拾ってる

response = requests.get(url, params=params) #urlのアドレスに検索条件を送りつけてリクエストを送り、サーバーからの返事を受け付けている。
data = response.json() #返ってきたデータを変換する処理。JSON形式の文字列を辞書とリストに変換してる。

print("総件数:", data["numberOfRecords"]) #検索条件にあう発言が全体で何件あるかをあらわす。

#評価:名前と肩書きを別々に採点し、肩書の不一致をパターンごとに数える
total = 0 
name_correct = 0 #totalの内、名前の正解した件数
position_correct = 0 #total内の、肩書きの正解した件数
#肩書きの振り分け
pattern_chair = 0 
pattern_contains = 0
pattern_other = 0

for record in data["speechRecord"]:
    result = extract_speaker(record["speech"])
    #除外した人を表示してるのは、発言なのに「⚪︎」で始まらないものがあると勝手に除外されてしまう恐れがあるため。
    if result is None: 
        print("除外:", record["speaker"])
        continue 
    answer = (record["speaker"], record["speakerPosition"])
    total += 1 
    if result[0] == answer[0]: #もし０番目、つまり名前が一致したら、
        name_correct += 1 #名前の正解した件数として１ずつ増やしてる。
    else: #一致しなかったら、
        print("名前の不一致:", result[0],"/", answer[0]) #不一致として中身を表示
    if result[1] == answer[1]: #もし１番目、つまり肩書きが一致したら、
            position_correct += 1 #肩書きの正解した件数として１ずつ増やしてる。
    elif result[1] == "委員長" and answer[1] is None: #自分の肩書きが委員長、APIの肩書きがNoneならば
        pattern_chair += 1
    elif result[1] is not None and answer[1] is not None and result[1] in answer[1]: #自分の肩書きがNoneでない、APIの肩書きがNoneでない、自分の肩書きがAPIの肩書きに含まれているならば
        pattern_contains += 1
    else: #上のどれもに当てはまらなければ、
        pattern_other += 1
        print("その他の不一致:", result[1],"/", answer[1]) #不一致として中身を表示
    

print("名前の正答率:", name_correct, "/", total, "=", round(name_correct/ total * 100, 1), "%") #round(正答率の計算, 1)で正答率を小数第一位までに表してる。
print("肩書きの正答率:", position_correct, "/", total, "=", round(position_correct/ total * 100, 1), "%") #round(正答率の計算, 1)で正答率を小数第一位までに表してる。
print("肩書きの不一致の内訳")
print("委員長の扱いの違い:", pattern_chair)
print("正式名称に含まれる:", pattern_contains)
print("その他:", pattern_other)
