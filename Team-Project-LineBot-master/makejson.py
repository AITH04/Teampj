import json

print("這是一個寫入LINEBOT JSON檔的工具")

def default():
    content = {'YOUR_CHANNEL_ACCESS_TOKEN':'', 'YOUR_CHANNEL_SECRET':''}
    with open('linebotToken.json', 'w', encoding='utf8') as f:
        json.dump(content, f, indent=4, ensure_ascii=False)
    print(f'儲存內容: {content}')


def update():
    answer = input(":: 請輸入 YOUR_CHANNEL_ACCESS_TOKEN \n\t>>")
    content = {'YOUR_CHANNEL_ACCESS_TOKEN': answer}
    answer = input(":: 請輸入 YOUR_CHANNEL_SECRET \n\t>>")
    content['YOUR_CHANNEL_SECRET'] = answer
    print("以下是您輸入的內容")
    print(f"YOUR_CHANNEL_ACCESS_TOKEN = {content['YOUR_CHANNEL_ACCESS_TOKEN']}")
    print(f"YOUR_CHANNEL_SECRET = {content['YOUR_CHANNEL_SECRET']}")
    with open('linebotToken.json', 'w', encoding='utf8') as f:
        json.dump(content, f, indent=4, ensure_ascii=False)
    print(f'已更新內容: {content}')


def checkcontent():
    try:
        with open('linebotToken.json', 'r', encoding='utf8') as f:
            content = json.load(f)
        print(f'::以下顯示JSON內容:: \n{content}\n')
    except:
        print("還沒建立檔案")


def main():
    select = -1
    while select != 0:
        print("="*40)
        print("\t>> MENU <<")
        print("0. 離開")
        print("1. 查看檔案內容")
        print("2. 更新檔案")
        print("3. 重置檔案")
        select = input("\n:: 請選擇功能 \n\t>>")
        try:
            select = int(select)
        except:
            continue
        if select == 1:
            checkcontent()
        elif select == 2:
            update()
        elif select == 3:
            default()
        else:
            continue


if __name__ == "__main__":
    main()