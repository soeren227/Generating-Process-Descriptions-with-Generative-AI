"""This is the module that extracts the time information from the patient journey."""
from datetime import datetime
from pathlib import Path

from ..logging import log_execution_time
from ..module import Module
from .. import prompts as p
from .. import utils as u


class TimeExtractor(Module):
    """
    This is the module that extracts the time information from the patient journey. This includes start dates,
    end dates and durations.
    """

    def __init__(self):
        super().__init__()
        self.name = "Time Extractor"
        self.description = "Extracts the timestamps for the corresponding activity labels from a patient journey."

    @log_execution_time(Path("extraction/logs/execution_time.log"))
    def execute(self, df, patient_journey=None):
        super().execute(df, patient_journey)
        df["start_date"] = df["event_information"].apply(self.__extract_start_date)
        df["end_date"] = df.apply(self.__extract_end_date, axis=1)
        df["duration"] = df.apply(self.__calculate_row_duration, axis=1)
        return df

    def __extract_start_date(self, activity_label):
        """Extract the start date for a given activity."""
        messages = [
            {"role": "system", "content": p.START_DATE_CONTEXT},
            {
                "role": "user",
                "content": f"{p.START_DATE_PROMPT} \nThe text: {self.patient_journey} \n"
                f"The bulletpoint: {activity_label}",
            },
            {"role": "assistant", "content": p.START_DATE_ANSWER},
        ]
        output = u.query_gpt(messages)
        fc_message = [
            {"role": "system", "content": p.FC_START_DATE_CONTEXT},
            {"role": "user", "content": p.FC_START_DATE_PROMPT + "The text: " + output},
        ]
        start_date = u.query_gpt(
            fc_message,
            tool_choice={"type": "function", "function": {"name": "add_start_dates"}},
        )

        return start_date

    def __extract_end_date(self, row):
        """Extract the end date for a given activity."""
        messages = [
            {"role": "system", "content": p.END_DATE_CONTEXT},
            {
                "role": "user",
                "content": f"{p.END_DATE_PROMPT} \nThe text: {self.patient_journey} \nThe bulletpoint: "
                f"{row['event_information']} \nThe start date: {row['start_date']}",
            },
            {"role": "assistant", "content": p.END_DATE_ANSWER},
        ]
        output = u.query_gpt(messages)
        fc_message = [
            {"role": "system", "content": p.FC_END_DATE_CONTEXT},
            {"role": "user", "content": p.FC_END_DATE_PROMPT + "The text: " + output},
        ]
        end_date = u.query_gpt(
            fc_message,
            tool_choice={"type": "function", "function": {"name": "add_end_dates"}},
        )

        return end_date

    @staticmethod
    def __calculate_row_duration(row):
        """Calculate the duration for a given activity."""
        if row["start_date"] == "N/A" or row["end_date"] == "N/A":
            return "N/A"
        start_date = datetime.strptime(row["start_date"], "%Y%m%dT%H%M")
        end_date = datetime.strptime(row["end_date"], "%Y%m%dT%H%M")
        duration = end_date - start_date
        hours, remainder = divmod(duration.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)

        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
