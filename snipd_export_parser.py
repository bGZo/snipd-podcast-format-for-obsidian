import os
import re

import click
import yaml  # 用于生成 YAML 格式 Front Matter


def delete_ep_heading(title):
    title = re.sub(r'优酷纪实', ' ', title)
    title = re.sub(r'YOUKU DOCUMENTARY', ' ', title)
    # Steve说
    title = re.sub(r'[ ]*Steve说', ' ', title)
    title = re.sub(r'[ ]*史蒂夫说', ' ', title)
    # 翻电Special
    title = re.sub(r'^[ ]*翻电Special', ' ', title)
    # 性愛診療室🔞
    title = re.sub(r'性愛診療室🔞', ' ', title)
    title = re.sub(r'愛情診療室💌', ' ', title)
    
    # 席外话 
    title = re.sub(r'^[ ]*席外话', ' ', title)
    # 维她命
    title = re.sub(r'^[ ]*维她命', ' ', title)
    # 科技乱炖
    title = re.sub(r'^[ ]*科技乱炖', ' ', title)
    # CDT周报
    title = re.sub(r'[第]*\d+期', ' ', title)
    title = re.sub(r'CDT周报', ' ', title)
    # CDT周报
    title = re.sub(r'^[ ]*随机波动', ' ', title)
    # 翻电问答
    title = re.sub(r'^[ ]*翻电问答', ' ', title)
    title = re.sub(r'圆桌派', ' ', title)
    title = re.sub(r'第.*?季', ' ', title)


    # kan li xiang
    title = re.sub(r'^[ ]*[Vv][oO][Ll]', ' ', title)
    title = re.sub(r'^[ ]*[Ee][Pp]*\d+', ' ', title)
    title = re.sub(r'^[ ]*[Nn][Oo] *\d+', ' ', title)
    title = re.sub(r'^[ ]*[E] *\d+', ' ', title)
    title = re.sub(r'^[ ]*Epi *\d+', ' ', title)
    title = re.sub(r'^[ ]*S\d+E\d+', ' ', title)
    # ep number
    title = re.sub(r'^[ ]*\d+[ ]+', ' ', title)

    return title

def replace_value(title):
    # 【圆桌派

    try:
        title = re.match(r'\[\[(.*)\]\]', title).group(1)
    except AttributeError:
        pass

    try:
        title = re.match(r'\[open in Snipd\]\((.*)\)', title).group(1)
    except AttributeError:
        pass

    try:
        title = re.sub(r'[@…：.？，！\|｜【】\[\]:!“”《》_、「」#——<>:"/\\|\-。（）&•]', ' ', title)
    except AttributeError:
        pass

    title = delete_ep_heading(title)

    title = re.sub(r'[ ]+', ' ', title)
    title = title.strip()
    title = re.sub(r' ', '-', title)

    return title

def replace_link(title):

    try:
        title = re.match(r'\[\[(.*)\]\]', title).group(1)
    except AttributeError:
        pass

    try:
        title = re.match(r'\[open in Snipd\]\((.*)\)', title).group(1)
    except AttributeError:
        pass


    return title.strip()


def replace_chapter(title):
    title = re.sub(r'---\n', '', title)
    title = re.sub(r'[\n]+', '\n', title)
    title = re.sub(r'[\n]+', '\n', title)
    title = re.sub(r'- Episode title::.*\n', '', title)
    title = re.sub(r'- Show::.*\n', '', title)
    title = re.sub(r'- Owner / Host::.*\n', '', title)
    title = re.sub(r'- Episode link::.*\n', '', title)
    title = re.sub(r'- Episode publish date::.*\n', '', title)
    title = re.sub(r'- Show notes link::.*\n', '', title)
    title = re.sub(r'- Tags::.*\n', '', title)
    title = re.sub(r'- Tags:.*\n', '', title)
    title = re.sub(r'- Export date::.*\n', '', title)
    title = re.sub(r'!\[Cover\|200\]\(.*\)\n', '', title)
    title = re.sub(r'<details>\n<summary>', '', title)
    title = re.sub(r'</details>', '', title)
    title = re.sub(r'</summary>', '', title)
    title = re.sub(r'Show notes', '## Show notes', title)
    title = re.sub(r'## Episode metadata\n', '', title)
    title = re.sub(r'<br\/>', '\n', title)
    title = re.sub(r'> [ ]+', '> ', title)


    title = re.sub(r'^#[^#]+?\n', '\n', title)

    return title


