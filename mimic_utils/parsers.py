import pandas as pd
import numpy as np


def parse_admission_location(values: pd.Series):
    temp = values.str.title()
    temp = np.where(
        temp.isin(["Emergency Room", "Physician Referral", "Transfer From Hospital"]),
        temp,
        "Other",
    )
    return temp

def parse_gender(values: pd.Series) -> pd.Series:
    mapped_values = np.empty(values.shape[0]) * np.nan
    mapping = {
        "Male": "M",
        "Female": "F",
    }
    for key, regexp in mapping.items():
        mapped_values = np.where(values.str.contains(regexp), key, mapped_values)
    return pd.Series(mapped_values).replace("nan", "Other")

def parse_race(values: pd.Series) -> pd.Series:
    """Parses MIMIC-IV self-identified race-ethnicity within the categories identified by Yarnell et al.

    Yarnell, Christopher J., Alistair Johnson, Tariq Dam, Annemijn Jonkman, Kuan Liu, Hannah Wunsch, Laurent Brochard, et al. 2023.
    “Do Thresholds for Invasive Ventilation in Hypoxemic Respiratory Failure Exist? A Cohort Study.”
    American Journal of Respiratory and Critical Care Medicine 207 (3): 271–82.

    Args:
        values (pd.Series): Input Series.

    Returns:
        pd.Series: Parsed Series.
    """
    mapped_values = np.empty(values.shape[0]) * np.nan
    mapping = {
        "White": "(WHITE)|(PORTUGUESE)",
        "Hispanic": "(HISPANIC)",
        "Asian": "(ASIAN)",
        "Black": "(BLACK)",
        "Other": "(OTHER)|(SOUTH AMERICAN)|(CARIBBEAN ISLAND)|(NATIVE HAWAIIAN OR OTHER PACIFIC ISLANDER)|(AMERICAN INDIAN/ALASKA NATIVE FEDERALLY RECOGNIZED TRIBE)",
    }

    for key, regexp in mapping.items():
        mapped_values = np.where(values.str.contains(regexp), key, mapped_values)
    return pd.Series(mapped_values).replace("nan", "Unknown")

def parse_language(values: pd.Series) -> pd.Series:
    """Parses MIMIC-IV patients' spoken language.

    Args:
        values (pd.Series): Input Series.

    Returns:
        pd.Series: Parsed Series.
    """
    mapped_values = np.empty(values.shape[0]) * np.nan
    mapping = {"English": "(ENGLISH)", "Other": "(\?)"}

    for key, regexp in mapping.items():
        mapped_values = np.where(values.str.contains(regexp), key, mapped_values)
    return mapped_values

def parse_insurance(values: pd.Series) -> pd.Series:
    """Parses MIMIC-IV patients'Insurance.

    Args:
        values (pd.Series): Input Series.

    Returns:
        pd.Series: Parsed Series.
    """
    mapped_values = np.empty(values.shape[0]) * np.nan
    mapping = {
        "Medicaid": "(Medicaid)",
        "Medicare": "(Medicare)",
        "Other": "(Other)",
    }

    for key, regexp in mapping.items():
        mapped_values = np.where(values.str.contains(regexp), key, mapped_values)
    return mapped_values

def parse_anchor_year(anchor_year_group:pd.Series,date:pd.Series,anchor_year:pd.Series)->pd.Series:
    """Categorizes MIMIC-IV dates into their relative anchor year groups.

    Tested for MIMIC-IV 3.1.

    Args:
        anchor_year_group (pd.Series): Patients' anchor year group as reported in physionet-data.mimiciv_hosp.patients.
        date (pd.Series): Pseudonimized date to be anchored.
        anchor_year (pd.Series): Patients' anchor year as reported in physionet-data.mimiciv_hosp.patients.

    Returns:
        pd.Series: Categorized dates.
    """
    anchor_year_group=anchor_year_group.apply(lambda x: int(x.split("-")[0].strip(""))+1)
    delta=anchor_year_group+(date.dt.year-anchor_year)
    

    def anchor_delta(delta):
        delta_anchors=[(2008,2011),(2011,2014),(2014,2017),(2017,2020),(2020,2023)]
        for da in delta_anchors:
            if delta in range(*da):
                output=f"{da[0]} - {da[1]}"
        return output

    return delta.apply(anchor_delta)

