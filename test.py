import requests
from io import BytesIO
import zipfile
import os
import time

def download_and_extract_zip(url, max_retries=3, retry_delay=5):
    for retry in range(max_retries):
        try:
            # ZIPファイルをダウンロード
            response = requests.get(url)
            response.raise_for_status()

            zip_content = BytesIO(response.content)

            # カレントディレクトリに解凍
            with zipfile.ZipFile(zip_content, 'r') as zip_ref:
                # ZIPファイル内のファイルをカレントディレクトリに移動
                for zip_info in zip_ref.infolist():
                    try:
                        # ファイルがディレクトリであるかどうかを確認
                        if not zip_info.is_dir():
                            zip_info.filename = os.path.basename(zip_info.filename)
                            zip_ref.extract(zip_info)
                    except Exception as e:
                        print(f"解凍中にエラーが発生しました: {e}")

            print(f"ZIPファイルをダウンロードして解凍しました。解凍先: {os.getcwd()}")
            return  # 成功した場合は関数を終了

        except requests.exceptions.RequestException as e:
            print(f"ダウンロードまたは解凍中にエラーが発生しました: {e}")
            if retry < max_retries - 1:
                print(f"リトライします... ({retry + 1}/{max_retries})")
                time.sleep(retry_delay)
            else:
                print("最大リトライ回数に達しました。プログラムを終了します。")
                break

# ダウンロードするZIPファイルのURLを指定
zip_url = "https://github.com/Genymobile/scrcpy/releases/download/v2.3.1/scrcpy-win64-v2.3.1.zip"

# ダウンロードと解凍の実行（最大リトライ回数は3回、リトライ間隔は5秒）
download_and_extract_zip(zip_url, max_retries=3, retry_delay=5)
