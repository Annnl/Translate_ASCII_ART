import google.generativeai as genai
from bs4 import BeautifulSoup, NavigableString
import re

# 配置Gemini API
GENAI_API_KEY = "AIzaSyChZQ1v3Wkn382omZlMMD3quQJgYOqOvxQ"  # 替换为你的实际API密钥
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# 翻译缓存字典（减少API调用）
translation_cache = {}

async def translate_japanese_to_chinese(text):
    # 检查缓存
    if text in translation_cache:
        return translation_cache[text]
    
    # 检查是否需要翻译（简单日语字符检测）
    if not re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]', text):
        return text
    
    # 调用Gemini API进行翻译
    response = await model.generate_content_async(
        f"将以下日文内容精确翻译成简体中文，保持专业语气，不要添加额外内容：\n{text}"
    )
    
    translated = response.text
    translation_cache[text] = translated  # 缓存结果
    return translated

def process_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    async def process_element(element):
        if isinstance(element, NavigableString):
            if element.parent.name not in ['script', 'style', 'meta']:
                original = str(element).strip()
                if original:
                    translated = await translate_japanese_to_chinese(original)
                    element.replace_with(translated)
        else:
            for child in element.contents:
                await process_element(child)
    
    # 注意：实际运行时需要异步事件循环
    import asyncio
    asyncio.run(process_element(soup))
    
    return str(soup)

# 主程序
if __name__ == "__main__":
    input_path = r"C:\Users\ningn\Downloads\【ほのぼの？】やる夫と町の怪奇譚【ホラー？】 第１話 『クチサケオンナ』(前編) その2 - 暇な時にやる夫まとめ.html"
    output_path = r"C:\Users\ningn\Downloads\test.html"
    # 读取输入文件
    with open(input_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 处理HTML内容
    processed_html = process_html(html_content)

    # 写入输出文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(processed_html)

    print("HTML文件翻译完成！")