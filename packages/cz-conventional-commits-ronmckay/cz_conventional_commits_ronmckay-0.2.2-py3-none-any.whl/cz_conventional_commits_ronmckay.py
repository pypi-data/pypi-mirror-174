import os
import re
import textwrap
from typing import Dict, List, Optional

from commitizen import defaults
from commitizen.cz.base import BaseCommitizen
from commitizen.cz.utils import required_validator
from commitizen.defaults import Questions


def parse_scope(text):
    return "-".join(text.strip().split())


def parse_subject(text):
    if isinstance(text, str):
        text = text.strip(".").strip().capitalize()

    return required_validator(text, msg="Subject is required.")


class RonMcKayConventionalCommits(BaseCommitizen):
    body_max_width = 80
    change_type_map: Optional[Dict[str, str]] = {
        "fix": "Fix",
        "feat": "Feature",
        "docs": "Documentation",
        "style": "Style",
        "refactor": "Refactor",
        "perf": "Performance",
        "test": "Tests",
        "build": "Build",
        "ci": "CI/CD",
    }
    change_type_order: Optional[List[str]] = [
        "BREAKING CHANGE",
        "Feature",
        "Fix",
        "Refactor",
        "Performance",
        "Tests",
        "Documentation",
        "Build",
        "CI/CD",
    ]
    bump_pattern: Optional[str] = (
        r"^(?:(BREAKING[\-\ ]CHANGE|feat|fix|refactor|perf)(\(.+\))?(!)?|"
        r"(docs|style|test|build|ci)(\(.+\))?(!))"
    )  # noqa: E501
    changelog_pattern: Optional[str] = bump_pattern
    bump_map: Optional[Dict[str, str]] = defaults.bump_map
    commit_parser: Optional[
        str
    ] = r"^(?P<change_type>feat|fix|refactor|perf|BREAKING CHANGE|docs|style|test|build|ci)(?:\((?P<scope>[^()\r\n]*)\)|\()?(?P<breaking>!)?:\s(?P<message>.*)?"  # noqa: E501

    def questions(self) -> Questions:
        questions = [
            {
                "type": "list",
                "name": "prefix",
                "message": "Select the type of change you are committing",
                "choices": [
                    {
                        "value": "fix",
                        "name": "fix: A bug fix. Correlates with PATCH in SemVer",
                        "key": "x",
                    },
                    {
                        "value": "feat",
                        "name": "feat: A new feature. Correlates with MINOR in SemVer",
                        "key": "f",
                    },
                    {
                        "value": "docs",
                        "name": "docs: Documentation only changes",
                        "key": "d",
                    },
                    {
                        "value": "style",
                        "name": (
                            "style: Changes that do not affect the "
                            "meaning of the code (white-space, formatting,"
                            " missing semi-colons, etc)"
                        ),
                        "key": "s",
                    },
                    {
                        "value": "refactor",
                        "name": (
                            "refactor: A code change that neither fixes "
                            "a bug nor adds a feature"
                        ),
                        "key": "r",
                    },
                    {
                        "value": "perf",
                        "name": "perf: A code change that improves performance",
                        "key": "p",
                    },
                    {
                        "value": "test",
                        "name": (
                            "test: Adding missing or correcting " "existing tests"
                        ),
                        "key": "t",
                    },
                    {
                        "value": "build",
                        "name": (
                            "build: Changes that affect the build system or "
                            "external dependencies (example scopes: pip, docker, npm)"
                        ),
                        "key": "b",
                    },
                    {
                        "value": "ci",
                        "name": (
                            "ci: Changes to our CI configuration files and "
                            "scripts (example scopes: GitLabCI)"
                        ),
                        "key": "c",
                    },
                ],
            },
            {
                "type": "input",
                "name": "scope",
                "message": (
                    "What is the scope of this change? (class or file name): "
                    "(press [enter] to skip)\n"
                ),
                "filter": parse_scope,
            },
            {
                "type": "input",
                "name": "subject",
                "filter": parse_subject,
                "message": (
                    "Write a short and imperative summary of the code changes: "
                    "(starting upper case and no period)\n"
                ),
            },
            {
                "type": "input",
                "name": "body",
                "message": (
                    "Provide additional contextual information about the code changes: "
                    "(press [enter] to skip)\n"
                ),
                "filter": lambda ans: "\n".join(
                    textwrap.wrap(ans, width=self.body_max_width)
                ),
            },
            {
                "type": "confirm",
                "message": "Is this a BREAKING CHANGE? Correlates with MAJOR in SemVer",
                "name": "is_breaking_change",
                "default": False,
            },
            {
                "type": "input",
                "name": "footer",
                "message": (
                    "Footer. Information about Breaking Changes and "
                    "reference issues that this commit closes: "
                    "(press [enter] to skip)\n"
                ),
            },
        ]

        return questions

    def message(self, answers: dict) -> str:
        prefix = answers["prefix"]
        scope = answers["scope"]
        subject = answers["subject"]
        body = answers["body"]
        footer = answers["footer"]
        is_breaking_change = answers["is_breaking_change"]

        if scope:
            scope = f"({scope})"
        if body:
            body = f"\n\n{body}"
        if is_breaking_change:
            footer = f"BREAKING CHANGE: {footer}" if footer else ""
        if footer:
            footer = f"\n\n{footer}"

        message = (
            f"{prefix}{scope}{'!' if is_breaking_change else ''}: "
            f"{subject}{body}{footer}"
        )

        return message

    def example(self) -> str:
        return (
            "fix: Correct minor typos in code\n"
            "\n"
            "see the issue for details on the typos fixed\n"
            "\n"
            "closes issue #12"
        )

    def schema(self) -> str:
        return (
            "<type>(<scope>): <subject>\n"
            "<BLANK LINE>\n"
            "<body>\n"
            "<BLANK LINE>\n"
            "(BREAKING CHANGE: <footer>)"
        )

    def schema_pattern(self) -> str:
        PATTERN = (
            r"(?s)"  # To explictly make . match new line
            r"(build|ci|docs|feat|fix|perf|refactor|style|test|chore|revert|bump)"
            r"(\(\S+\))?!?:"  # scope
            r"( [A-Z][^\n\r]+)"  # subject
            r"((\n\n.*)|(\s*))?$"
        )
        return PATTERN

    def info(self) -> str:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        filepath = os.path.join(dir_path, "conventional_commits_ronmckay_info.txt")
        with open(filepath, "r") as f:
            content = f.read()
        return content

    def process_commit(self, commit: str) -> str:
        pat = re.compile(self.schema_pattern())
        m = re.match(pat, commit)
        if m is None:
            return ""
        return m.group(3).strip()


discover_this = RonMcKayConventionalCommits
