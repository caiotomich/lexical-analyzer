import tokenize
import json
import re

path_key_words: str = r'./lib/key_words.json'
path_code: str = r'./programs/source_code.c'
path_tokens_file: str = r'./programs/list_of_tokens.txt'


def main():
    # load all key words of language C
    output: list = []
    key_words: list = []
    with open(path_key_words, 'r') as j:
        key_words = json.loads(j.read())

    with tokenize.open(path_code) as f:
        tokens = tokenize.generate_tokens(f.readline)

        # Types: NAME, NUMBER, OP, STRING, COMMENT (include)
        for t in tokens:
            t_name: str = tokenize.tok_name[t.type]
            token: str = None

            # new lines or blank lines
            if t_name in ['NL', 'NEWLINE']:
                continue

            # includes
            elif t.type == tokenize.COMMENT and re.match(r'# include.*', t.string):
                # captura nome do arquivo da biblioteca
                t.string = re.search(r'<(.*)>', t.string).group(1)
                token = 'Reserved Word, "{}" (include), {} ({})'.format(t.string, t.type, t.name)

            # reserved words / key words
            elif t.type == tokenize.NAME and t.string in key_words:
                token = 'Reserved Word, "{}", {} ({})'.format(t.string, t.type, t_name)

            # comments (//)
            elif t.type == tokenize.OP and re.match(r'^\/\/', t.string):
                token = 'Single-line Comment, "{}", {} ({})'.format(t.string, t.type, t_name)

            # identifiers
            elif t.type == tokenize.NAME:
                token = 'Identifier, "{}", {} ({})'.format(t.string, t.type, t_name)

            # operators
            elif t.type == tokenize.OP and re.match(r'[=\-\+\*\/<>%]{1,2}', t.string):
                token = 'Operator, "{}", {} ({})'.format(t.string, t.type, t_name)

            if token is not None:
                print(token)
                output.append(token)

    # save new lines in other file
    with open(path_tokens_file, 'w') as nl:
        nl.write('\n'.join(output))


if __name__ == "__main__":
    main()
