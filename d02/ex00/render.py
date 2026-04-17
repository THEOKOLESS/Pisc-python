import sys
import os
import re


def load_settings():
    with open("settings.py") as f:
        content = f.read()
    return {m.group(1): m.group(2)
            for m in re.finditer(r'^(\w+)\s*=\s*"([^"]*)"', content, re.MULTILINE)}


def render(template_path):
    settings = load_settings()
    with open(template_path) as f:
        content = f.read()
    content = content.format_map(settings)
    output_path = template_path.removesuffix('.template') + '.html'
    with open(output_path, 'w') as f:
        f.write(content)


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 render.py <file.template>", file=sys.stderr)
        sys.exit(1)

    template_path = sys.argv[1]

    if not template_path.endswith('.template'):
        print("Error: file must have a .template extension", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(template_path):
        print(f"Error: '{template_path}' not found", file=sys.stderr)
        sys.exit(1)

    render(template_path)


if __name__ == '__main__':
    main()
