import os
from google import genai
from sanskrit_transliteration import parse_mantra_text, create_transliteration_prompt, save_transliteration_result

def generate_text(api_key, prompt):
    """使用Gemini生成文本，每次调用时初始化API客户端"""
    try:
        # 创建客户端
        client = genai.Client(api_key=api_key)
        
        # 生成响应
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        # 返回生成的文本
        return response.text
    except Exception as e:
        print(f"生成文本时出错: {e}")
        return None

def process_mantras(api_key, input_file, output_file):
    """处理陀罗尼文件并生成音译结果"""
    # 读取输入文件
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"\n成功读取输入文件: {input_file}")
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return
    
    # 解析陀罗尼内容
    mantras = parse_mantra_text(content)
    print(f"共发现 {len(mantras)} 个陀罗尼需要处理")
    results = []
    
    # 处理每个陀罗尼
    for i, mantra in enumerate(mantras, 1):
        print(f"\n[{i}/{len(mantras)}] 正在处理: {mantra['title']}")
        print(f"原文内容: {mantra['content'][:100]}..." if len(mantra['content']) > 100 else f"原文内容: {mantra['content']}")
        
        # 创建提示词并获取音译
        print("正在生成音译...")
        prompt = create_transliteration_prompt(mantra['title'], mantra['content'])
        transliteration = generate_text(api_key, prompt)
        
        if transliteration:
            print(f"音译结果: {transliteration}")
            results.append({
                'title': mantra['title'],
                'sanskrit': mantra['content'],
                'transliteration': transliteration
            })
        else:
            print("❌ 音译失败")
    
    # 保存结果
    if results:
        save_transliteration_results(results, output_file)
        print(f"\n✅ 处理完成！成功音译 {len(results)}/{len(mantras)} 个陀罗尼")
        print(f"音译结果已保存到: {output_file}")
    else:
        print("\n❌ 没有成功生成任何音译结果")

def main():
    # 从环境变量获取API密钥
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("请设置GOOGLE_API_KEY环境变量")
        return
    
    # 设置输入输出文件路径
    input_file = "extracted_mantras2.txt"
    output_file = "transliterated_mantras.txt"
    
    # 处理陀罗尼
    process_mantras(api_key, input_file, output_file)

if __name__ == "__main__":
    main()