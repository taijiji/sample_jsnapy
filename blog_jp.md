#JSNApy使ってみた
Juniper社の公式手順書作成ツールであるJSNAPyを使ってみます。

#背景
手順書作成は手動で作成されることが主

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
公式ドキュメント
https://github.com/juniper/jsnapy/wiki

https://github.com/juniper/jsnapy
Installation:
You can install and run JSNAPy by following installation steps mentioned in wiki:
https://github.com/juniper/jsnapy/wiki
Some reference:
Source Code: https://github.com/juniper/jsnapy
Wiki: https://github.com/juniper/jsnapy/wiki
Examples: https://github.com/Juniper/jsnapy/tree/master/samples

--snap : snapショットを取得
--check : ２つのsnapを比較して評価
--snapshot : 既存snapと、現在のコンフィグとを比較して、評価
評価するための関数
https://github.com/Juniper/jsnapy/wiki

PyEz 

JUNOS 11.4よりサポート
公式APIドキュメント
http://junos-pyez.readthedocs.io/en/2.0.1/

- いい記事
Juniper JUNOS PyEz (python library)を試すメモ 1 ~PyEz概要~
http://qiita.com/hiromiarts/items/aade90a161acd63bc8ed

Juniper JUNOS PyEz (python library)を試すメモ 2 ~PyEzによる情報取得~
http://qiita.com/hiromiarts/items/f44ec5eab6a7508f050a#_reference-52d108e43bb587187d80

Juniper JUNOS PyEz (python library)を試すメモ ３ ~PyEzによる設定変更~
http://qiita.com/hiromiarts/items/ccaaeed4709d9961cdcc#_reference-75abb91c856511fe5b64




Configuration Process
lock() - コンフィグレーションのロック
load() - 設定の読込 (rollback()やrescue()による設定戻しも可)
commit() - 設定の反映
unlock() - コンフィグレーションのアンロック


load merge : 既に入力されているcandidateコンフィグに追加/マージした上で、loadする (commit未実施)
load overload : 既に入力されているcandidateコンフィグを消去した上で、loadする (commit未実施)
load replace : 専用の「replace:」タグを付けた部分のみを上書きして、loadする (commit未実施)
load (default) : load replace
http://www.infraeye.com/study/junos4.html
公式ページ: Loading a Configuration from a File
https://www.juniper.net/documentation/en_US/junos12.3/topics/task/configuration/junos-software-configuration-file-loading.html
load option overlide/merge/replaceサンプル
https://www.juniper.net/documentation/en_US/junos12.3/topics/example/junos-software-config-file-loading.html#id-10728250



# 検証構成
firefly1
- ge-0/0/0: DHCP
- ge-0/0/1: 192.168.33.16/24
firefly2
- ge-0/0/0: DHCP
- ge-0/0/1: 192.168.33.17/24
MacBook Air(host)
- vboxnet0: 192.168.33.1

メモ
firefly２台立ち上げると、Memoryが合計7.5Gも使ってしまい、
8.0G memory Macbook Aireではギリギリ。最初はPC固まった。
不要はプロセスは閉じて、2Gx2=4Gほどメモリ空きを確保してから実施しましょう

試行錯誤メモ
- VirtualBoxのネットワーク設定がNATだとうまくいかない
  昨日HostOnlyAdaptにしたら、Firefly -> MacへのpingだけOKになった。
- private_network, inte_netでも失敗。通信もなにもできない
- trust networkに追加したが、通信もなにもできない
- セグメントを変えてみる private : 192.168.34.xにしてみる
    - あれ、そもそもホストOS側に192.168.34.xのIPが振られてない。そういうものか
    - ダメ。状況変わらず
- public_network にしてみた。
    - ダメ。
- そもそもゲスト-ホスト間で通信できないのが、Vagrantとしておかしい。
    - firefly設定ミスによるものか
    - junos-vagrantがそもそもおかしい


