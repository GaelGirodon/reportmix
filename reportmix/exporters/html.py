from collections import OrderedDict
from os import path
from typing import List

import jinja2

from reportmix.exporter import Exporter
from reportmix.report.issue import Issue
from reportmix.report.severity import SEVERITIES


class HtmlExporter(Exporter):
    """
    Export a merged report to a HTML file.
    """

    def export(self, dest: str, issues: List[Issue]):
        # Load HTML template
        templates = path.realpath(path.join(path.dirname(__file__), "..", "..", "assets", "templates"))
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(templates),
            autoescape=jinja2.select_autoescape(['html'])
        )
        # Custom filters
        env.filters["limit"] = limit
        # Report template
        template = env.get_template('reportmix.html.jinja2')

        # Prepare templates values
        # Issues by tool
        tools = {}
        for t in set([i.tool_name for i in issues]):
            tools[t] = len([i for i in issues if i.tool_name == t])
        # Issues by severity
        severities = OrderedDict()
        for s in SEVERITIES:
            severities[s.name] = len([i for i in issues if i.severity == s])
        # Issues by type
        types = {}
        for t in set([i.type for i in issues]):
            types[t] = len([i for i in issues if i.type == t])
        # Render and write report
        with open(dest, "wb") as output_file:
            output = template.render(title="Issues Report", issues=issues,
                                     tools=tools, severities=severities, types=types)
            output_file.write(output.encode("utf-8"))


#
# Custom filters
#

def limit(value, max_length: str = 64) -> str:
    """
    Limit a value to a maximum length. If the value length is greater than max_length,
    the value is truncated, '...' is added at the end of the string,
    and the value is wrapped inside a <span> tag with a title containing
    the full string to allow the user to display it in a tooltip on hovering.
    :param value: Raw value
    :param max_length: Maximum string length (number of characters)
    :return: The output HTML code
    """
    if len(value) <= max_length:
        return value
    else:
        return '<span title="{}">{}</span>'.format(value, value[:max_length] + "...")
