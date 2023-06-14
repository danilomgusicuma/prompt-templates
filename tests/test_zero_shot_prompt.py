import unittest

from prompt_templates.zero_shot.zero_shot_prompt import ZeroShotPrompt


class TextTemplateTests(unittest.TestCase):
    def test_fill_variables(self):
        template = "Hello, {name}! Today is {day}."
        my_template = ZeroShotPrompt(template)

        filled_text = my_template.fill_variables(name="John", day="Monday")
        self.assertEqual(filled_text, "Hello, John! Today is Monday.")

    def test_fill_variables_with_missing_values(self):
        template = "Hello, {name}! Today is {day}."
        my_template = ZeroShotPrompt(template)

        with self.assertRaises(ValueError):
            my_template.fill_variables(name="John")

    def test_fill_variables_with_extra_values(self):
        template = "Hello, {name}! Today is {day}."
        my_template = ZeroShotPrompt(template)

        with self.assertRaises(ValueError):
            my_template.fill_variables(name="John", day="Monday", extra="Extra value")

    def test_fill_variables_with_empty_template(self):
        template = ""
        my_template = ZeroShotPrompt(template)

        filled_text = my_template.fill_variables()
        self.assertEqual(filled_text, "")


if __name__ == "__main__":
    unittest.main()