参考にしたVagrant設定ブログ
http://labs.septeni.co.jp/entry/20140707/1404670069


fireflyではVagrantFileで作ったinterfaceはデフォルトuntrustになっていて、通信できないようにしされている
とりあえずtrustにしてあげることで、全通信を許可させる
set security zones security-zone trust interfaces ge-0/0/1
set security zones security-zone trust interfaces ge-0/0/0

set security zones security-zone trust interfaces ge-0/0/1.0 host-inbound-traffic system-services ssh
set security zones security-zone trust interfaces ge-0/0/1.0 host-inbound-traffic system-services ping
# これいれて、やっと通信できた。。。

#初期設定
set system root-authentication plain-text-password
set system time-zone Asia/Tokyo
set system login user user1 class super-user
set system login user user1 authentication plain-text-password

# Mac側での準備
pip install junos-eznc
```:うまくいかない
*********************************************************************************

Could not find function xmlCheckVersion in library libxml2. Is libxml2 installed?

Perhaps try: xcode-select --install

*********************************************************************************

error: command 'cc' failed with exit status 1

----------------------------------------
Cleaning up...
Command /usr/bin/python -c "import setuptools, tokenize;__file__='/private/var/folders/1z/116vjww53yz3zf0nvbsp6dvm0000gn/T/pip_build_taiji/lxml/setup.py';exec(compile(getattr(tokenize, 'open', open)(__file__).read().replace('\r\n', '\n'), __file__, 'exec'))" install --record /var/folders/1z/116vjww53yz3zf0nvbsp6dvm0000gn/T/pip-9prVRB-record/install-record.txt --single-version-externally-managed --compile failed with error code 1 in /private/var/folders/1z/116vjww53yz3zf0nvbsp6dvm0000gn/T/pip_build_taiji/lxml
Storing debug log for failure in /Users/taiji/Library/Logs/pip.log
```

これでうまくいった。
xcode-select --install                                                

# 問題: sshパスワード認証でログインしようとすると、mac側に公開鍵を聞かれる。ツールでアクセスできない。
mac側の秘密鍵をキーチェインに登録しておく(Mac限定)
これではだめでした。
ssh-add -K ~/.ssh/id_rsa

ここに足してみることでいけた

vi /Users/taiji/.ssh/config
Host 192.168.34.16
  HostName 192.168.34.16
  IdentityFile      /Users/taiji/.vagrant.d/insecure_private_key
  User user1
  PasswordAuthentication no

ただしまだツールではうまくアクセスできない

Juniperドキュメント (ただしうまくアクセスできず)
http://forums.juniper.net/t5/Automation/Scripting-How-To-Junos-NETCONF-and-SSH-Part-2/ta-p/279102


```馬淵ツールの例
import os
import paramiko
from scp import SCPClient
# ssh config file lookup
def scp_get(FILENAME):
    try:
        config_file = os.path.join(os.getenv('HOME'), '.ssh/config')
        ssh_config = paramiko.SSHConfig()
        ssh_config.parse(open(config_file, 'r'))
        lkup = ssh_config.lookup('jaboten')

        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(
            lkup['hostname'],
            username=lkup['user'],
            password='****',
            key_filename=lkup['identityfile'],
            sock=paramiko.ProxyCommand(lkup['proxycommand'])
        )
        scp = SCPClient(ssh.get_transport())
        scp.get('/home/t-mabuchi/trafficwatcher/traffic_data/%s'%FILENAME)

        scp.close()
        ssh.close()
        return True
    except:
        raise
```

あれ、configcollector(Exscriptを利用)はすんなり取れる。。。

ルータに設定足してみる。だめ。。
```
set system services netconf ssh port 22
```

#解決した！！！！
pdbでデバッグで潜り続けていると、ncclientのポートでTCP830を使った通信をしていることが判明した
```
> /Library/Python/2.7/site-packages/ncclient/transport/ssh.py(363)connect()
-> sock.connect(sa)

(Pdb) p sa
('192.168.34.16', 830)
```

