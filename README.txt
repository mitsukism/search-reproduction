roca searchchrome拡張機能の実装コード
manifest.json...拡張機能の基本的な設定を記述
popup.js...アイコンをクリックされたら起動するポップアップのバックの処理内容を記述。
chromeから検索データを取得してURLを変換するassignNumber関数とAWSにデータを渡すSendEndpoint関数の順番で処理される。
検索データに使う情報には他にもいろいろ使える
popup.html...アイコンをクリックされたら起動するポップアップのフロントの処理内容を記述。

URLを変換する規則
1
start

2
before
https://www.google.com/search?q=___
curr
https://www.google.com/search?q=___~

queryが違う

3
before
https://www.google.com/search?q=____
curr
https://abc~

4
before
https://www.google.com/search?q=___
curr
https://www.google.com/search?q=___~

queryが一致

5
before
https://abc~
curr
https//:www.google.com/search?q=____

6
before
https://abc~
curr
https://abc~

ドメイン一致

7
before
https://abc~
curr
https://def~

ドメインが違う