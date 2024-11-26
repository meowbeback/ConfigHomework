import subprocess
import datetime
import argparse
import os
import subprocess
def get_commits_after_date(repo_path, date):
    date_str = date.strftime("%Y-%m-%d")
    git_command = [
        "git", "log", "--after", date_str, "--pretty=format:%H"
    ]
    result = subprocess.run(git_command, cwd=repo_path, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception("Ошибка при выполнении команды git log")

    commits = result.stdout.strip().split("\n")
    return commits

def get_changed_files(repo_path, commit_hash):
    git_command = [
        "git", "diff-tree", "--no-commit-id", "--name-only", "-r", commit_hash
    ]
    result = subprocess.run(git_command, cwd=repo_path, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Ошибка при получении измененных файлов для коммита {commit_hash}")

    files = result.stdout.strip().split("\n")
    return files


def sanitize_filename(filename):
    if not filename:
        return None

    sanitized = filename.replace("/", "_").replace("?", "_").replace(":", "_").replace("*", "_").replace(" ", "_")
    sanitized = sanitized.replace(".", "_")
    return sanitized

def build_dependency_graph(repo_path, commits):
    graph = "@startuml\n"
    for commit in commits:
        files = get_changed_files(repo_path, commit)

        if not files:
            continue

        commit_node = f"commit_{commit[:7]}"
        graph += f"entity {commit_node} as \"{commit[:7]}\"\n"

        for file in files:
            file_node = sanitize_filename(file)

            if not file_node:
                continue

            graph += f"entity {file_node} as \"{file}\"\n"
            graph += f"{commit_node} --> {file_node}\n"

    graph += "@enduml\n"
    return graph


def render_graph(plantuml_path, graph):
    with open("graph.puml", "w") as f:
        f.write(graph)

    plantuml_command = [plantuml_path, "graph.puml"]
    result = subprocess.run(plantuml_command, capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception("Ошибка при рендеринге графа с помощью PlantUML")

    # Выводим результат на экран
    with open("graph.png", "rb") as f:
        print(f.read())


def main():
    # Обработка аргументов командной строки
    parser = argparse.ArgumentParser(description="Генератор графа зависимостей для Git репозитория.")
    parser.add_argument("plantuml_path", help="Путь к программе PlantUML для рендеринга графов.")
    parser.add_argument("repo_path", help="Путь к анализируемому Git репозиторию.")
    parser.add_argument("date", help="Дата коммитов для фильтрации (в формате YYYY-MM-DD).")

    args = parser.parse_args()

    try:
        date = datetime.datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Некорректный формат даты. Используйте формат YYYY-MM-DD.")

    commits = get_commits_after_date(args.repo_path, date)

    graph = build_dependency_graph(args.repo_path, commits)

    render_graph(args.plantuml_path, graph)


if __name__ == "__main__":
    main()