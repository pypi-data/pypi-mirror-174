default_ignore: [str] = ['.idea', '__pycache__', '.next', 'node_modules', 'assets', 'coverage', '.vscode',
                         'public', 'yarn.lock', 'jest.config.ts', '.env.local', 'package.json', 'README.md']


class Writer:
    @staticmethod
    def create_ignore_file(path: str = '.\\'):
        with open(f'{path}\\.counterignore', 'w') as ignore_file:
            for ignore in default_ignore:
                ignore_file.write(f'{ignore}\n')
