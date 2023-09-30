class ChatHistory:
    def __init__(self, instruction_template, max_history=3):
        self.max_history = max_history
        self.history = []
        self.instruction_template = instruction_template

    def add_message(self, message):
        self.history.append(message)
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def summarize_history(self, history, llm, chat_summarization_instruction):
        history = llm(
            self.instruction_template.format(
                instruction=chat_summarization_instruction + '\n' + history
            ),
            max_tokens=2048,
            echo=False,
        )
        self.history = [history["choices"][0]["text"]]

        return self.get_chat_history()

    def get_chat_history(self):
        history = "\n".join(self.history)
        return history