RFC読むと、TCP830が正式なNETCONF over SSHの割当ポートらしい。
https://trac.tools.ietf.org/html/rfc4742
In order to allow NETCONF traffic to be easily identified and
   filtered by firewalls and other network devices, NETCONF servers MUST
   default to providing access to the "netconf" SSH subsystem only when
   the SSH session is established using the IANA-assigned TCP port
   <830>.  Servers SHOULD be configurable to allow access to the netconf
   SSH subsystem over other ports.

PyEZの挙動としては、デフォルトTCP830ポートを使ってるっぽい
('192.168.34.16', 830)

怪しいサイトには、以下のように書いている。
「デフォルトのNETCONF TCPポート830，または標準的なSSH TCPポート22のどちらかで，NETCONFを有効化する」
http://itdoc.hitachi.co.jp/manuals/3021/3021324220/NNMS0039.HTM

小島さんブログより
http://codeout.hatenablog.com/entry/2014/10/30/224405
Firefly は, SSH ポート(22/tcp) もしくはNETCONF ポート(830/tcp) で登録できる.

コマンド
vagrant ssh firefly1
vagrant ssh firefly2
ping 192.168.33.16
ping 192.168.33.17
ping 192.168.33.15
ping 192.168.33.1

ping 192.168.34.16
ping 192.168.34.17

# インストール
環境
- CetOS
- Juniper MX Series

```
jsnapy --snap pre -f sample/config_check.yml
```


# 実行

作成したファイル

```:sample/config_check.yml
hosts:
  - device:  xxx.xxx.xxx.xxx
    username : user1
    passwd: abcdef
tests:
  - /home/t-tsuchiya/sample_JSNAPy/sample/test_bgp_neighbor.yml
```

```:sample/test_bgp_neighbor.yml
test_bgp_neighbor:
  - command: show bgp neighbor
```

実行する

```
jsnapy --snap snap01 -f sample/config_check.yml


jsnapy --snap snap02 -f sample/config_check.yml
```

デフォルトでは/etc/jsnapy/snapshots ディレクトリにファイルが生成される
(jsnapy.cfgで生成場所を変更できるらしい)

```
 ls -al /etc/jsnapy/snapshots/
合計 52
drwxrwxrwx 2 root       root         121  9月 27 08:51 .
drwxrwxrwx 5 root       root          87  9月 26 17:34 ..
-rw-rw-r-- 1 t-tsuchiya t-tsuchiya 20984  9月 27 08:50 202.247.123.108_snap01_show_bgp_neighbor.xml
-rw-rw-r-- 1 t-tsuchiya t-tsuchiya 20984  9月 27 08:51 202.247.123.108_snap02_show_bgp_neighbor.xml
-rwxrwxrwx 1 root       root         146  9月 26 17:34 README
```

