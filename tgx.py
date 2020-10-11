import requests
import re
import prettytable

item_matcher = re.compile(r"<div class='tgxtablerow'(.*?)</small></td></table></div></div>")
type_matcher = re.compile(r"<small>(.*?)</small>")
title_matcher = re.compile(r"""<a title="(.*?)" """)
size_matcher = re.compile(r"style='border-radius:4px;'>(.*?)</span></div>")
torrent_matcher = re.compile(r"<a href='https(.*?)'")
page_matcher = re.compile(r"[0-9]+</a></li><li class='page-item'>")

download_path = r'C://Users/Dezheng Meng/Downloads/'

while(True):
    search_content = input("Search TorrentGalaxy:")
    search_content = search_content.replace(" ", "+")
    print("Start searching.")
    search_result = requests.get(r'https://torrentgalaxy.to/torrents.php?search=' + search_content + r'&sort=id&order=desc&page=0').text

    count = 1
    item_list = []

    page_list = page_matcher.findall(search_result)
    page_num = int(page_list[0].replace(r"</a></li><li class='page-item'>", ''))

    for num in range(page_num):
        print("Searching...(page:" + str(num + 1) + "/" + str(page_num) + ')', end="\r")
        if num == 0:
            pass
        else:
            search_result = requests.get(r'https://torrentgalaxy.to/torrents.php?search=' + search_content + r'&sort=id&order=desc&page=' + str(num)).text
        search_items = item_matcher.findall(search_result)
        for i in search_items:
            item = []
            item.append(str(count))
            count += 1
            type_list = type_matcher.findall(i)
            item.append(type_list[0].replace("&nbsp", ' '))
            title_list = title_matcher.findall(i)
            item.append(title_list[0])
            size_list = size_matcher.findall(i)
            item.append(size_list[0])
            torrent_list = torrent_matcher.findall(i)
            item.append('https' + torrent_list[0])
            item_list.append(item)

    print("\nSearch complete.")
    print("Start listing.")
    tables = []
    count1 = 0
    count2 = 1
    for i in item_list:
        print("Listing(" + str(count2) + "/" + str(len(item_list)) + ")", end="\r")
        if count1 == 0:
            table = prettytable.PrettyTable(["N0.", "Type", "Name", "Size"], vrules=prettytable.ALL, hrules=prettytable.ALL)
        table.add_row(i[0:4])
        count1 += 1
        count2 += 1
        if(count1 == 50):
            tables.append(table)
            count1 = 0
    print("\nList complete.")
    print("Search result:")
    for table in tables:
        print(table)

    while(True):
        while(True):
            next = input("Continue to download?(y/n):")
            if next == 'y' or next == 'Y' or next == 'n' or next == 'N':
                break
            else:
                continue
        if next == 'y' or next == 'Y':
            continue
        if next == 'n' or next == 'N':
            print("Finsh download!")
            break
        if len(item_list) == 0:
            break
        while(True):
            try:
                download = int(input("Download:"))
            except ValueError:
                print("Invalid Number Input!")
                continue
            else:
                if download > 0 and download <= len(item_list):
                    break
                else:
                    print("Invalid Number Input!")
                    continue
        print("Downloading...")
        torrent_file = requests.get(item_list[download-1][4]).content
        try:
            local_file = open(download_path + item_list[download-1][2] + '.torrent', 'xb')
        except FileExistsError:
            num = 1
            while(True):
                try:
                    local_file = open(download_path + item_list[download-1][2] + '(' + str(num) + ')' + '.torrent', 'xb')
                except FileExistsError:
                    num += 1
                    continue
                else:
                    break
        
        local_file.write(torrent_file)
        local_file.close()
        print("Finished!")
        
    while(True):
        next = input("Continue to search?(y/n):")
        if next == 'y' or next == 'Y' or next == 'n' or next == 'N':
            break
        else:
            continue
    if next == 'y' or next == 'Y':
        continue
    if next == 'n' or next == 'N':
        print("Quitting...")
        break