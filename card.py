from dataclasses import dataclass

from common import (
    call_metabase_api,
    get_source_table,
    modify_field_values,
)
from table import Table


@dataclass
class Card:
    id: int
    data: str = None

    def _get_question(self):
        query_endpoint = f"card/{self.id}"
        return call_metabase_api(query_endpoint)

    def __post_init__(self):
        self.data = self.data or self._get_question()

    def save(self):
        query_endpoint = f"card/{self.id}"
        return call_metabase_api(query_endpoint, method="PUT", data=self.data)

    def update_references(self, table: Table) -> bool:
        if self.data["query_type"] == "native":
            self.data["dataset_query"]["native"]["query"] = table.update_query(
                self.data["dataset_query"]["native"]["query"]
            )
            self.update_field_id_in_variables(
                table,
            )
            return True
            # c.save()

        if self.data["query_type"] == "query":
            if get_source_table(self.data["dataset_query"]) != table.old_id:
                return False

            self.data["dataset_query"]["stages"][0]["source-table"] = table.new_id

            self.data["dataset_query"] = modify_field_values(
                self.data["dataset_query"],
                table,
            )
            return True
        return False

    def update_field_id_in_variables(self, table):
        """
        This method replaces, in the variable reference, the old column/field id with the corresponding
        column/field id on the new table.
        """

        variables = self.data["dataset_query"]["native"].get("template-tags", {})

        for _, tag in variables.items():
            dimension = tag.get("dimension")
            # Not all template-tags are variables, so we need to skip some of them
            if (
                dimension  # to skip snippet
                and len(dimension) == 3
                and dimension[0] == "field"
                and isinstance(dimension[2], (int, float))
                and table.is_field_in_old_table(dimension[2])
            ):
                # Reuse the recursive MBQL5 ref mutator for native template tag dimensions.
                tag["dimension"] = modify_field_values(dimension, table)
