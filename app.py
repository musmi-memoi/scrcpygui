import flet as ft
import subprocess
import get_devices as gd
import time

def main(page: ft.Page):

    process = None
    connect = False

    page.title = "Scrcpy_GUI"
    page.window_width = 600
    page.window_max_height = 600
    page.padding = 24
    page.theme = ft.Theme(color_scheme_seed='green',use_material3=True)
    page.theme_mode = ft.ThemeMode.SYSTEM

    def check_av(e):
        if noaudio.value == True:
            novideo.value = False
            novideo.update()
        elif novideo.value == True:
            noaudio.value = False
            noaudio.update()

    def load_device(e):
        connected_devices = gd.get_connected_devices()
        options = [ft.dropdown.Option(device['device_id']) for device in connected_devices]
        device_dd.options = options
        page.update()

    def start_scrcpy(e):
        nonlocal connect, process

        nv = novideo.value
        cam = usecam.value
        na = noaudio.value
        bt = bitrate.value
        audio_s = audiosource.value
        ab = audiobuffer.value
        db = displaybuffer.value

        fps = int(maxfps.value) if maxfps.value else 60

        device = str(device_dd.value)
        print(device)
        command = ['scrcpy', '-s', device,f'--max-fps={fps}']
        if device != "None":
            if cam == True:
                command.append('--video-source=camera')
                command.append('--camera-ar=16:9')
            if nv == True:
                command.append('--no-video')
            if na == True:
                command.append('--no-audio')
            if bt:
                command += ['-b',f'{bt}M']
            if audio_s is None and audio_s == "内部音声":
                pass
            elif audio_s == "マイク":
                command.append('--audio-source=mic')
            if ab:
                command.append(f'--audio-buffer={ab}')
            if db:
                command.append(f'--display-buffer={db}')
            print("プロセスを開始"+str(command))
            process = subprocess.Popen(command,creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            connect_btn.text = "デバイスを選択してください"
            connect_btn.icon = ft.icons.ERROR
            connect_btn.update()
            time.sleep(2)
            connect_btn.text = "接続"
            connect_btn.icon = ft.icons.PLAY_ARROW
            connect_btn.update()
    
    title = ft.Text("Scrcpy_GUI", style=ft.TextThemeStyle.TITLE_MEDIUM,size=32)
    device_dd = ft.Dropdown(label="デバイス", expand=True, options=[],tooltip="右のボタンをクリックして読み込みます")
    connect_btn = ft.FloatingActionButton(icon=ft.icons.PLAY_ARROW, text="接続", on_click=start_scrcpy,tooltip="キャストを開始します")
    select_device = ft.Row([
        device_dd,
        ft.IconButton(icon=ft.icons.REFRESH,on_click=load_device,tooltip="デバイスを読み込む")
    ], expand=0)
    option_text = ft.Text("オプション")
    novideo = ft.Switch(label="画面をキャストしない",value=False,expand=True,on_change=check_av,tooltip="有効にすると画面は共有されません")
    noaudio = ft.Switch(label="音声をキャストしない",value=False,expand=True,on_change=check_av,tooltip="有効にすると音声は共有されません")
    usecam = ft.Switch(label="カメラを使用する",value=False,tooltip="有効にするとカメラの映像が共有されます")
    nosource = ft.Row([novideo,noaudio])
    bitrate = ft.TextField(label="映像ビットレート(デフォルト:8)",suffix_text="Mbps",tooltip="小さすぎると画質が悪く、大きすぎるとより安定した接続が必要になります")
    audiosource = ft.Dropdown(label="オーディオソース",options=[ft.dropdown.Option("内部音声"),ft.dropdown.Option("マイク")],tooltip=f"共有するソースを決められます\n内部音声の場合本体スピーカーから音が出力できなくなります")
    audiobuffer = ft.TextField(label="オーディオバッファー(デフォルト:50)",suffix_text="ms",expand=True,tooltip="大きくすれば途切れにくくなりますが遅延が大きくなります")
    displaybuffer = ft.TextField(label="ディスプレイバッファー(デフォルト:0)",suffix_text="ms",expand=True,tooltip="大きくすれば途切れにくくなりますが遅延が大きくなります")
    maxfps = ft.TextField(label="最大FPS(デフォルト:60)",suffix_text="fps",tooltip="FPSを指定できます")
    buffers = ft.Row([audiobuffer,displaybuffer])
    options = ft.Column([
        nosource,usecam,bitrate,audiosource,buffers,maxfps
    ],spacing=10)

    page.add(title, select_device,option_text, connect_btn,options)

if __name__ == "__main__":
    ft.app(main)
