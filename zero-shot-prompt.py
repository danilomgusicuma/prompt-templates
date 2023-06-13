from pydantic import create_model
import re


class ZeroShotPrompt:
    """
    A class representing a text template with variable placeholders that can be replaced with actual values.

    Attributes:
        template (str): The template string with variable placeholders.

    Methods: fill_variables(**variables): Fills the template placeholders with the provided variables and returns the
    filled text.
    """

    def __init__(self, template):
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
        """
        variables_instance = self._variables_model(**variables)
        filled_text = self._template.format(**variables_instance.dict())
        return filled_text


if __name__ == "__main__":
    zero_shot_template = ZeroShotPrompt("Good morning, {name}!")
    prompt = zero_shot_template.fill_variables(name="Danilo")
    print(prompt)
