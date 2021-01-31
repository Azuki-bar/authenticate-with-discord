# authenticate-with-discord

## 使用方法
プロジェクトのディレクトリに以下の内容のファイルを`AUTH_DATA.json`という
ファイル名で保存して下さい。

```json
{
  "Discord": {
    "Token": "YOUR DISCORD BOT TOKEN",
    "ChannelID": "YOUR DISCORD CHANNEL ID" 
  },
  "Google": {
    "Token": "YOUR GOOGLE 2FA SECRET KEY"
  }
}
```

そうしたら`pipenv install`で必要パッケージをインストールして下さい。

実行は`pipenv run python3 main.py`です。

## LICENSE
This source code is released under MIT license.
