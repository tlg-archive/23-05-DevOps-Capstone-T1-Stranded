#imports
from os import path
import json

class Parser:
    def __init__(self) -> None:
        with open(
            path.abspath(f"{'/'.join(path.abspath(__file__).split('/')[:-1])}/../data/actions.json"),
            encoding="utf-8"
            ) as actions_file:
            actions = json.load(actions_file)

        self.action_list: list[str] = []
        self.action_synonyms: dict[str, str] = {}

        for action in list(actions.keys()):
            self.action_list.append(action)
            for synonym in actions[action]:
                self.action_synonyms[synonym] = action

        with open(
            path.abspath(f"{'/'.join(path.abspath(__file__).split('/')[:-1])}/../data/selectors.json"),
            encoding="utf-8"
            ) as selectors_file:
            selectors = json.load(selectors_file)

        self.selector_list: list[str] = []
        self.selector_synonyms: dict[str, str] = {}

        for selector in list(selectors.keys()):
            self.selector_list.append(selector)
            for synonym in selectors[selector]:
                self.selector_synonyms[synonym] = selector

        with open(
            path.abspath(f"{'/'.join(path.abspath(__file__).split('/')[:-1])}/../data/reservedkeywords.json"),
            encoding="utf-8"
            ) as keywords_file:
            keywords = json.load(keywords_file)

        self.reserved_list: list[str] = []
        self.reserved_synonyms: dict[str, str] = {}

        for keyword in list(keywords.keys()):
            self.reserved_list.append(keywords)
            for synonym in keywords[keyword]:
                self.reserved_synonyms[synonym] = keyword

    def process_token(self, token: str) -> str:
        if token in self.action_list:
            return token
        if token in list(self.action_synonyms.keys()):
            return self.action_synonyms[token]
        if token in self.selector_list:
            return None
            # return token
        if token in list(self.selector_synonyms.keys()):
            return None
            #return self.selector_synonyms[token]
        if token in self.reserved_list:
            return token
        if token in list(self.reserved_synonyms.keys()):
            return self.reserved_synonyms[token]
        return token


    def parse(self, user_input: str) -> None:
        tokens = user_input.split()

        command = []
        for token in tokens:
            processed = self.process_token(token)
            if processed:
                if processed in self.selector_list:
                    if len(command) < 1:
                        continue
                    elif command[-1] not in self.selector_list and command[0] not in self.selector_list:
                        command.append(processed)
                else:
                    command.append(processed)
        return command
