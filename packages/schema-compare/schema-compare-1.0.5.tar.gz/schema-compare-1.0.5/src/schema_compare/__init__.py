from importlib import resources


__version__ = "1.0.5"

TEMPLATE = resources.read_text("schema_compare", "report.html")