PRC形式で出力される。
show bgp neighbor コマンドで取得できる情報はすべて格納されていそうだ。
```
<bgp-information>
<bgp-peer style="detail">
<peer-address>10.160.21.2+34245</peer-address>
<peer-as>65500</peer-as>
<local-address>10.160.21.1+179</local-address>
<local-as>65500</local-as>
<description>dos_genie</description>
<peer-type>Internal</peer-type>
<peer-state>Established</peer-state>
<peer-flags>Sync</peer-flags>
<last-state>OpenConfirm</last-state>
<last-event>RecvKeepAlive</last-event>
<last-error>None</last-error>
<bgp-option-information>
<export-policy>
genie_export1
</export-policy>
<bgp-options>Preference HoldTime LogUpDown AddressFamily Refresh Confed</bgp-options>
<bgp-options2>DropPathAttributes</bgp-options2>
<bgp-options-extended/>
<address-families>inet-unicast inet6-unicast</address-families>
<drop-path-attributes> 128</drop-path-attributes>
<holdtime>90</holdtime>
<preference>170</preference>
</bgp-option-information>
<flap-count>1</flap-count>
<last-flap-event>RecvNotify</last-flap-event>
<bgp-error>
<name>Cease</name>
<send-count>0</send-count>
<receive-count>1</receive-count>
</bgp-error>
<peer-id>172.16.55.28</peer-id>
<local-id>10.160.99.1</local-id>
<active-holdtime>90</active-holdtime>
<keepalive-interval>30</keepalive-interval>
<group-index>2</group-index>
<peer-index>0</peer-index>
<bgp-bfd>
<bfd-configuration-state>disabled</bfd-configuration-state>
<bfd-operational-state>down</bfd-operational-state>
</bgp-bfd>
<peer-restart-nlri-configured>inet-unicast inet6-unicast</peer-restart-nlri-configured>
<nlri-type-peer>inet-unicast inet-vpn-unicast inet6-unicast inet-flow inet-vpn-flow</nlri-type-peer>
<nlri-type-session>inet-unicast inet6-unicast</nlri-type-session>
<peer-no-refresh/>
<peer-stale-route-time-configured>300</peer-stale-route-time-configured>
<peer-no-restart/>
<peer-no-helper/>
<peer-4byte-as-capability-advertised>65500</peer-4byte-as-capability-advertised>
<peer-addpath-not-supported/>
<bgp-rib style="detail">
<name>inet.0</name>
<rib-bit>10001</rib-bit>
<bgp-rib-state>BGP restart is complete</bgp-rib-state>
<send-state>in sync</send-state>
<active-prefix-count>0</active-prefix-count>
<received-prefix-count>0</received-prefix-count>
<accepted-prefix-count>0</accepted-prefix-count>
<suppressed-prefix-count>0</suppressed-prefix-count>
<advertised-prefix-count>4</advertised-prefix-count>
</bgp-rib>
<bgp-rib style="detail">
<name>inet6.0</name>
<rib-bit>20001</rib-bit>
<bgp-rib-state>BGP restart is complete</bgp-rib-state>
<send-state>in sync</send-state>
<active-prefix-count>0</active-prefix-count>
<received-prefix-count>0</received-prefix-count>
<accepted-prefix-count>0</accepted-prefix-count>
<suppressed-prefix-count>0</suppressed-prefix-count>
<advertised-prefix-count>4</advertised-prefix-count>
</bgp-rib>
<last-received>12</last-received>
<last-sent>22</last-sent>
<last-checked>72</last-checked>
<input-messages>10111</input-messages>
<input-updates>0</input-updates>
<input-refreshes>0</input-refreshes>
<input-octets>192167</input-octets>
<output-messages>11085</output-messages>
<output-updates>9</output-updates>
<output-refreshes>0</output-refreshes>
<output-octets>211002</output-octets>
<bgp-output-queue>
<number>0</number>
<count>0</count>
</bgp-output-queue>
<bgp-output-queue>
<number>1</number>
<count>0</count>
</bgp-output-queue>
</bgp-peer>
<bgp-peer style="detail">
<peer-address>10.160.43.2+179</peer-address>
<peer-as>65100</peer-as>
<local-address>10.160.43.1+64868</local-address>
<local-as>65518</local-as>
<description>dos_customer</description>
<peer-type>External</peer-type>
<peer-state>Established</peer-state>
<peer-flags>Sync</peer-flags>
<last-state>OpenConfirm</last-state>
<last-event>RecvKeepAlive</last-event>
<last-error>None</last-error>
<bgp-option-information>
<export-policy>
as65100-export1
</export-policy>
<import-policy>
as65100-import1
</import-policy>
<bgp-options>Preference HoldTime LogUpDown AddressFamily PeerAS Refresh</bgp-options>
<bgp-options2>DropPathAttributes</bgp-options2>
<bgp-options-extended/>
<address-families>inet-unicast</address-families>
<drop-path-attributes> 128</drop-path-attributes>
<holdtime>90</holdtime>
<preference>170</preference>
</bgp-option-information>
<flap-count>0</flap-count>
<peer-id>172.32.160.1</peer-id>
<local-id>10.160.96.1</local-id>
<active-holdtime>90</active-holdtime>
<keepalive-interval>30</keepalive-interval>
<group-index>3</group-index>
<peer-index>0</peer-index>
<bgp-bfd>
<bfd-configuration-state>disabled</bfd-configuration-state>
<bfd-operational-state>down</bfd-operational-state>
</bgp-bfd>

```


