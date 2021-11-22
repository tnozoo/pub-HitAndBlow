# 【Python】数字当てゲーム（ヒットアンドブロー Hit and Blow）を作ってみる

## はじめに

はるか昔，ボードゲームでやったことがある
何色かの色ピンを使ったボードゲームだったような…
場所があっていたら黒ピン，場所は違うけど色があっていたら白ピンを立てる
確か，そんなような…

家族がピンの代わりに数字でやる，現代版のやり方を教えてくれて，
少しはまっている

調べると，ヒットアンドブロー（Hit and Blow）というらしい
はるか昔の色ピンを使ったゲームは何ていう名のゲームだったんだろう…

Python で作ってみたらどうだろうと考えたら，
割と簡単にいけるんじゃないかと思ったので，作ってみる

## ルール

4桁の数字行う場合のルールを書くと次のようだ

- 親が決めた4桁の正解数字（使ってよい数字は0から9まで）を，子が当てる
- 子が予想した数字を正解数字と比較して，Hit 数と Blow 数を言う
- 数字とその数字が使われている場所（桁）があっている場合は Hit
- 数字はあっているが，数字が使われている場所（桁）があっていない場合は Blow
- 例えば，正解が「2578」のとき，「1270」は 1 Hit 1 Blow となる
- 子が4 Hitの数字を予想するまで繰り返す（4 Hit になったらゲーム終了）

## 要件

Python で作るにあたっての要件を決めておこう

- 3桁から6桁の数字で遊べること
- 桁数はゲーム起動時のコマンドライン引数で与えられること
- 途中で，ギブアップ（ゲーム終了）できること
- 何回で正解したか分かること

## コマンドライン引数（argparse.ArgumentParser）

コマンドライン引数の処理には，argparse.ArgumentParser を使う
桁数のデフォルトを4にして，'-k' または '--keta' で引数を与えられるようにする

```python:test01.py
import argparse;

parser = argparse.ArgumentParser();
parser.add_argument('--keta', '-k', help = '桁数', type = int, default = 4);
args = parser.parse_args();
print(args.keta);
```

test01.py を動かすと次のようだ

引数が何もない場合はデフォルトの 4

```python
❯ python test01.py
4
```

'-k' または '--keta' を与えた場合は，引数で与えた値

```python
❯ python test01.py -k 5
5

❯ python test01.py --keta 2
2
```

'-k' または '--keta' を指定して数字以外を与えた場合はエラー

```python
❯ python test01.py -k w
usage: test01.py [-h] [--keta KETA]
test01.py: error: argument --keta/-k: invalid int value: 'w'
```

'-k' または '--keta' を指定して値を指定しない場合はエラー

```python
❯ python test01.py -k
usage: test01.py [-h] [--keta KETA]
test01.py: error: argument --keta/-k: expected one argument
```

'-m' のような定義されていない引数の場合はエラー

```python
❯ python test01.py -m 3
usage: test01.py [-h] [--keta KETA]
test01.py: error: unrecognized arguments: -m 3
```

'-h' または '--help' で使用法

```python
❯ python test01.py -h
usage: test01.py [-h] [--keta KETA]

optional arguments:
  -h, --help            show this help message and exit
  --keta KETA, -k KETA  桁数
```

## 標準入力（input）

input 関数を使えばよい
プロンプトとして，'> ' を表示して，
プレイヤーが入力した数字を取得する場合は次のようにすればよい

```python
v = input('> ');
```

## ランダムな数列（numpy.random.shuffle）

numpy.arange を使って，0から始まる要素数10個の数列を公差1で作る

```python
import numpy as np;
_seq = np.arange(0, 10, 1);
```

そして，numpy.random.shuffle を使って，順番をランダムに並び変える

```python
np.random.shuffle(_seq);
```

正解の数字として，先頭の4要素を取得する

```python
answer = _seq[0: 4];
```

## 数字かどうかのチェック（try except ValueError）

int 関数で int への型変換を行う
行う際に型変換エラーをキャッチした場合は数字ではないと判断する

checkInt という関数を用意し，引数が int かどうか判断する
int であれば True，int でなければ False を返す

```python
def checkInt(v):
    r = False;
    try:
        _ = int(v);
        r = True;
    except ValueError:
        pass;
    return r;
```

## 文字の重複チェック（count）

プレイヤーが入力した文字に重複があればエラーとしたい
入力した文字をスライス [start: end] を count で確認すればよい
必ず1個はあるので，1より大きければ重複だ

```python
def checkSame(v):
    for i in range(0, len(v)):
        if v.count(v[i: i + 1]) > 1:
            return False;
    return True;
```

## numpy 配列の要素に条件を満たすものがあるかどうかのチェック（numpy.count_nonzero）

numpy.count_nonzero はデフォルトでは 0 以外の要素数を返すが，
条件式にしてあげれば，その条件を満たす要素数を返す

```python
>>> import numpy as np;
>>> _seq = np.arange(0, 10, 1);
>>> np.random.shuffle(_seq);
>>> answer = _seq[0: 4];
>>> answer;
array([7, 6, 9, 1])
>>> np.count_nonzero(answer);
4 ## 0 以外の要素数を返している
>>> np.count_nonzero(answer == 9);
1 ## 条件（数字の9）を満たす要素数を返している
```

## OS判定（os.name）

ゲームを起動した直後に画面のクリアを行いたいと思ったが，
画面クリアコマンドがOSにより違う
WSL や Mac は clear
Windows は cls
なので，ゲームを動かす環境により，コマンドを出しわける必要がある

Python で環境の違いでコマンドを出しわけたいような場合は，
os.name で判断ができる

WSL（Debian），Mac

```python
>>> import os;
>>> os.name
'posix'
```

Windows

```python
>>> import os;
>>> os.name
'nt'
```

なので，次のように CLEAR 変数にコマンド名を入れるようにすればいいだろう

```python
CLEAR = 'clear';
if os.name == 'nt':
    CLEAR = 'cls'
```

## さいごに

- 簡単だと思ったが，調べてみないと実現しないことが多々あった
- コンソール画面で行うゲームも面白いが，やはり人と対戦でやったほうが面白い！
