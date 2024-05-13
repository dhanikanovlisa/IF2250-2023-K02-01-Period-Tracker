"""
Default or built-in values used in the apps
"""

symptom_names = [
    "Blood Flow", "Intensitas Olahraga", "Kualitas Tidur", "Kram Perut", "Mood"]

symptom_rates = [0, 0, 0, 0, 0]

symptoms = [{"name": name, "rate": symptom_rates[i]}
            for i, name in enumerate(symptom_names)]

symptom_custom = {
    "name": "",
    "rate": 0,
    "desc": ""
}
