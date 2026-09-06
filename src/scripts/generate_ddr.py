import logging

from eralchemy2 import render_er
from sqlmodel import SQLModel

from logger import setup_logger
from shareholder_registry.models import Company, Part, Person, Shares  # noqa: F401

setup_logger(logging.INFO)

logger = logging.getLogger(__name__)


def generate_diagram():
    logger.info("Mapping database entities...")
    render_er(SQLModel.metadata, "datamodel_graph.png")
    logger.info("Success! Created 'datamodel_graph.png' in your root directory.")


if __name__ == "__main__":
    generate_diagram()
