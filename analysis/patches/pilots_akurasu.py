# -*- coding: utf-8 -*-
"""Pilot names verified against akurasu's Z3 Pilot Database.

Source: https://akurasu.net/wiki/Super_Robot_Wars/Z3/Pilot_Database
Akurasu lists English only, so the Japanese side is matched from the game's own
library (MTZKN_PT: CHFN full name, CHNN short name).

AMBIGUOUS entries are the ones a global find-and-replace gets wrong, which is
the whole reason this file records status rather than just a mapping. The
clearest case here is ドロシー: it is the short name of BOTH
ドロシー・カタロニア (Gundam Wing) and Ｒ．ドロシー・ウェインライト (The Big O).
Whichever way it is renamed globally, one of the two is wrong.
"""

O, A = "official", "ambiguous"
SRC = "akurasu:Super_Robot_Wars/Z3/Pilot_Database"

# (japanese, english, status, note)
FULL = [
 # --- original ---
 ("神代ヒビキ", "Hibiki Kamishiro", O, "the default name behind the $n placeholder"),
 ("西条涼音", "Suzune Saijou", O, ""),
 ("アンナロッタ・ストールズ", "Annalotta Stohls", O, ""),
 ("アドヴェント", "Advent", O, ""),
 # --- Trider G7 ---
 ("竹尾ワッ太", "Watta Takeo", O, ""), ("柿小路梅麻呂", "Umemaro Kakikouji", O, ""),
 ("熱井徹雄", "Tetsuo Atsui", O, ""), ("木下藤八郎", "Touhachirou Kinoshita", O, ""),
 ("砂原郁絵", "Ikue Sunabara", O, ""), ("滝かおる", "Kaoru Taki", O, ""),
 # --- Tetsujin 28 ---
 ("金田正太郎", "Shotaro Kaneda", O, ""), ("敷島牧子", "Makiko Shikishima", O, ""),
 # --- Godmars ---
 ("明神タケル", "Takeru Myojin", O, ""), ("飛鳥ケンジ", "Kenji Asuka", O, ""),
 ("伊集院ナオト", "Naoto Ijuin", O, ""), ("木曽アキラ", "Akira Kiso", O, ""),
 ("日向ミカ", "Mika Hyuga", O, ""), ("ロゼ", "Roze", O, ""),
 # --- VOTOMS ---
 ("キリコ・キュービー", "Chirico Cuvie", O, ""), ("ル・シャッコ", "Ru Shako", O, ""),
 # --- Orguss ---
 ("桂木桂", "Kei Katsuragi", O, "short name 桂 is Kei, not Katsura"),
 ("モーム", "Mome", O, ""),
 # --- Zeta Gundam ---
 ("カミーユ・ビダン", "Kamille Bidan", O, ""), ("ファ・ユイリィ", "Fa Yuiri", O, ""),
 ("フォウ・ムラサメ", "Four Murasame", O, ""), ("エマ・シーン", "Emma Sheen", O, ""),
 ("カツ・コバヤシ", "Katz Kobayashi", O, ""), ("ハマーン・カーン", "Haman Karn", O, ""),
 ("クワトロ・バジーナ", "Quattro Bajeena", O, ""),
 # --- Char's Counterattack ---
 ("アムロ・レイ", "Amuro Ray", O, ""), ("シャア・アズナブル", "Char Aznable", O, ""),
 ("クェス・パラヤ", "Quess Paraya", O, ""), ("ギュネイ・ガス", "Gyunei Guss", O, ""),
 ("ハサウェイ・ノア", "Hathaway Noa", O, ""), ("ブライト・ノア", "Bright Noa", O, ""),
 # --- Gundam Wing ---
 ("ヒイロ・ユイ", "Heero Yui", O, ""), ("デュオ・マックスウェル", "Duo Maxwell", O, ""),
 ("トロワ・バートン", "Trowa Barton", O, ""),
 ("カトル・ラバーバ・ウィナー", "Quatre Raberba Winner", O, ""),
 ("張五飛", "Wufei Chang", O, ""), ("ゼクス・マーキス", "Zechs Marquise", O, ""),
 ("ルクレツィア・ノイン", "Lucrezia Noin", O, ""),
 ("ヒルデ・シュバイカー", "Hilde Schubaker", O, ""),
 ("ドロシー・カタロニア", "Dorothy Catalonia", O, ""),
 # --- SEED Destiny ---
 ("シン・アスカ", "Shinn Asuka", O, "Shinn, two n's"),
 ("キラ・ヤマト", "Kira Yamato", O, ""),
 # --- Gundam 00 ---
 ("刹那・Ｆ・セイエイ", "Setsuna F. Seiei", O, ""),
 ("ロックオン・ストラトス", "Lockon Stratos", O, ""),
 ("アレルヤ・ハプティズム", "Allelujah Haptism", O, ""),
 ("ソーマ・ピーリス", "Soma Peries", O, ""), ("ティエリア・アーデ", "Tieria Erde", O, ""),
 ("スメラギ・李・ノリエガ", "Sumeragi Lee Noriega", O, ""),
 ("ラッセ・アイオン", "Lasse Aeon", O, ""), ("フェルト・グレイス", "Feldt Grace", O, ""),
 ("ミレイナ・ヴァスティ", "Mileina Vashti", O, ""), ("グラハム・エーカー", "Graham Aker", O, ""),
 ("パトリック・コーラサワー", "Patrick Colasour", O, ""),
 ("アンドレイ・スミルノフ", "Andrei Smirnov", O, ""),
 # --- Gundam UC ---
 ("バナージ・リンクス", "Banagher Links", O, ""),
 ("リディ・マーセナス", "Riddhe Marcenas", O, ""), ("マリーダ・クルス", "Marida Cruz", O, ""),
 ("ダグザ・マックール", "Daguza Mackle", O, ""),
 # --- Gunbuster ---
 ("タカヤノリコ", "Noriko Takaya", O, ""),
 # --- Macross ---
 ("熱気バサラ", "Basara Nekki", O, ""), ("ガムリン木崎", "Gamlin Kizaki", O, ""),
 ("早乙女アルト", "Alto Saotome", O, ""), ("ミハエル・ブラン", "Michel Blanc", O, ""),
 ("ルカ・アンジェローニ", "Luca Angelloni", O, ""), ("オズマ・リー", "Ozma Lee", O, ""),
 ("クラン・クラン", "Klan Klang", O, ""),
 ("カナリア・ベルシュタイン", "Canaria Bernstein", O, ""),
 ("ジェフリー・ワイルダー", "Jeffrey Wilder", O, ""),
 ("ボビー・マルゴ", "Bobby Margot", O, ""),
 ("キャサリン・グラス", "Catherine Glass", O, ""),
 # --- Getter ---
 ("流竜馬", "Ryouma Nagare", O, ""), ("神隼人", "Hayato Jin", O, ""),
 ("車弁慶", "Benkei Kurama", O, ""),
 # --- Mazinger ---
 ("兜甲児", "Kouji Kabuto", O, ""), ("弓さやか", "Sayaka Yumi", O, ""),
 ("ボス", "Boss", O, ""),
 # --- Dai-Guard ---
 ("赤木俊介", "Shunsuke Akagi", O, ""), ("桃井いぶき", "Ibuki Momoi", O, ""),
 ("青山圭一郎", "Keiichirou Aoyama", O, ""),
 # --- The Big O ---
 ("ロジャー・スミス", "Roger Smith", O, ""),
 ("Ｒ．ドロシー・ウェインライト", "R. Dorothy Waynewright", O, ""),
 # --- Full Metal Panic! ---
 ("相良宗介", "Sousuke Sagara", O, ""), ("メリッサ・マオ", "Melissa Mao", O, ""),
 ("クルツ・ウェーバー", "Kurz Weber", O, ""),
 ("テレサ・テスタロッサ", "Teletha Testarossa", O, ""),
 ("リチャード・マデューカス", "Richard Mardukas", O, ""),
 ("ベルファンガン・クルーゾー", "Belfangan Clouseau", O, ""),
 ("千鳥かなめ", "Kaname Chidori", O, ""), ("常盤恭子", "Kyoko Tokiwa", O, ""),
 ("工藤詩織", "Shiori Kudou", O, ""),
 # --- Dancouga Nova ---
 ("日高アオイ", "Aoi Hidaka", O, ""), ("橘クララ", "Kurara Tachibana", O, ""),
 ("加門サクヤ", "Sakuya Kamon", O, ""), ("ジョニー・バーネット", "Johnny Burnette", O, ""),
 # --- Gurren Lagann ---
 ("シモン", "Simon", O, ""), ("ヴィラル", "Viral", O, ""), ("ニア", "Nia", O, ""),
 ("ヨーコ", "Yoko", O, ""), ("キタン", "Kittan", O, ""), ("ロージェノム", "Lordgenome", O, ""),
 # --- Evangelion ---
 ("碇シンジ", "Shinji Ikari", O, ""), ("綾波レイ", "Rei Ayanami", O, ""),
 ("式波・アスカ・ラングレー", "Asuka Langley Shikinami", O, ""),
 ("真希波・マリ・イラストリアス", "Mari Illustrious Makinami", O, ""),
 # --- Code Geass ---
 ("ゼロ", "Zero", O, ""), ("枢木スザク", "Suzaku Kururugi", O, ""),
 ("紅月カレン", "Kallen Kozuki", O, ""), ("Ｃ．Ｃ．", "C.C.", O, ""),
 # --- Aquarion EVOL ---
 ("アマタ・ソラ", "Amata Sora", O, ""), ("ゼシカ・ウォン", "Zessica Wong", O, ""),
 ("カイエン・スズシロ", "Cayenne Suzushiro", O, ""),
 ("ミコノ・スズシロ", "Mikono Suzushiro", O, ""),
 ("アンディ・Ｗ・ホール", "Andy W. Hole", O, ""),
 ("シュレード・エラン", "Shrade Elan", O, ""),
 ("ユノハ・スルール", "Yunoha Thrul", O, ""),
]

# Short names. Most are unambiguous, but a few are shared between series.
SHORT = [
 ("ヒビキ", "Hibiki", O, ""), ("スズネ", "Suzune", O, ""),
 ("ワッ太", "Watta", O, ""), ("かおる", "Kaoru", O, ""),
 ("正太郎", "Shotaro", O, ""), ("マッキー", "Makki", O, ""),
 ("桂", "Kei", O, "桂木桂 of Orguss; NOT Katsura"),
 ("カミーユ", "Kamille", O, ""), ("クワトロ", "Quattro", O, ""),
 ("アムロ", "Amuro", O, ""), ("シン", "Shinn", O, ""), ("キラ", "Kira", O, ""),
 ("ロジャー", "Roger", O, ""),
 ("ドロシー", "Dorothy", A,
  "shared by ドロシー・カタロニア (Gundam Wing) and R. Dorothy Waynewright "
  "(The Big O) -- never globally replace, decide per scene"),
 ("宗介", "Sousuke", O, ""), ("マオ", "Mao", O, ""), ("クルツ", "Kurz", O, ""),
 ("かなめ", "Kaname", O, ""), ("恭子", "Kyoko", O, ""), ("詩織", "Shiori", O, ""),
]
