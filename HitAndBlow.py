import os;
import numpy as np;
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
def is_unique(player_string):
    # 集合にして，長さが変わらなければ同一文字なし（ユニーク）
    # 長さが変われば，同一文字あり
    return (len(set(player_string)) == len(player_string));

# 入力した文字の桁数（＝文字数）がゲームの桁数と同じかどうか
def is_correct_keta(keta, player_string):
    return (len(player_string) == keta);

# 引数が int かどうか判断する
# int であれば True，int でなければ False を返す
def is_int(player_string):
    # int 関数で int への型変換を行う
    # 行う際に型変換エラーをキャッチした場合は数字ではないと判断する
    try:
        int(player_string);
        return True;
    except ValueError:
        return False;

def hit_and_blow(keta, player_string, answer):
    r = False;
    hit = 0;
    blow = 0;
    for i in range(0, keta):
        tgt = int(player_string[i: i + 1]);
        if answer[i] == tgt:
            hit += 1;
        elif np.count_nonzero(answer == tgt) > 0:
            blow += 1;
    if hit == keta:
        r = True;
    return (r, hit, blow);

def start_game(keta, answer):
    os.system(CLEAR);
    print('*** Hit And Blow (%d 桁) ***' % (keta));

    # 試行回数
    seq = 1;

    while True:
        print(MSG_QUESTION % (seq));
        player_string = input('> ');
        if player_string == 'q':
            print(MSG_ANSWER % (answer));
            break;
        elif player_string == 'answer':
            print(answer);
            continue;
        else:
            if ((not is_correct_keta(keta, player_string)) or (not is_int(player_string)) or (not is_unique(player_string))):
                print(MSG_ERROR1 % (keta));
                continue;
            hint = hit_and_blow(keta, player_string, answer);
            if hint[0]:
                print(MSG_OK % (seq));
                break;
            else:
                print(MSG_HINT % (hint[1], hint[2]));
        seq += 1;

def main(keta):
    # 正解の数字を作る
    ## numpy.arange を使って，0から始まる要素数10個の数列を公差1で作る
    _seq = np.arange(0, 10, 1);
    ## numpy.random.shuffle を使って，順番をランダムに並び変える
    np.random.shuffle(_seq);
    ## 正解の数字として，先頭のN要素を取得する
    answer = _seq[0: keta];

    # ゲーム開始
    start_game(keta, answer);

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

