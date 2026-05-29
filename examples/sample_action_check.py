import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kineshield.feasibility.feasibility_checker import FeasibilityChecker
from kineshield.parser.action_parser import parse_action


def main() -> None:
    sample_path = ROOT / "benchmark" / "sample_cases.json"
    cases = json.loads(sample_path.read_text())

    checker = FeasibilityChecker()

    for case in cases:
        action = parse_action(case["action"])
        verdict = checker.check(action)
        print(json.dumps(verdict.to_dict(), indent=2))


if __name__ == "__main__":
    main()
