import tkinter as tk
from tkinter import filedialog
import re

def convert_to_html(custom_text):
    lines = custom_text.split('\n')

    # Проверка на наличие тега языка и названия
    language = None
    title = None

    for line in lines:
        line = line.strip()
        if line.startswith("language:"):
            language = line.split(':', 1)[1].strip() if ':' in line else None
        elif line.startswith("title:"):
            title = line.split(':', 1)[1].strip() if ':' in line else None

    if language is None:
        raise ValueError("Файл должен содержать тег 'language: <язык>'")
    if title is None:
        raise ValueError("Файл должен содержать тег 'title: <название>'")

    html_output = []
    in_code_block = False
    tag_stack = []  # Стек для отслеживания открытых тегов
    list_level = 0  # Отслеживание уровня вложенности списков

    # Добавляем контейнер с отступами
    html_output.append('<div class="container" style="max-width: 800px; margin: 0 auto; padding: 20px;">')
    tag_stack.append(("div", 0))

    for line in lines:
        line = line.strip()

        # Пропускаем пустые строки и метаданные
        if not line or line.startswith('language:') or line.startswith('title:'):
            continue

        if line.startswith('```'):
            in_code_block = not in_code_block
            if in_code_block:
                html_output.append("    " + "<pre><code>")
                tag_stack.append(("pre", list_level + 1))
                tag_stack.append(("code", list_level + 1))
            else:
                html_output.append("    " + "</code></pre>")
                tag_stack.pop()  # code
                tag_stack.pop()  # pre
            continue

        if in_code_block:
            html_output.append("    " + line)
            continue

        # Определение отступа для списков
        indent = len(line) - len(line.lstrip())
        current_level = indent // 2 + 1  # +1 для учета основного контейнера

        # Закрытие списков при изменении уровня
        while list_level > current_level - 1 and tag_stack:
            tag, level = tag_stack[-1]
            if level >= list_level:
                html_output.append("    " * (level) + f"</{tag}>")
                tag_stack.pop()
            list_level -= 1

        line = line.lstrip()  # Убираем начальные пробелы после подсчета

        # Заголовки с классами
        class_match = re.search(r'\{(.+?)\}', line)
        class_attr = f' class="{class_match.group(1)}"' if class_match else ''

        if line.startswith('#'):
            level = line.count('#')
            html_output.append("    " * current_level + f"<h{level}{class_attr}>{line[level:].strip()}</h{level}>")
            continue

        # Списки
        if line.startswith('-'):
            if current_level - 1 > list_level:
                html_output.append("    " * list_level + "<ul>")
                tag_stack.append(("ul", list_level))
                list_level = current_level - 1
            html_output.append("    " * current_level + f"<li>{line[1:].strip()}</li>")
            continue

        if re.match(r'^\d+\.', line):
            if current_level - 1 > list_level:
                html_output.append("    " * list_level + "<ol>")
                tag_stack.append(("ol", list_level))
                list_level = current_level - 1
            html_output.append("    " * current_level + f"<li>{line.split('.', 1)[1].strip()}</li>")
            continue

        # Закрываем все открытые списки, если встречаем не-список
        while list_level > 0 and tag_stack:
            tag, level = tag_stack[-1]
            if tag in ('ul', 'ol'):
                html_output.append("    " * level + f"</{tag}>")
                tag_stack.pop()
                list_level -= 1
            else:
                break

        # Обработка интерактивных элементов
        if line.startswith('[button]'):
            button_text = line.split(']', 1)[1].strip() if ']' in line else ""
            html_output.append("    " * current_level + f'<button>{button_text}</button>')
        elif line.startswith('[slider]'):
            html_output.append("    " * current_level + '<input type="range" min="1" max="100" value="50" class="slider">')
        elif line.startswith('[checkbox]'):
            html_output.append("    " * current_level + '<input type="checkbox"> ' + line[10:].strip())
        elif line.startswith('[toggle]'):
            html_output.append("    " * current_level + f'<button onclick="toggleAccordion()">Свернуть/развернуть</button>')
            html_output.append("    " * current_level + '<div id="accordionContent" style="display: none;">')
            html_output.append("    " * (current_level + 1) + f"{line[8:].strip()}")
            html_output.append("    " * current_level + "</div>")
        elif line.startswith('[dropdown]'):
            options = line[10:].strip().split(',')
            html_output.append("    " * current_level + '<select>')
            for option in options:
                html_output.append("    " * (current_level + 1) + f'<option value="{option.strip()}">{option.strip()}</option>')
            html_output.append("    " * current_level + '</select>')
        elif line.startswith('[input]'):
            html_output.append("    " * current_level + '<input type="text" placeholder="Введите текст здесь">')
        elif line.startswith('>'):
            html_output.append("    " * current_level + f"<blockquote>{line[1:].strip()}</blockquote>")
        elif line.strip():
            line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
            line = re.sub(r'__(.*?)__', r'<strong>\1</strong>', line)
            line = re.sub(r'\*(.*?)\*', r'<em>\1</em>', line)
            line = re.sub(r'_(.*?)_', r'<em>\1</em>', line)
            line = re.sub(r'`(.*?)`', r'<code>\1</code>', line)
            html_output.append("    " * current_level + f"<p>{line}</p>")

    # Закрываем все оставшиеся открытые теги
    while tag_stack:
        tag, level = tag_stack.pop()
        html_output.append("    " * level + f"</{tag}>")

    # Создаем базовую структуру HTML с базовыми стилями и скриптами
    html_document = [
        "<!DOCTYPE html>",
        f"<html lang='{language}'>",
        "<head>",
        "    <meta charset='UTF-8'>",
        "    <meta name='viewport' content='width=device-width, initial-scale=1.0'>",
        f"    <title>{title}</title>",
        "    <style>",
        "        body {",
        "            margin: 0;",
        "            padding: 0;",
        "            font-family: Arial, sans-serif;",
        "            line-height: 1.6;",
        "        }",
        "        .container {",
        "            max-width: 800px;",
        "            margin: 0 auto;",
        "            padding: 20px;",
        "        }",
        "        button {",
        "            padding: 10px 15px;",
        "            font-size: 16px;",
        "            cursor: pointer;",
        "        }",
        "        img {",
        "            max-width: 100%;",
        "            height: auto;",
        "        }",
        "    </style>",
        "</head>",
        "<body>",
        "    <script>",
        "    function toggleAccordion() {",
        "        var content = document.getElementById('accordionContent');",
        "        if (content.style.display === 'none') {",
        "            content.style.display = 'block';",
        "        } else {",
        "            content.style.display = 'none';",
        "        }",
        "    }",
        "    </script>"
    ] + html_output + ["</body>", "</html>"]

    return "\n".join(html_document)

def load_file():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(filetypes=[("HTMLang files", "*.HTMLang")])
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                custom_text = file.read()

            html_result = convert_to_html(custom_text)

            output_file_path = file_path.rsplit('.', 1)[0] + '.html'
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(html_result)

            print(f"Конвертация завершена. Результат сохранен в {output_file_path}")
        except ValueError as e:
            print(e)
        except Exception as e:
            print(f"Произошла ошибка: {str(e)}")
    else:
        print("Файл не выбран.")

load_file()