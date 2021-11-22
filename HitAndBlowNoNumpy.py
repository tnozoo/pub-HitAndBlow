import os;
import random;
import argparse;

MSG_QUESTION = '%d 回目: さぁどうぞ！ Type [q] to quit.';
MSG_ANSWER = '正解は %s でした';
MSG_HINT = '%d Hit, %d Blow';
MSG_ERROR1 = '数字%d桁すべて異なる数字を入力しなさい';
MSG_OK = '%d 回で正解しました！';
MSG_PARAM = '3から6桁位の間がよろしいかと';

# WSL（Debian），Mac であれば os.name は 'posix'
# Windows であれば os.name は 'nt'
CLEAR = 'clear';
if os.name == 'nt':
    CLEAR = 'cls'

# コマンドライン引数の処理には，argparse.ArgumentParser を使う
# 桁数のデフォルトを4にして，'-k' または '--keta' で引数を与えられるようにする
def get_args():
    parser = argparse.ArgumentParser();
    parser.add_argument('--keta', '-k', help = '桁数', type = int, default = 4);
    args = parser.parse_args();
    return(args)

# 入力した文字に同一文字がないかどうか
def checkSame(v):
    for i in range(0, len(v)):
        if v.count(v[i: i + 1]) > 1:
            return False;
    return True;

# 入力した文字の桁数（＝文字数）がゲームの桁数と同じかどうか
def checkKeta(keta, v):
    return (len(v) == keta);

# 引数が int かどうか判断する
# int であれば True，int でなければ False を返す
def checkInt(v):
    # int 関数で int への型変換を行う
    # 行う際に型変換エラーをキャッチした場合は数字ではないと判断する
    r = False;
    try:
        _ = int(v);
        r = True;
    except ValueError:
        pass;
    return r;

def checkGame(keta, v, answer):
    r = False;
    hit = 0;
    blow = 0;
    for i in range(0, keta):
        tgt = int(v[i: i + 1]);
        if answer[i] == tgt:
            hit += 1;
        elif answer.count(tgt) > 0:
            blow += 1;
    if hit == keta:
        r = True;
    return (r, hit, blow);

def doGame(keta, answer):
    os.system(CLEAR);
    print('*** Hit And Blow (%d 桁) ***' % (keta));

    # 試行回数
    seq = 1;

    while True:
        print(MSG_QUESTION % (seq));
        v = input('> ');
        if v == 'q':
            print(MSG_ANSWER % (answer));
            break;
        elif v == 'answer':
            print(answer);
            continue;
        else:
            if ((not checkKeta(keta, v)) or (not checkInt(v)) or (not checkSame(v))):
                print(MSG_ERROR1 % (keta));
                continue;
            hint = checkGame(keta, v, answer);
            if hint[0]:
                print(MSG_OK % (seq));
                break;
            else:
                print(MSG_HINT % (hint[1], hint[2]));
        seq += 1;

def main(keta):
    # 正解の数字を作る
    answer = random.sample(range(0, 10), keta);

    # ゲーム開始
    doGame(keta, answer);

if __name__ == '__main__':
    # コマンドライン引数を確認する
    args = get_args()
    keta = args.keta

    # コマンドライン引数に対するエラー処理を行う
    if keta < 3 or keta > 6:
        print(MSG_PARAM);
    else:
        # ゲームのメイン関数を呼び出す
        main(keta);

