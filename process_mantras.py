import os
from sanskrit_transliteration import parse_mantra_text, create_transliteration_prompt, save_transliteration_result
from gemini_demo import generate_text, setup_gemini_api
import time # 添加 time 模块导入

def process_mantras_batch(input_file, output_file):
    """批量处理陀罗尼文本并生成音译结果"""

    # 设置API
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("请设置GOOGLE_API_KEY环境变量")
        return
    if not setup_gemini_api(api_key):
        print("Gemini API 初始化失败，请检查API密钥和网络连接。")
        return

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
    
    # 清空输出文件以便进行实时写入
    with open(output_file, 'w', encoding='utf-8') as f:
        pass # 清空文件
    print(f"清空输出文件: {output_file}")

    processed_count = 0
    # 处理每个陀罗尼
    for i, mantra in enumerate(mantras, 1):
        print(f"\n[{i}/{len(mantras)}] 正在处理: {mantra['title']}")
        print(f"原文内容: {mantra['content'][:100]}..." if len(mantra['content']) > 100 else f"原文内容: {mantra['content']}")
        
        # 创建提示词并获取音译
        print("正在生成音译...")
        prompt = create_transliteration_prompt(mantra['title'], mantra['content'])
        transliteration = generate_text(prompt)
        
        if transliteration:
            print(f"音译结果: {transliteration}")
            result = {
                'title': mantra['title'],
                'sanskrit': mantra['content'],
                'transliteration': transliteration
            }
            # 实时保存结果
            save_transliteration_result(result, output_file)
            processed_count += 1
        else:
            print("❌ 音译失败")
            
        # 添加延迟以控制请求频率
        time.sleep(4.1) # 每分钟最多约 14.6 次请求 (60 / 4.1)
    
    # 总结处理结果
    if processed_count > 0:
        print(f"\n✅ 处理完成！成功音译 {processed_count}/{len(mantras)} 个陀罗尼")
        print(f"音译结果已实时保存到: {output_file}")
    else:
        print("\n❌ 没有成功生成任何音译结果")

def main():
    # 设置输入输出文件路径
    input_file = 'extracted_mantras2.txt'
    output_file = 'transliteration_results.txt'
    
    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"错误：输入文件 {input_file} 不存在")
        return
    
    # 开始处理
    print(f"开始处理陀罗尼音译任务...")
    process_mantras_batch(input_file, output_file)

if __name__ == "__main__":
    main()