```
jsnapy --check snap01 snap02 -f sample/config_check.yml
```

作成されたスナップショット差分をjsnapy --checkコマンドでチェックしてみる。
snap01などのように、作成時に指定したsnapshot名で呼び出しが可能。

実行してみると下記のようにたくさんエラーがでる。
どの部分で発生しているかわからずにたくさん怒られてた。。
（実際はBGPのタイマーやribの変化を全部抽出している）


```
jsnapy --check snap01 snap02 -f sample/config_check.yml


Difference in pre and post snap file
0] <last-received> value different:
    Pre node text: '12'    Post node text: '23'    Parent node: <bgp-peer>
1] <last-sent> value different:
    Pre node text: '22'    Post node text: '7'    Parent node: <bgp-peer>
2] <last-checked> value different:
    Pre node text: '72'    Post node text: '23'    Parent node: <bgp-peer>
3] <input-messages> value different:
    Pre node text: '10111'    Post node text: '10112'    Parent node: <bgp-peer>
4] <input-octets> value different:
    Pre node text: '192167'    Post node text: '192186'    Parent node: <bgp-peer>
5] <output-messages> value different:
    Pre node text: '11085'    Post node text: '11087'    Parent node: <bgp-peer>
6] <output-octets> value different:
    Pre node text: '211002'    Post node text: '211040'    Parent node: <bgp-peer>
7] <last-received> value different:
    Pre node text: '16'    Post node text: '28'    Parent node: <bgp-peer>
8] <last-sent> value different:
    Pre node text: '22'    Post node text: '7'    Parent node: <bgp-peer>
9] <last-checked> value different:
    Pre node text: '38'    Post node text: '79'    Parent node: <bgp-peer>
10] <input-messages> value different:
    Pre node text: '11326'    Post node text: '11327'    Parent node: <bgp-peer>
11] <input-octets> value different:
    Pre node text: '215226'    Post node text: '215245'    Parent node: <bgp-peer>
12] <output-messages> value different:
    Pre node text: '11216'    Post node text: '11218'    Parent node: <bgp-peer>
13] <output-octets> value different:
    Pre node text: '213339'    Post node text: '213377'    Parent node: <bgp-peer>
14] <last-received> value different:
    Pre node text: '6'    Post node text: '21'    Parent node: <bgp-peer>
15] <last-sent> value different:
    Pre node text: '8'    Post node text: '24'    Parent node: <bgp-peer>
16] <last-checked> value different:
    Pre node text: '50'    Post node text: '12'    Parent node: <bgp-peer>
17] <input-messages> value different:
    Pre node text: '2379'    Post node text: '2380'    Parent node: <bgp-peer>
18] <input-octets> value different:
    Pre node text: '45337'    Post node text: '45356'    Parent node: <bgp-peer>
19] <output-messages> value different:
    Pre node text: '2347'    Post node text: '2348'    Parent node: <bgp-peer>
20] <output-octets> value different:
    Pre node text: '44716'    Post node text: '44735'    Parent node: <bgp-peer>
21] <last-received> value different:
    Pre node text: '3'    Post node text: '15'    Parent node: <bgp-peer>
22] <last-sent> value different:
    Pre node text: '23'    Post node text: '10'    Parent node: <bgp-peer>
23] <last-checked> value different:
    Pre node text: '20'    Post node text: '61'    Parent node: <bgp-peer>
24] <input-messages> value different:
    Pre node text: '11210'    Post node text: '11211'    Parent node: <bgp-peer>
25] <input-octets> value different:
    Pre node text: '213188'    Post node text: '213207'    Parent node: <bgp-peer>
26] <output-messages> value different:
    Pre node text: '11203'    Post node text: '11205'    Parent node: <bgp-peer>
27] <output-octets> value different:
    Pre node text: '213271'    Post node text: '213309'    Parent node: <bgp-peer>
28] <last-received> value different:
    Pre node text: '4'    Post node text: '19'    Parent node: <bgp-peer>
29] <last-sent> value different:
    Pre node text: '12'    Post node text: '24'    Parent node: <bgp-peer>
30] <last-checked> value different:
    Pre node text: '24'    Post node text: '65'    Parent node: <bgp-peer>
31] <input-messages> value different:
    Pre node text: '11326'    Post node text: '11327'    Parent node: <bgp-peer>
32] <input-octets> value different:
    Pre node text: '215272'    Post node text: '215291'    Parent node: <bgp-peer>
33] <output-messages> value different:
    Pre node text: '11215'    Post node text: '11216'    Parent node: <bgp-peer>
34] <output-octets> value different:
    Pre node text: '213493'    Post node text: '213512'    Parent node: <bgp-peer>
35] <last-received> value different:
    Pre node text: '15'    Post node text: '1'    Parent node: <bgp-peer>
36] <last-sent> value different:
    Pre node text: '23'    Post node text: '7'    Parent node: <bgp-peer>
37] <last-checked> value different:
    Pre node text: '40'    Post node text: '81'    Parent node: <bgp-peer>
38] <input-messages> value different:
    Pre node text: '2375'    Post node text: '2377'    Parent node: <bgp-peer>
39] <input-octets> value different:
    Pre node text: '45243'    Post node text: '45281'    Parent node: <bgp-peer>
40] <output-messages> value different:
    Pre node text: '2346'    Post node text: '2348'    Parent node: <bgp-peer>
41] <output-octets> value different:
    Pre node text: '44798'    Post node text: '44836'    Parent node: <bgp-peer>
42] <last-received> value different:
    Pre node text: '2'    Post node text: '14'    Parent node: <bgp-peer>
43] <last-sent> value different:
    Pre node text: '22'    Post node text: '7'    Parent node: <bgp-peer>
44] <last-checked> value different:
    Pre node text: '14'    Post node text: '55'    Parent node: <bgp-peer>
45] <input-messages> value different:
    Pre node text: '11207'    Post node text: '11208'    Parent node: <bgp-peer>
46] <input-octets> value different:
    Pre node text: '213041'    Post node text: '213060'    Parent node: <bgp-peer>
47] <output-messages> value different:
    Pre node text: '11201'    Post node text: '11203'    Parent node: <bgp-peer>
48] <output-octets> value different:
    Pre node text: '213332'    Post node text: '213370'    Parent node: <bgp-peer>
------------------------------- Final Result!! -------------------------------
Total No of tests passed: 0
Total No of tests failed: 1
Overall Tests failed!!!
```


