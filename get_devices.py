import subprocess

def get_connected_devices():
    # adb devicesコマンドを実行して接続されているデバイスの一覧を取得
    print('デバイスを確認しています…')
    result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
    
    # 出力からデバイスのリストを作成
    output_lines = result.stdout.splitlines()[1:]
    devices = [{'device_id': line.split('\t')[0]} for line in output_lines if len(line.split('\t')) == 2]
    return devices