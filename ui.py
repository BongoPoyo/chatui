from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input
from textual.widgets import Markdown
from textual.containers import VerticalScroll
from ollama import chat


class ChaTUI(App):
    CSS_PATH = "layout.tcss"
    BINDINGS = [("q", "quit", "Quit app"),
                ("a", "focus_text", "Focus Text Field")
                ]
    full_text = ""

    md_viewer: Markdown
    input_prompt: Input

    def compose(self) -> ComposeResult:
        yield Header("CHATUI")
        self.md_viewer = Markdown("# Chat output will appear here.")
        self.md_viewer.code_indent_guides = True
        self.input_prompt = Input(placeholder="Enter the question")
        with VerticalScroll():
            yield self.md_viewer
        yield self.input_prompt
        yield Footer()

    def on_mount(self) -> None:
        self.theme = "catppuccin-mocha"

    def action_focus_text(self) -> None:
        self.md_viewer.blur()
        self.input_prompt.focus()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        prompt = self.input_prompt.value
        self.input_prompt.value = ""
        event.input.blur()

        self.md_viewer.focus()
        self.run_worker(self.run_llm_stream(prompt), exclusive=True)

    async def run_llm_stream(self, prompt: str):

        stream = chat(
            model="gemma3:1b",
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )
        self.full_text += "\n\n # Question: " + prompt + "\n\n"
        for chunk in stream:
            token = chunk["message"]["content"]
            self.full_text += token
            # Update markdown live
            await self.md_viewer.update(self.full_text)


if __name__ == "__main__":
    app = ChaTUI()
    app.run()