def parse_careunit(values: pd.Series) -> pd.Series:
    """Parses MIMIC-IV Care Units in groups defined by Yarnell et al.

    Yarnell, Christopher J., Alistair Johnson, Tariq Dam, Annemijn Jonkman, Kuan Liu, Hannah Wunsch, Laurent Brochard, et al. 2023.
    “Do Thresholds for Invasive Ventilation in Hypoxemic Respiratory Failure Exist? A Cohort Study.”
    American Journal of Respiratory and Critical Care Medicine 207 (3): 271–82.

    Args:
        values (pd.Series): Input Series.

    Returns:
        pd.Series: Parsed Series.
    """
    mapped_values = np.empty(values.shape[0]) * np.nan
    mapping = {
        "Medical-Surgical": "(Medical Intensive Care Unit)|(Medical/Surgical Intensive Care Unit)|(Surgical Intensive Care Unit)",
        "Cardiac": "(Cardiac Vascular Intensive Care Unit)|(Coronary Care Unit)",
        "Neuro-Trauma": "(Neuro Intermediate)|(Neuro Stepdown)|(Neuro Surgical Intensive Care Unit)|(Trauma SICU)",
    }

    for key, regexp in mapping.items():
        mapped_values = np.where(values.str.contains(regexp), key, mapped_values)
    return mapped_values

def parse_time(values: pd.Series) -> pd.Series:
    """Parses MIMIC-IV patients'time of intervention according to Yarnell et al.

    Yarnell, Christopher J., Alistair Johnson, Tariq Dam, Annemijn Jonkman, Kuan Liu, Hannah Wunsch, Laurent Brochard, et al. 2023.
    “Do Thresholds for Invasive Ventilation in Hypoxemic Respiratory Failure Exist? A Cohort Study.”
    American Journal of Respiratory and Critical Care Medicine 207 (3): 271–82.

    Args:
        values (pd.Series): Input Series.

    Returns:
        pd.Series: Parsed Series.
    """
    mapped_values = np.empty(values.shape[0]) * np.nan
    mapping = {
        "00-06": (0, 6),
        "06-12": (6, 12),
        "12-18": (12, 18),
        "18-24": (18, 24),
    }

    for key, item in mapping.items():
        values = pd.to_datetime(values)
        mapped_values = np.where(values.dt.hour.between(*item), key, mapped_values)
    return mapped_values.astype(str)

def parse_bmi(values: pd.Series,impute_heights:bool=False) -> str:
    """BMI Classification.
    Source: Weir, Connor B., and Arif Jan. "BMI classification percentile and cut off points." (2019).
    Reasons of missing heights: https://github.com/MIT-LCP/mimic-code/issues/394#issuecomment-364529448

    Args:
        bmi_and_race (pd.Series): A series with at leastan index called bmi and one called race.

    Returns:
        str: BMI classification.
    """

    temp = values.copy()

    if impute_heights:
        temp.height=temp.height.fillna(temp.height.astype(float).mean())


    temp["bmi"] = temp.weight * ((temp.height.astype(float) / 100) ** -2)

    def __parse__(bmi_and_race):
        bmi = bmi_and_race.bmi
        ethnicity = bmi_and_race.race

        if bmi < 16.5:
            output = "Severly Underweight"
        elif bmi >= 16.5 and bmi < 18.5:
            output = "Underweight"
        elif bmi >= 18.5:
            if "asian" in ethnicity.lower():
                if bmi >= 18.5 and bmi < 23.0:
                    output = "Normal"
                elif bmi >= 23.0 and bmi < 25.0:
                    output = "Overweight"
                elif bmi >= 25.0:
                    output = "Obesity"
            else:
                if bmi >= 18.5 and bmi < 25.0:
                    output = "Normal"
                elif bmi >= 25.0 and bmi < 30.0:
                    output = "Overweight"
                elif bmi >= 30.0:
                    output = "Obesity"
        else:
            output = "Unknown or Unavailable"
        return output

    return temp.apply(__parse__, axis=1)