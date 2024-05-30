import os
import multiprocessing
import time
import psutil
from PIL import Image

#これがないとでかすぎるとエラーが起きるからつけます
Image.MAX_IMAGE_PIXELS = None

"""
pngやjpegのメタデータは全部消えるので注意
もとのファイルの２倍まで一時的に膨らむから注意



使い方
まず使いたいファイルをコピーしてから
ファイルパスにコピーした使いたいディレクトリのパスを入れる
そしたら圧縮できた画像だけのこるから
元のコピーしてない使いたいディレクトリをエクスプローラーでコピペして
置き換えずにスキップしたらok



ver変えたから
使い方変わった
注意点は変わってない

使い方ver2
一応安全性のために使いたいファイルをコピーして
コピーしたファイルを指定
除外したいサブファイル（サブディレクトリ）があるなら除外して
cpuコアとか指定して実行すればいい


"""


# 末端のファイルに作用する関数
def process_file(file_path):
    try:
        with Image.open(file_path) as image:
            #imageのフォーマットを調べてwebp方式か確認してwebpだったら実行しない
            if image.format != "WEBP":
                
                #print(image.format)
                #入れた画像のサイズをinput_image_sizeに保存
                input_image_size = os.path.getsize(file_path)

                

                #画像をwebp形式、lossless、名前を-recompressを追加して保存

                #ファイルの名前と拡張子を入手
                file_name, file_extension = os.path.splitext(os.path.basename(file_path))
                
                #ファイルパスをオールドファイルパスとしておく
                old_file_path = file_path


                #ファイルパスをrecompressを追加した形に更新
                file_path = os.path.join(os.path.dirname(file_path), file_name + "-recompress" + file_extension)

                base = os.path.basename(old_file_path)
                #print(file_path)
                #セーブ、ここの設定変えたらもっと圧縮できるよ
                image.save(file_path,"webp",lossless=True,method=6)


                #保存した画像が元の画像より大きいかを判定
                if os.path.getsize(file_path) >= input_image_size:
                    #大きかったので削除
                    os.remove(file_path)
                else:
                    #小さかったので元のファイルを削除
                    os.remove(old_file_path)
                    #print("削除しました")
                    #os.path.join(os.path.dirname(file_path), os.path.basename(file_path))
                    

                    try:
                        #新しいほうの名前を変更
                        os.rename(file_path,os.path.join(os.path.dirname(old_file_path),os.path.basename(old_file_path)))
                        #print(f"変更しました {file_path} , {base}")
                    except:
                        import traceback
                        traceback.print_exc()
    except:
        import traceback
        traceback.print_exc()

def worker_init(cpu_ids):
    p = psutil.Process(os.getpid())
    p.cpu_affinity(cpu_ids)





# ファイル構造を再帰的に探索して、末端のファイルに対して関数を適用する関数
def process_files_in_directory(directory):
    #プロセスリストを作成、どれくらいプロセスがあるのかわかるようにする
    process_list = list()
    image_extensions = {".jpg", ".jpeg", ".png"}


    with multiprocessing.Pool(processes=int(len(cpu_ids)*1.5), initializer=worker_init, initargs=(cpu_ids,)) as pool:
            results = []

            # ディレクトリ内のすべてのファイルに対して処理を実行
            for root, dirs, files in os.walk(directory):
                # 除外するサブディレクトリを削除
                dirs[:] = [d for d in dirs if os.path.join(root, d) not in exclude_dirs]

                for file in files:
                    file_path = os.path.join(root, file)

                    _, ext = os.path.splitext(file_path)
                    if ext.lower() in image_extensions:
                        #if 
                        #非同期処理を追加
                        result = pool.apply_async(process_file, (file_path,))
                        results.append(result)
                        print(f"({len(results)}) このファイルを処理に回しました:{os.path.basename(file_path)}")




            # プールを閉じて、すべてのタスクの完了を待機
            pool.close()
            pool.join()

            #終わったのでＥＮＤといいます
            print("END")

if __name__ == "__main__":
    # ファイルを探索するディレクトリ
    directory_to_search = r

    #除外するサブディレクトリ
    exclude_dirs = []


    #使うcpuのコアを指定
    cpu_ids = list(range(0,32))
    print(cpu_ids)

    # ファイル構造を再帰的に探索して、末端のファイルに対して関数を適用
    process_files_in_directory(directory_to_search)
