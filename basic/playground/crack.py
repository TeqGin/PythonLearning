def generate_continuous_candidates(s, key_length=24):
    """生成所有可能的连续子串候选"""
    candidates = []
    n = len(s)
    if n < key_length:
        return candidates
    for i in range(n - key_length + 1):
        candidates.append(s[i:i+key_length])
    return candidates

def generate_fixed_infix_candidates(s, key_length=24):
    """生成固定间隔插入字符的候选"""
    candidates = []
    n = len(s)
    max_k = (n - 1) // (key_length - 1) if key_length > 1 else 0
    for k in range(1, max_k + 1):
        step = k + 1
        max_start = n - (step * (key_length - 1) + 1)
        if max_start < 0:
            continue
        for start in range(0, max_start + 1):
            indices = [start + i * step for i in range(key_length)]
            if indices[-1] >= n:
                continue
            candidate = ''.join([s[i] for i in indices])
            candidates.append(candidate)
    return candidates

def generate_two_part_candidates(s, key_length=24):
    """生成分割为两段的候选"""
    candidates = []
    n = len(s)
    for l1 in range(1, key_length):
        l2 = key_length - l1
        for i in range(n - l1 + 1):
            part1 = s[i:i+l1]
            remaining = n - (i + l1)
            if remaining < l2:
                continue
            for j in range(i + l1, n - l2 + 1):
                part2 = s[j:j+l2]
                candidates.append(part1 + part2)
    return candidates

# 混淆后的字符串
obfuscated_str = "*w+H,hZsCpv:y,mcA<aat#X8 * 41hyK!|Gc%IbsjLct>A}QpKzEC%+^KeBFF!g#,)scI#gkc&h+kAipGKcJmHhjccBx"

# 生成候选
continuous = generate_continuous_candidates(obfuscated_str)
fixed_infix = generate_fixed_infix_candidates(obfuscated_str)
two_part = generate_two_part_candidates(obfuscated_str)

# 合并并去重
all_candidates = list(set(continuous + fixed_infix + two_part))

# 输出结果
print(f"Generated {len(all_candidates)} candidates.")
for idx, candidate in enumerate(all_candidates):  # 示例：打印前10个候選
    if candidate == "cA41hIbsjQpKzE!g#kc&hGKc":
        print("found")
#print(f"Candidate {idx+1}: {candidate}")

# 可根据需要将候选写入文件或进一步处理
# with open('candidates.txt', 'w') as f:
#     for candidate in all_candidates:
#         f.write(candidate + '\n')
