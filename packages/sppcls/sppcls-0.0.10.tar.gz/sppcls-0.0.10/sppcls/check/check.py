import csv
from os.path import isfile


def read_tokens(token_file_path):
    result = []

    with open(token_file_path, 'r', encoding='utf-8') as token_file:
        reader = csv.reader(token_file, delimiter='\t')

        header = next(reader, None)
        column_count = len(header)

        for row in reader:
            if len(row) == 1:
                result.append(row[0])
            else:
                result.append(row)

    return column_count, result


def check_for_issues(org_tokens, project_tokens, column_count):

    if len(org_tokens) != len(project_tokens):
        raise Exception("Token lists differ in length")

    for line, (org_token, project_token) in enumerate(zip(org_tokens, project_tokens)):
        if isinstance(org_token, str):
            if not isinstance(project_token, str):
                raise Exception(f"Tokens don't match (line {line + 2})")

            continue

        if len(project_token) != column_count:
            raise Exception(f"Incorrect column count (line {line + 2})")

        for i in range(0, len(org_token)):
            if org_token[i] != project_token[i]:
                raise Exception(f"Tokens don't match (line {line + 2}, position {i + 1})")


def main(org_tokens_file_path, project_tokens_file_path):

    if not isfile(org_tokens_file_path) or not org_tokens_file_path.endswith(".tsv"):
        raise Exception("Invalid original tokens tsv file path")

    if not isfile(project_tokens_file_path) or not project_tokens_file_path.endswith(".tsv"):
        raise Exception("Invalid project tokens tsv file path")

    print(f'Compare {org_tokens_file_path} and {project_tokens_file_path}')

    _, org_tokens = read_tokens(org_tokens_file_path)
    project_column_count, project_tokens = read_tokens(project_tokens_file_path)

    check_for_issues(org_tokens, project_tokens, project_column_count)

    print("No issues found")


if __name__ == '__main__':
    pass
