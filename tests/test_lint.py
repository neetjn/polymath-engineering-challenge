from unittest import TestCase
from pylint.lint import Run


class LintTest(TestCase):

    def test_api_core(self):
        with self.assertRaises(SystemExit) as lint_check:
            Run(['--errors-only', 'polymath'])
        self.assertEqual(lint_check.exception.code, 0)
