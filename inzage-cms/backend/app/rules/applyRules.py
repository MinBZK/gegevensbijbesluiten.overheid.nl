import inspect
import re
from glob import glob
from importlib import util
from os import path
from pathlib import Path

from app import schemas
from app.rules._superrule import SuperRule


class ExpertService:
    def __init__(self) -> None:
        self.rule_path = Path(__file__).parent.parent / "rules"
        self.rules: list[SuperRule] = self.register_rules()

    def __atoi(self, text):
        return int(text) if text.isdigit() else text

    def __natural_keys(self, text):
        """
        alist.sort(key=natural_keys) sorts in human order
        http://nedbatchelder.com/blog/200712/human_sorting.html
        (See Toothy's implementation in the comments)
        '"""
        return [self.__atoi(c) for c in re.split(r"(\d+)", text)]

    def register_rules(self) -> list[SuperRule]:
        """
        Registers the defined rules by walking over the rules folder
        and adding all rule classes to the experts rule knowledge base.
        Rules have to be subclass of SuperRule in order to be registered.

        Returns the found set of rule class objects.
        """
        rules = []
        start_path = path.abspath(self.rule_path)
        pattern = "**/*.py"
        py_files = [
            f
            for f in sorted(
                glob(path.join(start_path, pattern), recursive=True),
                key=self.__natural_keys,
            )
            if not f.endswith("__.py")
        ]

        for py_file in py_files:
            spec = util.spec_from_file_location("", py_file)
            module = util.module_from_spec(spec)
            spec.loader.exec_module(module)
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, SuperRule) and name != "SuperRule":
                    rules.append(obj)
        return rules

    def validate_structure(self, content) -> list[schemas.rules.ValidateStructureResult]:
        findings = []
        applicable_rules = [r() for r in self.rules]

        for rule in applicable_rules:
            try:
                results = rule.applyRule(content)
                findings.append(
                    {
                        "ruleId": rule.get_code,
                        "name": rule.get_name,
                        "explanation": rule.get_explanation,
                        "importance": rule.get_importance_displayname,
                        "result": results != None,  # noqa
                        "content": results,
                    }
                )
            except Exception:
                findings.append(
                    {
                        "ruleId": rule.get_code,
                        "name": rule.get_name,
                        "explanation": rule.get_explanation,
                        "importance": rule.get_importance_displayname,
                        "result": True,
                        "content": [{"feedback_message": rule.get_exception_message}],
                    }
                )

        return [schemas.rules.ValidateStructureResult.model_validate(f) for f in findings]
