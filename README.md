# HTMLang
Write on Markdown and get HTML! This is a converter that will allow you to write HTML more conveniently!

Sure, here's a detailed documentation for the code in English:

```
# Markdown to HTML Converter

This Python script converts a custom Markdown-like format (referred to as "HTMLang") to HTML. It supports various Markdown elements such as headings, lists, links, images, code blocks, and formatting.

## Features

- Converts custom "HTMLang" format to HTML
- Automatically detects and sets the language and title of the HTML document
- Handles various Markdown elements:
  - Headings (with optional classes)
  - Unordered and ordered lists
  - Links
  - Images
  - Code blocks
  - Blockquotes
  - Bold and italic formatting
- Applies basic styling to the generated HTML:
  - Responsive container with a maximum width
  - Styling for code blocks, blockquotes, and images
- Saves the generated HTML file with the same name as the input file, but with the `.html` extension

## Usage

1. Run the script using a Python interpreter.
2. When prompted, select the "HTMLang" file you want to convert.
3. The script will generate an HTML file with the same name as the input file, but with the `.html` extension, and save it in the same directory.

## Input Format

The input file should be in the "HTMLang" format, which is a custom Markdown-like format. The file should start with the following metadata:

```
language: <language>
title: <title>
```

The `<language>` and `<title>` tags are required, and the script will use this information to set the appropriate HTML elements.

After the metadata, the file can contain the following Markdown-like elements:

- Headings: `# Heading 1`, `## Heading 2`, `### Heading 3`, etc. (Headings can also have classes, e.g., `# {custom-class} Heading 1`)
- Unordered lists: `-` followed by the list item
- Ordered lists: `1.` followed by the list item
- Links: `[link text](url)`
- Images: `![alt text](image_url)`
- Code blocks: Surrounded by ````` on separate lines
- Blockquotes: Starting with `>`
- Bold text: `**bold text**` or `__bold text__`
- Italic text: `*italic text*` or `_italic text_`
- Inline code: `` `inline code` ``

## Example Input

```
language: en
title: My Document

# {custom-class} Introduction
This is a sample document in the HTMLang format.

## Lists
- Unordered list item 1
- Unordered list item 2
  - Nested unordered list item
1. Ordered list item 1
2. Ordered list item 2

## Links and Images
Here is a [link to Google](https://www.google.com) and an ![image](https://via.placeholder.com/150).

## Code and Formatting
Here is some `inline code` and a code block:

```python
print("Hello, World!")
```

> This is a blockquote.

**This is bold text** and *this is italic text*.
```

## Example Output

The generated HTML file will look similar to the following:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Document</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            line-height: 1.6;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        img {
            max-width: 100%;
            height: auto;
        }
        pre {
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }
        blockquote {
            border-left: 4px solid #ccc;
            margin: 0;
            padding-left: 16px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="custom-class">Introduction</h1>
        <p>This is a sample document in the HTMLang format.</p>

        <h2>Lists</h2>
        <ul>
            <li>Unordered list item 1</li>
            <li>Unordered list item 2
                <ul>
                    <li>Nested unordered list item</li>
                </ul>
            </li>
        </ul>
        <ol>
            <li>Ordered list item 1</li>
            <li>Ordered list item 2</li>
        </ol>

        <h2>Links and Images</h2>
        <p>Here is a <a href="https://www.google.com">link to Google</a> and an <img src="https://via.placeholder.com/150" alt="image"></p>

        <h2>Code and Formatting</h2>
        <p>Here is some <code>inline code</code> and a code block:</p>
        <pre><code>print("Hello, World!")</code></pre>

        <blockquote>
            <p>This is a blockquote.</p>
        </blockquote>

        <p><strong>This is bold text</strong> and <em>this is italic text</em>.</p>
    </div>
</body>
</html>
```

## Dependencies

- Python 3.x
- `tkinter` (built-in)

## Limitations

- The script currently only supports the specific Markdown-like elements mentioned in the "Input Format" section.
- The styling applied to the generated HTML is basic and may need to be customized for specific use cases.

## Contribution

If you find any issues or have suggestions for improvements, feel free to create a new issue or submit a pull request on the project's GitHub repository.
