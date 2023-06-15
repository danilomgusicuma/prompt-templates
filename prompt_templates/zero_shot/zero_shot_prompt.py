from pydantic import create_model
import re

from prompt_templates.base_prompt import BasePrompt


class ZeroShotPrompt(BasePrompt):
    """
    A class representing a text template with variable placeholders that can be replaced with actual values.

    Attributes:
        template (str): The template string with variable placeholders.

    Methods: fill_variables(**variables): Fills the template placeholders with the provided variables and returns the
    filled text.
    """

    def __init__(self, template: str):
        self._template = template
        self._variables_model = self._infer_variables_model()

    @property
    def template(self):
        """
        Gets the template string with variable placeholders.

        Returns:
            str: The template string.
        """
        return self._template

    def _infer_variables_model(self):
        variables = self._extract_template_variables()
        model_fields = {var: (str, ...) for var in variables}
        variables_model = create_model('TemplateVariables', **model_fields)
        return variables_model

    def _extract_template_variables(self):
        pattern = r"{(.*?)}"
        variables = re.findall(pattern, self.template)
        return [var.strip() for var in variables]

    def fill_variables(self, **variables):
        """
        Fills the template placeholders with the provided variables and returns the filled text.

        Args:
            **variables: Keyword arguments representing the variables to be substituted in the template.

        Returns:
            str: The filled text with variables replaced.

        Raises:
            ValueError: If there are extra variables or missing values for required variables.
        """
        expected_variables = self._extract_template_variables()
        extra_variables = [var for var in variables if var not in expected_variables]

        if extra_variables:
            raise ValueError(f"Unexpected variables: {', '.join(extra_variables)}")

        missing_variables = [var for var in expected_variables if var not in variables]
        if missing_variables:
            raise ValueError(f"Missing values for variables: {', '.join(missing_variables)}")

        variables_instance = self._variables_model(**variables)
        filled_text = self.template.format(**variables_instance.dict())
        return filled_text


if __name__ == "__main__":
    zero_shot_template = ZeroShotPrompt("Good morning, {name}!")
    prompt = zero_shot_template.fill_variables()
    print(prompt)
