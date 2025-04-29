# MIMIC-IV utils
## A collection of low-level utilities to simplify processing of MIMIC-IV data.

### Installation
Run: `pip install "git+https://github.com/jhn-nt/mimic_utils.git"`

### Parsers
Collection of methods to categorize and parse various features commonly found in literature.
```python
from mimic_utils import parsers

df=load_mimic_dataset()

# Categorizes hospital admission locations
admissions_locations=parse_admission_location(df.admission_location)

# Renames MIMIC gender's label
gender=parse_gender(df.gender)

# Categorizes race & ethnicities 
race=parse_race(df.race)

# Categorizes available languages
language=parse_language(df.language)

# Categorizes available insurances
insurance=parse_insurance(df.insurance)

# Categorizes MIMIC-IV dates in anchor year groups
insurance=parse_anchor_year(df.anchor_year_group,df.dates,df.anchor_year)

# Categorizes available care units
careunit=parse_careunit(df.careunit)

# Categorizes daytime slots
daytime_slots=parse_time(df.daytime)

# Categorizes BMI according to the latest WHO classification
bmi=parse_time(df[["height","weight","race_and_ethnicity"]])

```

### References

1. [Johnson, Alistair, et al. "Mimic-iv." PhysioNet. Available online at: https://physionet. org/content/mimiciv/1.0/(accessed August 23, 2021) (2020).](https://physionet.org/content/mimiciv/2.1/)

2. [Yarnell, Christopher J., Alistair Johnson, Tariq Dam, Annemijn Jonkman, Kuan Liu, Hannah Wunsch, Laurent Brochard, et al. 2023. “Do Thresholds for Invasive Ventilation in Hypoxemic Respiratory Failure Exist? A Cohort Study.” American Journal of Respiratory and Critical Care Medicine 207 (3): 271–82.](https://pubmed.ncbi.nlm.nih.gov/36150166/)

3. [Weir, Connor B., and Arif Jan. "BMI classification percentile and cut off points." (2019).](https://pubmed.ncbi.nlm.nih.gov/31082114/)