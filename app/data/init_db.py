"""
Database definition creation.
"""

from data import models, database


def main():
    models.Base.metadata.create_all(bind=database.engine)


if __name__ == "__main__":
    main()
