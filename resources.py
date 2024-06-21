from typing import List
import os
import json

def print_with_indent(value, indent=0):
    tab = '\t' * indent
    print(f'{tab}{str(value)}')


class Entry:
    def __init__(self, title, entries=None, parent=None):
        self.title = title
        if entries is None:
            self.entries = []
        else:
            self.entries = entries
        self.parent = parent

    def __str__(self):
        return f"{self.title}"

    def add_entry(self, entry):
        self.entries.append(entry)
        if entry.parent == None:
            entry.parent = self

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        # if self.entries is not None:
        for e in self.entries:
            e.print_entries(indent + 1)

    def json(self):
        grocery_json = {
            'title': self.title,
            'entries': [x.json() for x in self.entries]
        }
        # for entry in self.entries:
        #     grocery_json['entries'].append(entry.title)
        return grocery_json

    @classmethod
    def from_json(cls, value: dict):
        new_entry = cls(value['title'])
        for v in value.get('entries', []):
            new_entry.add_entry(entry_from_json(v))
        return new_entry

    def save(self, path):
        content = self.json()
        with open(f'{path}/{self.title}.json', 'w', encoding='utf-8') as f:
            json.dump(content, f)

    @classmethod
    def load(cls, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            content = json.load(f)
        print(content)
        return Entry.from_json(content)


def entry_from_json(value: dict) -> Entry:
    # print(isinstance(value, dict))
    # json_value = json.loads(value)
    new_entry = Entry(value.get('title'))
    for v in value.get('entries', []):
        new_entry.add_entry(entry_from_json(v))
    return new_entry


class EntryManager:
    def __init__(self, data_path: str):
        self.data_path: str = data_path
        self.entries: List[Entry] = []

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)

    def load(self):
        files = os.listdir(self.data_path)
        # print(files)
        for file in files:
            # print(file)
            if file.endswith('.json'):
                print(os.path.join(self.data_path, file))
                entry = Entry.load(os.path.join(self.data_path, file))
                self.entries.append(entry)

    def add_entry(self, title: str):
        self.entries.append(Entry(title))