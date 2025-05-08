import re

def parse_mantra_text(text):
    """解析陀罗尼文本，提取标题和梵文内容"""
    mantras = []
    current_title = ""
    current_content = ""
    
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        # 检查是否是标题行（以M开头的编号）
        if re.match(r'^M\d+\.\d+', line):
            # 如果已有内容，保存前一个陀罗尼
            if current_title and current_content:
                mantras.append({
                    'title': current_title,
                    'content': current_content.strip()
                })
            # 开始新的陀罗尼
            current_title = line
            current_content = ""
        else:
            current_content += " " + line
    
    # 添加最后一个陀罗尼
    if current_title and current_content:
        mantras.append({
            'title': current_title,
            'content': current_content.strip()
        })
    
    return mantras

def create_transliteration_prompt(title, sanskrit_text):
    """创建用于Gemini API的音译提示词"""
    prompt = f"""请将以下梵文陀罗尼按照现代梵音发音规则音译为简体中文。
要求：只输出音译结果，输出结果为纯简体中文无其他语言，无错音漏音。

梵文原文：
{sanskrit_text}
"""
    return prompt

def save_transliteration_result(result, output_file):
    """保存单个音译结果到文件"""
    with open(output_file, 'a', encoding='utf-8') as f:
        f.write(f"{result['title']}\n")
        f.write(f"梵文：{result['sanskrit']}\n")
        f.write(f"音译：{result['transliteration']}\n\n")

def main():
    # 测试用例
    test_text = """M1.1 第一个陀罗尼
namaḥ sarva tathāgatebhyaḥ sarva mukhebhyaḥ sarvathā traṭ canda mahā roṣaṇa khaṃ khāhi khāhi sarva vighnaṃ hūṃ traṭ hāṃ māṃ

M1.2 第二个陀罗尼
oṃ vajra krodha mahā bala hana daha paca vidhvaṃsaya ucchuṣma krodha hūṃ phaṭ svāhā"""
    
    # 解析测试文本
    print("测试文本解析功能...")
    mantras = parse_mantra_text(test_text)
    print(f"成功解析 {len(mantras)} 个陀罗尼")
    
    # 测试提示词生成
    print("\n测试提示词生成功能...")
    for mantra in mantras:
        print(f"\n标题: {mantra['title']}")
        print(f"内容: {mantra['content']}")
        prompt = create_transliteration_prompt(mantra['title'], mantra['content'])
        print("生成的提示词:")
        print(prompt)
    
    # 测试实时结果保存
    print("\n测试实时结果保存功能...")
    test_results = [
        {
            'title': 'M1.1 测试陀罗尼',
            'sanskrit': 'oṃ maṇi padme hūṃ',
            'transliteration': '嗡 玛 尼 贝 美 吽'
        },
        {
            'title': 'M1.2 另一个陀罗尼',
            'sanskrit': 'tadyathā oṃ gate gate pāragate pārasaṃgate bodhi svāhā',
            'transliteration': '达迪亚他 嗡 嘎喋 嘎喋 巴拉嘎喋 巴拉桑嘎喋 菩提 梭哈'
        }
    ]
    test_output = 'test_output.txt'

    # 清空文件以便进行实时写入测试
    with open(test_output, 'w', encoding='utf-8') as f:
        pass # 清空文件

    print(f"开始实时写入结果到: {test_output}")
    for i, result in enumerate(test_results):
        print(f"写入第 {i+1} 个结果...")
        save_transliteration_result(result, test_output)
        # 实际应用中，这里会调用 Gemini API 并获取结果，然后调用 save_transliteration_result
        # 为了模拟实时性，这里可以添加一个小的延迟 time.sleep(1)

    print("所有测试结果已实时保存。")

if __name__ == "__main__":
    main()