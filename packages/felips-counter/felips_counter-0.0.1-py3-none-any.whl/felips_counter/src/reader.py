import os

default_ignore: [str] = ['.idea', '__pycache__', '.next', 'node_modules', 'assets', 'coverage', '.vscode',
                         'public', 'yarn.lock', 'jest.config.ts', '.env.local', 'package.json', 'README.md']


class Reader:
    def __init__(self, ignore_blank_lines: bool = True, encoding: str = 'UTF-8'):
        self.__ignore_blank_lines: bool = ignore_blank_lines
        self.__encoding: str = encoding
        self.__ignore: [str] = default_ignore

    def __count_document_lines(self, document_path: str) -> int:
        """
        Open a document and count its lines.

        :param document_path: The document path.
        :return: The number of lines of the document.
        """

        try:
            with open(document_path, encoding=self.__encoding) as document:
                document_lines: [str] = document.readlines()
                lines_length: int = len(document_lines)

                for line in document_lines:
                    if self.__ignore_blank_lines and line is '\n':
                        lines_length -= 1
            return lines_length

        except PermissionError:
            return 0
        except UnicodeDecodeError:
            return 0

    @staticmethod
    def __get_ignore_config(ignore_file: str) -> [str]:
        ignore = ['.counterignore']
        with open(ignore_file) as document:
            document_lines: [str] = document.readlines()
            for line in document_lines:
                ignore.append(line.split('\n')[0])
        return ignore

    def open_input_path(self, input_path: str, total_lines: int = 0) -> int:
        if input_path is '.':
            input_path = '\\'

        isdir: bool = os.path.isdir(input_path)
        isfile: bool = os.path.isfile(input_path)

        if isdir:
            documents = os.listdir(input_path)
            if '.counterignore' in documents:
                ignore_file: str = input_path + '\\.counterignore'
                self.__ignore = self.__get_ignore_config(ignore_file)
            for document in documents:
                document_path = os.path.join(input_path, document)
                if os.path.isdir(document_path):
                    if os.path.split(document_path)[-1] in self.__ignore:
                        continue
                    total_lines += self.open_input_path(document_path)
                elif os.path.isfile(document_path):
                    if os.path.split(document_path)[-1] in self.__ignore:
                        continue
                    elif os.path.splitext(document_path)[-1] in self.__ignore:
                        continue
                    total_lines += self.__count_document_lines(document_path)

        elif isfile:
            total_lines += self.__count_document_lines(input_path)

        return total_lines
