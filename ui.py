from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input
from textual.widgets import Markdown
from textual.containers import VerticalScroll
from ollama import chat


class MarkdownApp(App):
    CSS_PATH = "layout.tcss"
    BINDINGS = [("q", "quit", "Quit app")]

    md_viewer: Markdown
    input_prompt: Input

    def compose(self) -> ComposeResult:
        yield Header()
        self.md_viewer = Markdown("# Chat output will appear here.")
        self.md_viewer.code_indent_guides = True
        self.input_prompt = Input(placeholder="Enter the question")
        with VerticalScroll():
            yield self.md_viewer
        yield self.input_prompt
        yield Footer()

    def on_mount(self) -> None:
        self.theme = "catppuccin-mocha"

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        prompt = self.input_prompt.value
        self.input_prompt.value = ""
        self.md_viewer.focus()
        self.run_worker(self.run_llm_stream(prompt), exclusive=True)

    async def run_llm_stream(self, prompt: str):

        await self.md_viewer.update("Generating your answer.")

        stream = chat(
            model="gemma3:1b",
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        # Buffer for all markdown received so far
        full_text = ""
        # Stream chunks from Ollama
        for chunk in stream:
            token = chunk["message"]["content"]
            full_text += token

        # Update markdown live
        await self.md_viewer.update(full_text)


if __name__ == "__main__":
    app = MarkdownApp()
    app.run()
