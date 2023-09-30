from llama_cpp import Llama

from chat_history_management import ChatHistory
from scrape import download_text_from_url, extract_urls


class LLM:
    def __init__(self, conf, console) -> None:
        self.conf = conf
        self.console = console
        with open(conf["prompt_template"]) as f:
            self.conf["prompt_template"] = f.read()
        with open(conf["system_prompt"]) as f:
            self.conf["system_prompt"] = f.read()

        self.llm = Llama(model_path=self.conf["model_path"], n_ctx=2048)
        self.instruction_template = self.format_template(
            self.conf["prompt_template"], self.conf["system_prompt"]
        )
        self.chat_history = ChatHistory(self.instruction_template, 5)

    def format_template(self, template, system_prompt):
        modified_template = template.replace("{system_prompt}", system_prompt)
        return modified_template

    def reply(self, message):
        p = message
        generated_text = ""
        if len(p.strip()) > 0:
            p = self.expand_urls_in_prompt(p)
            prompt = self.instruction_template.format(instruction=p)

            history = self.chat_history.get_chat_history()
            if len(self.llm.tokenize(history.encode("utf-8"))) > 1000:
                history = self.chat_history.summarize_history(
                    history,
                    self.llm,
                    self.conf["chat_summarization_instruction"],
                )

            generator = self.llm(
                history + "\n" + prompt,
                max_tokens=2048,
                echo=False,
                stop=["[INST]", "<<SYS>>", "</s>", "<s>", "<</sys>>"],
                stream=True,
            )
            for t in generator:
                token = t["choices"][0]["text"]
                generated_text += token
                yield token
            self.chat_history.add_message(prompt + generated_text)

    def chat(
        self,
    ):
        while True:
            p = self.console.input("You: ")
            if len(p.strip()) > 0:
                p = self.expand_urls_in_prompt(p)
                prompt = self.instruction_template.format(instruction=p)

                history = self.chat_history.get_chat_history()
                if len(self.llm.tokenize(history.encode("utf-8"))) > 1000:
                    history = self.chat_history.summarize_history(
                        history,
                        self.llm,
                        self.conf["chat_summarization_instruction"],
                    )

                gen = self.llm(
                    history + "\n" + prompt,
                    max_tokens=2048,
                    echo=False,
                    stop=["[INST]", "<<SYS>>", "</s>", "<s>", "<</sys>>"],
                    stream=True,
                )
                generated_text = self.generate_text(gen).strip()
                self.chat_history.add_message(prompt + generated_text)
            print()

    def generate_text(self, generator):
        generated_text = ""
        self.console.print("Bot:", end=" ")
        for obj in generator:
            token = obj["choices"][0]["text"]
            generated_text += token
            self.console.print(f"{token}", end="")
        return generated_text

    def expand_urls_in_prompt(self, prompt):
        for url in extract_urls(prompt):
            text = download_text_from_url(url)
            if text and len(text) > 4000:
                text = text[:4000]
            prompt = prompt.replace(url, text if text else "")
        return prompt
