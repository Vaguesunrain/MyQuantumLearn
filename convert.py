import sys
import os
import nbformat
from nbconvert import MarkdownExporter

def convert_to_md_with_suffix(ipynb_path):
    # 1. 读取笔记本
    with open(ipynb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
        
    # 2. 内存中自动去重并加后缀
    seen_names = {}
    for cell in nb.cells:
        if cell.cell_type == 'markdown' and hasattr(cell, 'attachments') and cell.attachments:
            attachments = cell.attachments
            new_attachments = {}
            source = cell.source
            
            for name, content in attachments.items():
                if name in seen_names:
                    seen_names[name] += 1
                    base, ext = name.rsplit('.', 1) if '.' in name else (name, '')
                    new_name = f"{base}_{seen_names[name]}.{ext}" if ext else f"{base}_{seen_names[name]}"
                else:
                    seen_names[name] = 0
                    new_name = name
                
                if new_name != name:
                    source = source.replace(f"attachment:{name}", f"attachment:{new_name}")
                new_attachments[new_name] = content
            
            cell.attachments = new_attachments
            cell.source = source

    # 3. 调用 API 转换为 Markdown
    md_exporter = MarkdownExporter()
    (body, resources) = md_exporter.from_notebook_node(nb)
    
    # 4. 写出 md 文件与图片
    base_path = os.path.splitext(ipynb_path)[0]
    md_path = base_path + '.md'
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(body)
        
    if 'outputs' in resources:
        for filename, data in resources['outputs'].items():
            out_path = os.path.join(os.path.dirname(ipynb_path), filename)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, 'wb') as img_f:
                img_f.write(data)
                
    print(f"转换成功！已生成: {md_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用错误。请输入: python convert.py <你的笔记本路径.ipynb>")
    else:
        convert_to_md_with_suffix(sys.argv[1])