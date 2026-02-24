from openai import OpenAI

class ai:
    def __init__(self, key):
        self.client = OpenAI(api_key=key)

    
    def talk_openai(self, question, instruction = "Give a short reply"):
        response = self.client.responses.create(
            model="gpt-5",
            instructions=f"You are a bot named Jarvis on a discord servers of some friends studying computer science. Please {instruction}",
            input=question
        )

        return response.output_text, response.usage
    
    def code_openai(self, question, instruction):
        response = self.client.responses.create(
            model="gpt-5",
            instructions=f"You are a bot named Jarvis on a discord server of some friends studying computer science. You are an expert on the field and you can provide a perfect answer to any question regarding our studies. Please {instruction}",
            input = question
        )

        return response.output_text, response.usage
    

    def vibe_openai(self, question, instruction, file, mode):
        if mode == 0:
            text = ""
            with open(file, "r") as file:
                text = file.read()
            response = self.client.responses.create(
                model="gpt-5",
                instructions=f"{question}. {instruction}",
                input = text
            )

            return response.output_text, response.usage
        elif mode == 1:
            text = ""
            with open(file, "r") as file:
                text = file.read()
            response = self.client.responses.create(
                model="gpt-5",
                instructions=f"Improved code {question}. {instruction}. The old code is the input",
                input = text
            )

            return response.output_text, response.usage


    def solve_openai(self, question, instruction, file, mode):
        text = ""
        if (mode == 1):
            with open(file, "r") as file:
                text = file.read()
        elif (mode == 0):
            text = file

        instruction += text
        response = self.client.responses.create(
            model="gpt-5",
            instructions=f"You are a bot named Jarvis on a discord server of some friends studying computer science. You are an expert on the field and you can provide a perfect answer to any question regarding our studies. Please {instruction}.",
            input=question
        )

        return response.output_text, response.usage
    
    def summarize_openai(self, question, instruction, file, mode):
        text = ""
        if (mode == 1):
            with open(file, "r") as file:
                text = file.read()
        elif (mode == 0):
            text = file

        instruction += text
        response = self.client.responses.create(
            model="gpt-5",
            instructions=f"You are a bot named Jarvis on a discord server of some friends studying computer science. You are an expert on the field and you can provide a perfect answer to any question regarding our studies. Please {instruction}",
            input=question
        )

        return response.output_text, response.usage

    def quiz_openai(self, question, instruction, file, mode):
        text = ""
        if (mode == 1):
            with open(file, "r") as file:
                text = file.read()
        elif (mode == 0):
            text = file

        instruction += text
        response = self.client.responses.create(
            model="gpt-5",
            instructions=f"You are a bot named Jarvis on a discord server of some friends studying computer science. You are an expert on the field and you can provide a perfect answer to any question regarding our studies. Please {instruction}",
            input=question
        )

        return response.output_text, response.usage