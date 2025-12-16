import re
import html
import sys
from dataclasses import dataclass, field
from typing import List, Optional
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

INPUT_FILE = "script.rhps"
OUTPUT_FILE = "index.html"
TEMPLATE_FILE = "template.html"

@dataclass
class ScriptElement:
    @property
    def type(self):
        return self.__class__.__name__

@dataclass
class SceneHeader(ScriptElement):
    title: str
    id: str = field(default="")
    number: int = field(default=0)

@dataclass
class StageDirection(ScriptElement):
    lines: List[str] = field(default_factory=list)

@dataclass
class CrowdAction(ScriptElement):
    lines: List[str] = field(default_factory=list)

@dataclass
class CastAction(ScriptElement):
    lines: List[str] = field(default_factory=list)

@dataclass
class Dialogue(ScriptElement):
    character: str
    lines: List[str] = field(default_factory=list)

class RhpsParser:
    def parse(self, text: str) -> List[ScriptElement]:
        elements: List[ScriptElement] = []
        lines = text.split('\n')
        current_dialogue: Optional[Dialogue] = None

        for line in lines:
            raw_line = line.rstrip()
            stripped_line = raw_line.strip()

            if not stripped_line:
                continue

            # Indentation (Continuation)
            if re.match(r'^\s+', raw_line) and current_dialogue and not (stripped_line.startswith('((') or stripped_line.startswith('[[') or stripped_line.startswith('#')):
                current_dialogue.lines.append(stripped_line)
                continue

            # Scene Header
            if stripped_line.startswith('#'):
                title = stripped_line.lstrip('#').strip()
                elements.append(SceneHeader(title=title))
                current_dialogue = None
                continue

            # Crowd Actions (( ... ))
            if stripped_line.startswith('((') and stripped_line.endswith('))'):
                content = stripped_line[2:-2].strip()
                elements.append(CrowdAction(lines=[content]))
                current_dialogue = None
                continue

            # Cast Actions [[ ... ]]
            if stripped_line.startswith('[[') and stripped_line.endswith(']]'):
                content = stripped_line[2:-2].strip()
                elements.append(CastAction(lines=[content]))
                current_dialogue = None
                continue

            # Speaker
            speaker_match = re.match(r'^([A-Za-z0-9\s\.\-\(\)\'&]+):\s+(.*)', raw_line)
            if speaker_match:
                char_name = speaker_match.group(1)
                first_line = speaker_match.group(2)
                new_dialogue = Dialogue(character=char_name, lines=[first_line])
                elements.append(new_dialogue)
                current_dialogue = new_dialogue
                continue

            # Fallback (Stage Direction)
            elements.append(StageDirection(lines=[stripped_line]))
            current_dialogue = None

        return elements

def render_callback_content(content):
    if '/' in content:
        c, a = content.split('/', 1)
        return f'<span class="cb-call">{c.strip()}</span><span class="cb-sep">/</span><span class="cb-answer">{a.strip()}</span>'
    return f'<span class="cb-std">{content}</span>'

def parse_markup_filter(text):
    text = html.escape(text)
    def overlap_replacer(match):
        dialogue_text = match.group(1)
        callback_raw = match.group(2)
        formatted_cb = render_callback_content(callback_raw)
        return (f'<span class="overlap-group">'
                f'<span class="overlap-cb">{formatted_cb}</span>'
                f'<span class="overlap-text">{dialogue_text}</span>'
                f'</span>')
    text = re.sub(r'\{(.*?)\}\s*&lt;(.*?)&gt;', overlap_replacer, text)
    text = re.sub(r'\(\((.*?)\)\)', r'<span class="crowd-cue">PROPS: \1</span>', text)
    text = re.sub(r'\[\[(.*?)\]\]', r'<span class="cast-cue">CAST: \1</span>', text)
    text = re.sub(r'\[(.*?)\]', r'<span class="event-cue">\1</span>', text)
    text = re.sub(r'&lt;(.*?)&gt;', lambda m: render_callback_content(m.group(1)), text)
    return text

def main():
    base_path = Path(__file__).parent
    input_path = base_path / INPUT_FILE
    template_path = base_path / TEMPLATE_FILE
    output_path = base_path / OUTPUT_FILE

    if not input_path.exists():
        print(f"Error: {INPUT_FILE} not found.")
        return
    
    print(f"Rendering {INPUT_FILE}...")
    with open(input_path, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    parser = RhpsParser()
    script_objects = parser.parse(raw_text)

    scenes_list = []
    scene_counter = 0
    for element in script_objects:
        if isinstance(element, SceneHeader):
            scene_counter += 1
            element.number = scene_counter
            element.id = f"scene-{scene_counter}"
            scenes_list.append(element)

    env = Environment(loader=FileSystemLoader(str(base_path)))
    env.filters['render_markup'] = parse_markup_filter
    
    try:
        template = env.get_template(TEMPLATE_FILE)
        html_output = template.render(script=script_objects, scenes=scenes_list)
    except Exception as e:
        print(f"Template Rendering Error: {e}")
        return

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_output)
    

if __name__ == "__main__":
    main()