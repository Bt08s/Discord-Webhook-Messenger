from discord_webhook import DiscordWebhook
import dearpygui.dearpygui as dpg
from torswitch import TorProtocol
import threading
import os

dpg.create_context()


def clear():
    os.system("cls" if os.name == "nt" else "clear")
    

def send():
    use_tor = dpg.get_value("use tor")
    use_avatar = dpg.get_value("use avatar")

    url = dpg.get_value("webhook url")
    username = dpg.get_value("webhook username")
    message = dpg.get_value("message")
    count = int(dpg.get_value("message count"))
    avatar_url = dpg.get_value("avatar url")

    if use_tor is True:
        proxies = {
            'http': "socks5://127.0.0.1:9050",
            'https': "socks5://127.0.0.1:9050"
        }

        def ip_changer():
            while True:
                tor_ip = tor.AbsoluteNewTorIp()
                print("New tor ip", tor_ip)

        def threaded_sender():
            response = webhook.execute()
            rs = response.status_code
            if rs == 200:
                dpg.set_value("msg status", f"           Good response :) {rs}")
            else:
                dpg.set_value("msg status", f"           Bad response :( {rs}")

        tor = TorProtocol()
        tor.Stop()
        tor.Start()

        if count > 10:
            thread = threading.Thread(target=ip_changer)
            thread.start()

        if use_avatar:
            webhook = DiscordWebhook(url=url, rate_limit_retry=True, content=message, username=username, proxies=proxies, avatar_url=avatar_url)
        else:
            webhook = DiscordWebhook(url=url, rate_limit_retry=True, content=message, username=username, proxies=proxies)

        threads = []
        for _ in range(count):
            thread = threading.Thread(target=threaded_sender)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        tor.Stop()
    else:
        def threaded_sender():
            response = webhook.execute()
            rs = response.status_code
            if rs == 200:
                dpg.set_value("msg status", f"          Good response :) {rs}")
            else:
                dpg.set_value("msg status", f"          Bad response :( {rs}")

        if use_avatar:
            webhook = DiscordWebhook(url=url, rate_limit_retry=True, content=message, username=username, avatar_url=avatar_url)
        else:
            webhook = DiscordWebhook(url=url, rate_limit_retry=True, content=message, username=username)

        threads = []
        for _ in range(count):
            thread = threading.Thread(target=threaded_sender)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    dpg.set_value("webhook msg status", "")
    dpg.show_item("done popup")


with dpg.window(label="Webhook", tag="Webhook window"):
    dpg.add_checkbox(label="Use tor proxy", tag="use tor", default_value=True)
    dpg.add_checkbox(label="Custom avatar", tag="use avatar", default_value=False)
    dpg.add_spacer(parent=3)
    dpg.add_input_text(label="Tor proxy", default_value="http(s): socks5://127.0.0.1:9050", readonly=True)
    dpg.add_input_text(label="Avatar url", tag="avatar url")
    dpg.add_spacer(parent=3)
    dpg.add_input_text(label="Webhook url", tag="webhook url")
    dpg.add_input_text(label="Webhook name", tag="webhook username")
    dpg.add_input_text(label="Message", tag="message")
    dpg.add_input_text(label="Message count", tag="message count")
    dpg.add_button(label="Send", width=100, callback=send)
    dpg.add_spacer(parent=3)
    dpg.add_text(tag="webhook msg status", color=(0, 128, 0))

    with dpg.popup(dpg.last_item(), modal=True, tag="done popup"):
        dpg.add_text("Sent!")


with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 3)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3)
        dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 3)
        dpg.add_theme_style(dpg.mvStyleVar_TabRounding, 3)
        dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 3)
        dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, 3)
        dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 3)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 4, 4)
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 5, 5)

clear()
dpg.bind_theme(global_theme)
dpg.create_viewport(title='Discord webhook messenger by Bt08s', width=780, height=370)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Webhook window", True)
dpg.start_dearpygui()
dpg.destroy_context()
