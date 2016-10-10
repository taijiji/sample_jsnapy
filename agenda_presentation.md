#タイトル
JSNAPyとPyEZで作る次世代ネットワーク運用の可能性

#発表者
ビッグローブ株式会社　土屋　太二

#発表概要
Chef, Ansibleに代表される構成管理ツールや、Serverspecに代表されるサーバテストツールの登場により、
サーバインフラの運用現場ではここ数年で飛躍的に自動化が進んできました。
しかしネットワークインフラの運用については、有効な手段に乏しく依然として自動化が進んでいないのが実情です。

本発表では、Juniper公式OSSであるネットワーク状態管理ツール JSNAPy(https://github.com/Juniper/jsnapy)と
ネットワーク設定ライブラリであるJUNOS PyEZ(http://www.juniper.net/techpubs/en_US/release-independent/junos-pyez/information-products/pathway-pages/index.html)
を使い、ISPでよくあるネットワーク設定作業を例に、次世代ネットワーク運用の形を提案します。

#発表の流れ
- 自己紹介 (1 min)
- ネットワークオペレーションを自動化するために必要なこと (2 min)
- JSNAPy概要 / サンプルコード (3 min)
- PyEZ 概要 / サンプルコード (3 min)
- ISPでのネットワーク設定作業の例、確認項目 (3 min)
    - Private Peering
    - ルータ新規構築 (時間次第でカット)
- JSNAPy, PyEZでISPネットワーク作業を実現 (5 min)
    - パターン1: ネットワーク運用者によるCLIを使った設定作業の半自動化
    - パターン2: Pythonスクリプトによる設定作業の全自動化
    - パターン3: Ansible or Jenkinsによる設定作業の全自動化(時間次第でカット)
- 現状における課題 (2 min)
- まとめ (1 min)
- 質疑応答(5 min)