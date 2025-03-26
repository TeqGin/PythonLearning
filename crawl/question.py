def determine_attachment(anxiety, security, avoidance):
    scores = {'焦虑': anxiety, '安全': security, '回避': avoidance}
    max_dim = max(scores, key=lambda k: scores[k])
    max_score = scores[max_dim]

    # 计算与另两个维度的差值
    diff1 = max_score - scores['安全'] if max_dim == '焦虑' else max_score - scores['焦虑'] if max_dim == '安全' else max_score - scores['焦虑']
    diff2 = max_score - scores['回避'] if max_dim == '焦虑' else max_score - scores['回避'] if max_dim == '安全' else max_score - scores['安全']

    # 判断是否满足双差值≥16条件
    if diff1 >= 16 and diff2 >= 16:
        return f'{max_dim}型依恋模式'
    
    # 检查三个维度间是否所有差值都<16
    all_diff = [
        abs(anxiety - security),
        abs(anxiety - avoidance),
        abs(security - avoidance)
    ]
    if all(d < 16 for d in all_diff):
        return '混合型依恋模式'
    else:
        return f'你在依恋模式各类型中得分较为平均，更倾向于{max_dim}型依恋模式'

# 题目与维度映射
dimension_map = {
    '焦虑': [4, 8, 10, 11, 13, 16, 17, 21],
    '安全': [1, 2, 5, 6, 9, 18, 22, 24],
    '回避': [3, 7, 12, 14, 15, 19, 20, 23]
}

question_arr = ['我认为我很容易和别人亲近。',
'适度依赖别人让我感到安心。',
'我不愿意和别人分享内心深处的感受。',
'我经常为人际关系感到烦恼。',
'即使和亲友发生争吵，我也不会全盘否定我们的感情。',
'如果别人对我的态度有些冷淡，我会冷静地思考原因是什么，并且我认为对方的表现也许并不是因为我。',
'我觉得与别人亲近会让我有些不舒服。',
'我容易对别人产生依赖的感觉。',
'我对自己的人际关系感到很满意。',
'如果别人对我的态度突然冷淡，我会觉得是我做错了什么。',
'在跟亲人朋友发生矛盾时，我有时会说一些狠话，做一些偏激的事情，过后又感到很后悔。',
'我很少对人际关系感到烦恼，因为我觉得人际关系不那么重要。',
'我对别人的情绪变化很敏感。',
'如果和我很亲近的朋友表现得有些冷淡疏远，我会感觉无动于衷，甚至如释重负。',
'我发现自己很难全身心依赖别人。',
'向别人倾诉我内心的感受时，我会担心对方发现我不好的一面。',
'我发现别人不乐意像我希望的那样与我亲近。',
'我很容易和别人沟通自己的需要和想法。',
'在和亲人朋友发生矛盾后，我很快就能平静下来，把心思放在其他事情上。',
'看到别人伤心的时候，我感觉很难给对方情感上的支持。',
'我担心如果我离开现在的朋友，很难再结交其他的朋友。',
'即使与好友曾经有过矛盾，我们仍然可以继续做朋友。',
'当别人与我很亲近的时候，我会感到不安。',
'和别人意见不一致的时候，我也能心平气和地表达。',]

# 输入处理
score_map = {'A':1, 'B':2, 'C':3, 'D':4, 'E':5}
answers = []
for i in range(1, 25):
    while True:
        ans = input(f"问题{i}:\t"+question_arr[i-1]+"\n（选项A.完全不符合 B.比较不符合 C.不确定 D.比较符合 E.完全符合）: ").strip().upper()
        if ans in score_map:
            answers.append(score_map[ans])
            break
        else:
            print("输入无效，请重新输入A/B/C/D/E")

# 计算维度得分
scores = {dim: sum(answers[q-1] for q in questions) 
          for dim, questions in dimension_map.items()}

# 输出结果
print("\n各维度得分：")
for dim, score in scores.items():
    print(f"{dim}维度：{score}")

result = determine_attachment(scores['焦虑'], scores['安全'], scores['回避'])
print("\n您的依恋模式判断结果：", result)
