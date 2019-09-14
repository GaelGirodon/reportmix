from collections import OrderedDict
from typing import List

import jinja2

from reportmix.exporter import Exporter
from reportmix.models.issue import Issue
from reportmix.models.severity import SEVERITIES


class HtmlExporter(Exporter):
    """
    Export a merged report to a HTML file.
    """

    def export(self, output_file: str, issues: List[Issue], fields: List[str]):
        # Load HTML template
        env = jinja2.Environment(
            loader=jinja2.PackageLoader("reportmix.exporters", "templates"),
            autoescape=jinja2.select_autoescape(['html'])
        )
        # Custom filters
        env.filters["limit"] = limit
        env.filters["prettyfield"] = pretty_field
        # Report template
        template = env.get_template('reportmix.html.jinja2')

        # Prepare templates values and statistics
        # Issues by tool
        tools = OrderedDict()
        for t in sorted(set([i.tool.name for i in issues]), key=lambda tool_name: tool_name.casefold()):
            tools[t] = len([i for i in issues if i.tool.name == t])
        # Issues by severity
        severities = OrderedDict()
        for s in SEVERITIES:
            severities[s.name] = len([i for i in issues if i.severity == s])
        # Issues by type
        types = OrderedDict()
        for t in sorted(set([i.type for i in issues]), key=lambda type: type.casefold()):
            types[t] = len([i for i in issues if i.type == t])
        # Render and write report
        with open(output_file, "wb") as output_file:
            output = template.render(title="Issues Report", logo=self.config["logo"],
                                     issues=[i.flatten() for i in issues], fields=fields,
                                     tools=tools, severities=severities, types=types)
            output_file.write(output.encode("utf-8"))


#
# Custom filters
#

def limit(value, max_length: int = 64) -> str:
    """
    Limit a value to a maximum length. If the value length is greater than max_length,
    the value is truncated, '...' is added at the end of the string,
    and the value is wrapped inside a <span> tag with a title containing
    the full string to allow the user to display it in a tooltip on hovering.
    :param value: Raw value
    :param max_length: Maximum string length (number of characters)
    :return: The output HTML code
    """
    val = str(value)
    if len(val) <= max_length:
        return val
    else:
        return '<span title="{}">{}</span>'.format(val, val[:max_length] + "...")


def pretty_field(value: str) -> str:
    """
    Format a snake_case field for display (snake_case -> Snake case)
    and make some other adjustments (identifier => id).
    :param value: Raw field name
    :return: Field to display
    """
    return value.capitalize().replace("_", " ").replace("identifier", "id")
