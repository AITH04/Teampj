from linebot.models import (
    TextMessage, TextSendMessage, QuickReplyButton, MessageAction, QuickReply
)


def scenes1():
    # 場景名: wait_user
    reply = []
    welcome_word1 = "歡迎來到「送禮達人」，我們的目標只有一個，就是為您找出讓人感動的禮物。\n\n我們每次會從不同角度協助您選擇，讓您每次都有不同的驚奇。"
    messages1 = TextSendMessage(text=welcome_word1)
    reply.append(messages1)

    welcome_word2 = "請問您要送誰禮物？"
    messages2 = TextSendMessage(text=welcome_word2)
    reply.append(messages2)
    return reply


def scense2():
    # 場景名: ask_interest
    reply = []
    ask_interst = "他喜歡什麼音樂？電影？影集？人物？"
    messages0 = TextSendMessage(text=ask_interst)
    reply.append(messages0)
    return reply


def scense3(subject, present_cnt, next_tag):
    # 場景名: first_question
    reply = []
    reply_word = f"好的，我們一起來為 {subject} 挑禮物吧"
    messages0 = TextSendMessage(text=reply_word)
    reply.append(messages0)
    reply_word = f"候選禮物數：{present_cnt}"
    messages1 = TextSendMessage(text=reply_word)
    reply.append(messages1)

    reply_items = []
    reply_word = f"您覺得 {subject} 對 {next_tag} 有興趣嗎？\n有／無（換一題)"
    reply_items.append(QuickReplyButton(action=MessageAction(label="有", text="有")))
    reply_items.append(QuickReplyButton(action=MessageAction(label="無,換一題", text="無")))
    messages2 = TextSendMessage(reply_word, quick_reply=QuickReply(items=reply_items))
    reply.append(messages2)

    return reply


def scense4(subject, next_tag):
    # 場景名: question_loop_False
    reply = []
    reply_items = []
    reply_word = f"您覺得 {subject} 對 {next_tag} 有興趣嗎？有／無（換一題)"
    reply_items.append(QuickReplyButton(action=MessageAction(label="有", text="有")))
    reply_items.append(QuickReplyButton(action=MessageAction(label="無,換一題", text="無")))
    messages2 = TextSendMessage(reply_word, quick_reply=QuickReply(items=reply_items))
    reply.append(messages2)
    return reply


def scense5(subject, present_cnt, next_tag, tags):
    # 場景名: question_loop_True
    reply = []
    str_tags = tags[0]
    if len(tags)>1:
        for i in range(1,len(tags)):
            str_tags = str_tags + "、"+tags[i]
    reply_word = f"他有興趣的元素：{str_tags}\n候選禮物數：{present_cnt}"
    messages0 = TextSendMessage(text=reply_word)
    reply.append(messages0)

    # quick btn
    reply_items = []
    reply_word = f"您覺得 {subject} 對 {next_tag} 有興趣嗎？有／無（換一題)"
    reply_items.append(QuickReplyButton(action=MessageAction(label="有", text="有")))
    reply_items.append(QuickReplyButton(action=MessageAction(label="無,換一題", text="無")))
    messages2 = TextSendMessage(reply_word, quick_reply=QuickReply(items=reply_items))
    reply.append(messages2)

    return reply


def scense6(subject, present_cnt, tags, product_info, thx_word):
    # 場景名: end_conversation
    reply = []

    str_tags = tags[0]
    if len(tags)>1:
        for i in range(1,len(tags)):
            str_tags = str_tags + "、"+tags[i]
    reply_word = f"他有興趣的元素：{str_tags}\n候選禮物數：{present_cnt}"
    messages0 = TextSendMessage(text=reply_word)
    reply.append(messages0)

    show_products = f"以下是我們覺得 {subject} 會喜歡的禮物\n"
    no = 1
    for key in product_info.keys():
        show_products = show_products + str(no) + ". " + key + '\n    ' + product_info[key] + "\n"
        no += 1
    messages1 = TextSendMessage(text=show_products)
    reply.append(messages1)
    messages2 = TextSendMessage(text=thx_word)
    reply.append(messages2)
    return reply


def main(response):
    state = response['cur_state']
    print('!!!!!!!!response',response)
    if state == "wait_user":
        return scenes1()
    elif state == "ask_interest":
        return scense2()
    elif state == "first_question":
        return scense3(response["subject"], response['product_cnt'], response['next_tag'])
    elif state == "question_loop_False":
        return scense4(response["subject"], response['next_tag'])
    elif state == "question_loop_True":
        return scense5(response["subject"], response['product_cnt'], response['next_tag'], response["conds"])
    elif state == "end_conversation":
        return scense6(response["subject"], response['product_cnt'], response["conds"], response["products"], response["thx words"])
    else:
        # 變成回音機器人
        reply = []
        messages0 = TextSendMessage(text='出現錯誤狀態，請回頭檢查機器人')
        reply.append(messages0)
        return reply