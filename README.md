# スクリプトの目的

publish_image.py スクリプトは､ブログやSNSに自分が撮った写真をアップロードするにあたり､定型的に毎回行う処理を自動化しました｡

# スクリプトの機能

- 指定された画像のサイズを､長辺を1200ピクセルにし､縦横比を保持してリサイズします｡
- EXIF情報を消去します｡
- EXIFのorientation情報を元に､画像を回転させます｡
- スクリプト内で`signiture`変数で設定している署名を､右下に小さく入れます｡
- 引数に入力したタイトルを左上に入れます｡
- 署名とタイトルの文字色は､白か黒で､画像の明るさに応じて自動選択します｡

# 依存ライブラリ

```
pip3 install pillow
```

# Fontの指定

予め当スクリプトと同じディレクトリに､タイトルや署名の文字を描画するtrue type形式のフォントを保存し､`font_file`変数にファイル名を記載しておいてください｡

# 使用方法

```
% python3 publish_image <IMAGE_FILE> <TITLE>
```

- IMAGE_FILEはJPEGファイルを指定すること
- TITLEは省略可能
- TITLEが複数単語の場合は､ダブルコーテーションで囲むこと