def parse_markdown(md_content):
    """
    解析 Markdown 内容为章节列表
    """
    # 分割章节，以 "# " 开头为章节标志
    chapters = re.split(r'(?<=\n)\n(?=# )', md_content.strip())
    return chapters

def extract_metadata(chapter):
    """
    从章节中提取元数据并返回一个字典
    """
    metadata_pattern = r'## Episode metadata\n(.*?)\n(?=\n|##)'
    match = re.search(metadata_pattern, chapter, re.DOTALL)
    if not match:
        return {}
    metadata_block = match.group(1)

    # 'add source'
    metadata_pattern = r'- Show notes link:: \[open website\]\((.*?)\)\n'
    match = re.search(metadata_pattern, chapter, re.DOTALL)
    if not match:
        return {}
    source = match.group(1)

    # 'add cover'
    metadata_pattern = r'!\[Cover\|200\]\((.*?)\)\n'
    match = re.search(metadata_pattern, chapter, re.DOTALL)
    if not match:
        return {}
    cover = match.group(1)

    metadata = {}
    date = ''
    for line in metadata_block.split('\n'):
        key_value_match = re.match(r'- (.+?):: (.+)', line.strip())
        if key_value_match:
            key = key_value_match.group(1).strip()
            value = key_value_match.group(2).strip()

            # print('key', key, 'value', value)
            if(key == 'Episode link'):
                metadata['snipd'] = replace_link(value)
                continue

            elif (key == 'Episode publish date'):
                value += "T09:36:39"
                metadata['published'] = value
                date = value
                continue

            elif (key == 'Episode title'):
                metadata['title'] = replace_link(value)
                continue
            
            elif (key == 'Owner / Host'):
                metadata['author'] = replace_link(value)
                continue
            
            elif (key == 'Show'):
                metadata['show'] = replace_link(value)
                continue

            metadata[key] = replace_link(value)

    metadata['cover'] = cover
    metadata['created'] = date
    metadata['modified'] = date
    metadata['source'] = source
    metadata['type'] = 'podcast-episode'

    return metadata

def create_front_matter(metadata):
    """
    根据提取的元数据生成 YAML 格式的 Front Matter
    """
    if not metadata:
        return ""
    front_matter = "---\n"
    front_matter += yaml.dump(metadata, allow_unicode=True, default_flow_style=False)
    front_matter += "---\n\n"
    return front_matter

def save_chapter_to_file(chapter, output_folder):
    """
    保存章节内容到文件
    """
    # 获取标题作为文件名
    title_match = re.match(r'# (.+)', chapter)
    if not title_match:
        return
    title = replace_value(title_match.group(1).strip())

    file_name = f"~{title}.md"
    file_path = os.path.join(output_folder, file_name)

    # 提取元数据
    metadata = extract_metadata(chapter)
    front_matter = create_front_matter(metadata)

    # 保存章节内容到文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(front_matter)
        file.write(replace_chapter(chapter))

    print(f"文件已创建: {file_path}")

@click.command()
@click.argument('file')
@click.option('--output', '-o', default="chapters"
    , type=click.Path(exists=True))
def main(file: str, output: str) -> None:
    # folder_path = "backup"
    input_file = file # os.path.join(folder_path, file)

    # 确保输出文件夹存在
    os.makedirs(output, exist_ok=True)

    # 读取文件内容
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            markdown_content = file.read()
    except FileNotFoundError:
        print(f"文件 {input_file} 未找到！请确保文件存在于当前目录。")
        return

    # 解析 Markdown 内容
    chapters = parse_markdown(markdown_content)

    # 遍历每个章节并保存为单独文件
    for chapter in chapters:
        save_chapter_to_file(chapter, output)

@click.command()
def cli() -> None:
    print("I'm working")

if __name__ == "__main__":
    main()