今度はjsnapy --diff コマンドで差分を見てみる
実際どの部分に差分が発生しているのか、人間に見やすい形で表示してくれる。
とはいえRPC形式なので見づらいか


```
jsnapy --diff snap01 snap02 -f sample/config_check.yml


************************** Device: 202.247.123.108 **************************
Tests Included: test_bgp_neighbor
************************* Command: show bgp neighbor *************************
/etc/jsnapy/snapshots/202.247.123.108_snap01_show_bgp_neighbor.xml /etc/jsnapy/snapshots/202.247.123.108_snap02_show_bgp_neighbor.xml
<received-prefix-count>0</received-prefix-count>  <received-prefix-count>0</received-prefix-count>
<accepted-prefix-count>0</accepted-prefix-count>  <accepted-prefix-count>0</accepted-prefix-count>
<suppressed-prefix-count>0</suppressed-prefix-co  <suppressed-prefix-count>0</suppressed-prefix-co
unt>                                              unt>
<advertised-prefix-count>4</advertised-prefix-co  <advertised-prefix-count>4</advertised-prefix-co
unt>                                              unt>
</bgp-rib>                                        </bgp-rib>
<last-received>12</last-received>                 <last-received>23</last-received>
<last-sent>22</last-sent>                         <last-sent>7</last-sent>
<last-checked>72</last-checked>                   <last-checked>23</last-checked>
<input-messages>10111</input-messages>            <input-messages>10112</input-messages>
<input-updates>0</input-updates>                  <input-updates>0</input-updates>
<input-refreshes>0</input-refreshes>              <input-refreshes>0</input-refreshes>
<input-octets>192167</input-octets>               <input-octets>192186</input-octets>
<output-messages>11085</output-messages>          <output-messages>11087</output-messages>
<output-updates>9</output-updates>                <output-updates>9</output-updates>
<output-refreshes>0</output-refreshes>            <output-refreshes>0</output-refreshes>
<output-octets>211002</output-octets>             <output-octets>211040</output-octets>
<bgp-output-queue>                                <bgp-output-queue>
<number>0</number>                                <number>0</number>
<count>0</count>                                  <count>0</count>
</bgp-output-queue>                               </bgp-output-queue>
<bgp-output-queue>                                <bgp-output-queue>
```



