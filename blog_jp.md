#JSNApy使ってみた
Juniper社の公式手順書作成ツールであるJSNAPyを使ってみます。

#背景
手順書作成は手動でおこわられることが主

JSNAPyでできること
- ネットワークデバイスの状態定義
- スナップショットの取得
- 状態検査
- レポートの自動生成(独自フォーマット？)

サポートしているネットワークプロトコル
- BGP
- OSPF
- ICMP


JSNAPy
https://github.com/juniper/jsnapy
Installation:
You can install and run JSNAPy by following installation steps mentioned in wiki:
https://github.com/juniper/jsnapy/wiki
Some reference:
Source Code: https://github.com/juniper/jsnapy
Wiki: https://github.com/juniper/jsnapy/wiki
Examples: https://github.com/Juniper/jsnapy/tree/master/samples


# インストール
環境
- CetOS
- Juniper MX Series

```
%  sudo pip install jsnapy
```



#おまけ
JSNAPyの裏はPyEZというJuniper公式Netconfツールが動いている。
この仕組みを流用すれば、異なるデバイスで動かくことが可能。

たとえば、フロントエンドをJSNAPy、裏をNapalmにすることで
全部の機器を同じ手順書で実装可能、とか