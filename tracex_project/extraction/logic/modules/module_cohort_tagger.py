"""This is the module that cohort tags from the patient journey."""
from pathlib import Path
from django.conf import settings

from extraction.models import Prompt
from extraction.logic.module import Module
from tracex.logic.logger import log_execution_time
from tracex.logic import utils as u


class CohortTagger(Module):
    """
    This is the module that extracts the cohort tags from the patient journey.
    """

    def __init__(self):
        super().__init__()
        self.name = "Cohort Tagger"
        self.description = "Extracts the cohort tags from a patient journey."

    @log_execution_time(Path(settings.BASE_DIR / "tracex/logs/execution_time.log"))
    def execute_and_save(
        self, df, patient_journey=None, patient_journey_sentences=None
    ):
        """
        Extracts the cohort from the patient journey and saves the result in the database.
        """
        super().execute_and_save(
            df,
            patient_journey=patient_journey,
            patient_journey_sentences=patient_journey_sentences,
        )

        cohort_tags = self.__extract_cohort_tags(patient_journey)
        cohort_dict = self.__prepare_cohort_dict(cohort_tags)
        cohort_dict_normalized = self.normalize_coniditons_snomed(cohort_dict)

        return cohort_dict_normalized

    @staticmethod
    def __extract_cohort_tags(patient_journey):
        """Extracts information about condition, gender, age, origin and preexisting condition."""
        cohort_data = {}
        for message_list in Prompt.objects.get(name="COHORT_TAG_MESSAGES").text:
            messages = message_list[1:]
            messages.append(
                {"role": "user", "content": patient_journey},
            )
            tag = u.query_gpt(messages)
            cohort_data[message_list[0]] = tag

        return cohort_data

    @staticmethod
    def __prepare_cohort_dict(cohort_data):
        """Prepares the cohort tags dictionary for saving into database."""
        cohort_dict = {
            key: value for key, value in cohort_data.items() if value != "N/A"
        }

        # If all values are "N/A", return None to indicate no valid cohort data
        if not any(value != "N/A" for value in cohort_dict.values()):
            return None

        return cohort_dict

    @staticmethod
    def normalize_coniditons_snomed(cohort_dict):
        """Normalizes conditions to a SNOMED code."""
        condition = cohort_dict.get("condition")
        preexisting_condition = cohort_dict.get("preexisting_condition")

        if condition is not None:
            (
                cohort_dict["condition"],
                cohort_dict["condition_snomed_code"],
            ) = u.get_snomed_ct_info(condition)

        if preexisting_condition is not None:
            (
                cohort_dict["preexisting_condition"],
                cohort_dict["preexisting_condition_snomed_code"],
            ) = u.get_snomed_ct_info(preexisting_condition)

        return cohort_dict