#ケーススタディ

ネットワーク作業シナリオ

1. Pubril Peerを新規作成
  - Router CPU/Memory Usage
  - IF 確認
  - ping IP address
  - Traceroute
  - Traffic Check
  - show bgp summary
  - show bgp neihbor
  - スクリプトチェック
    - Policyがないこと
    - BGP 設定がないこと
  - 設定
    - Policy
    - BGP neighber
    - Filter open
  - スクリプトチェック
    - Policyが入っていること
    - BGP 設定がはいっていること
  - show bgp summary
  - show bgp neighbor recived route
  - show bgp neighbor advertised route
  - Traffic check
  - Traceroute
  - Ping Test
  - Router CPU/Memory Usage


2. Private Peerを新規作成
  - 1. に加えて以下を追加
  - 設定
   - Interface
   - Interface up/donw check
   - ping IP

3. GWルータを新規構築
  - OSPF check
  - 設定
    - Interface
    - OSPF
    - iBGP
     - RR




snapshot出力ファイルの設定を変更したい
- /etc/jsnapy/snapshots/ の出力先ディレクトリを変更したい(作業順や対象がごちゃごちゃになる)
- ファイル名に日付,日時を入れたい (202.247.123.108_snap02_show_bgp_neighbor.xmlだといつの結果かわからないよね。)
- snap名とファイル名が紐付いてないのはどう定義するのがベストか考える必要がある

時間差でupしてくるようなものについてはどうチェックするか？
10秒単位で見に行く？

実践的なシチュエーションを考えてみる
- １台のルータを設定作業する場合
  - 設定はどうする？CLI? 別の自動ツール？ PyEzでやるならスクリプト？
  - JSNAPyコマンドがよい or Python Scriptがよいかは、自分なりの結論を出すべき。
- 複数台のルータを同時に作業する場合
 - 複数台のときはどうするのかいな？
 - でも複数台のルータをバージョン管理したいケースはあるはず。
- 異なるベンダー装置で作業する場合
 - 運用者としての視点で必須
 - JSNAPyではおそらく無理なので、現実的な方法を考察/提案
 - そのサンプルコードまで実現できてるとGood


#おまけ
JSNAPyの裏はPyEZというJuniper公式Netconfツールが動いている。
この仕組みを流用すれば、異なるデバイスで動かくことが可能。

たとえば、フロントエンドをJSNAPy、裏をNapalmにすることで
全部の機器を同じ手順書で実装可能、とか
