from prompt_toolkit import Application
from prompt_toolkit.layout import Layout, HSplit
from prompt_toolkit.widgets import TextArea, Label
from prompt_toolkit.key_binding import KeyBindings
import pyperclip

# Instructions at the top
instructions = Label(text=(
    "Bitmapper Beta (In-Place Editor)\n"
    "Commands:\n"
    "  CTRL+D = quit and copy\n"
    "  Arrows = move cursor\n"
    "  ENTER = new line, BACKSPACE = delete"
))

# Blank line to separate instructions from editor
spacer = Label(text="")

# Editable text area
editor = TextArea(multiline=True, wrap_lines=False)

# Key bindings
kb = KeyBindings()

@kb.add('c-d')  # CTRL+D
def _(event):
    """Quit application."""
    event.app.exit()

# Layout: instructions, spacer, editor
root_container = HSplit([instructions, spacer, editor])
layout = Layout(container=root_container, focused_element=editor)

app = Application(layout=layout, full_screen=True, key_bindings=kb)

def main():
    app.run()
    text = editor.text.splitlines()
    bitmap = [list(line) for line in text]
    pyperclip.copy(str(bitmap))
    print(bitmap)
    print("\nCopied to clipboard:")
    print(bitmap)

if __name__ == "__main__":
    main()
