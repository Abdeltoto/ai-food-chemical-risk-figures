"""Coding of the 60 included documents (CRA steps and AI method families).

Steps: HI hazard identification, HC hazard characterization, EA exposure assessment,
RC risk characterization & prioritization.
"""

STEPS = ["HI", "HC", "EA", "RC"]
STEP_LABELS = {
    "HI": "Hazard\nidentification",
    "HC": "Hazard\ncharacterization",
    "EA": "Exposure\nassessment",
    "RC": "Risk characterization\n& prioritization",
}

FAMILIES = ["ML", "DL", "NLP", "KG", "BN", "QSAR", "EXP", "DB", "XAI"]
FAMILY_LABELS = {
    "ML": "Classical machine learning",
    "DL": "Deep learning",
    "NLP": "NLP, text mining & LLMs",
    "KG": "Knowledge graphs & ontologies",
    "BN": "Bayesian networks",
    "QSAR": "QSAR, read-across & in silico toxicology",
    "EXP": "High-throughput & probabilistic exposure models",
    "DB": "Curated toxicological databases",
    "XAI": "Explainability, trust & governance",
}

# code: (year, type, steps, families)
# type: P primary study, R review/survey, D database/resource, G governance/perspective/report
CODING = {
    "C01": (2020, "G", "HI HC EA RC", "NLP XAI"),
    "C02": (2018, "D", "HI EA", "KG"),
    "C03": (2023, "R", "HI", "ML DL"),
    "C04": (2024, "R", "HI EA", "ML DL"),
    "C05": (2026, "R", "HI", "ML DL"),
    "C06": (2025, "R", "HI RC", "ML DL BN NLP KG"),
    "C07": (2025, "P", "RC", "NLP DL ML XAI"),
    "C08": (2025, "R", "HI RC", "ML DL"),
    "C09": (2025, "G", "HI RC", "ML DL NLP XAI"),
    "C10": (2026, "R", "HI RC", "XAI DL"),
    "C11": (2026, "R", "HC EA RC", "ML DL QSAR"),
    "C12": (2024, "D", "HI HC", "DB"),
    "N01": (2024, "P", "HI HC", "NLP"),
    "N02": (2025, "G", "HI", "NLP"),
    "N03": (2024, "P", "HI HC", "NLP KG"),
    "N04": (2026, "P", "HC", "NLP"),
    "N05": (2026, "P", "HI HC", "NLP"),
    "N06": (2026, "G", "HC RC", "NLP XAI"),
    "N07": (2025, "R", "HI", "NLP ML"),
    "N08": (2024, "P", "HI", "NLP"),
    "N09": (2024, "P", "HI", "NLP"),
    "N10": (2021, "P", "HI", "ML NLP"),
    "N11": (2023, "P", "EA", "NLP ML"),
    "N12": (2026, "R", "HI", "KG NLP"),
    "N13": (2026, "P", "RC", "KG ML"),
    "N14": (2026, "R", "HI", "NLP"),
    "N15": (2020, "D", "HI HC", "DB"),
    "N16": (2017, "D", "HI HC EA", "DB QSAR EXP"),
    "N17": (2018, "P", "HI HC", "QSAR ML NLP"),
    "N18": (2018, "R", "HI HC", "QSAR ML NLP"),
    "N19": (2023, "R", "HC", "QSAR ML DL"),
    "N20": (2024, "P", "HC", "QSAR DL"),
    "N21": (2025, "P", "EA RC", "QSAR DL"),
    "N22": (2023, "G", "HI HC RC", "XAI NLP DL"),
    "N23": (2017, "P", "EA RC", "EXP"),
    "N24": (2018, "P", "EA RC", "EXP"),
    "N25": (2022, "P", "EA", "ML"),
    "N26": (2021, "P", "HI RC", "DL ML"),
    "N27": (2025, "P", "RC", "NLP DL ML XAI"),
    "N28": (2018, "P", "HI RC", "BN"),
    "N29": (2022, "P", "HI RC", "ML BN"),
    "N30": (2023, "P", "HI RC", "ML"),
    "N31": (2023, "P", "RC", "BN"),
    "N32": (2021, "D", "HC EA RC", "EXP QSAR DB"),
    "N33": (2025, "P", "EA RC", "ML XAI"),
    "N34": (2022, "P", "EA RC", "DL"),
    "N35": (2017, "P", "HC EA RC", "EXP"),
    "N36": (2022, "P", "EA", "ML"),
    "N37": (2022, "P", "EA", "ML BN"),
    "N38": (2025, "R", "HI EA", "ML DL"),
    "N39": (2021, "R", "HI EA", "ML BN DL"),
    "N40": (2022, "R", "HI RC", "ML NLP"),
    "N41": (2024, "R", "HI RC", "ML NLP KG"),
    "N42": (2024, "G", "HC RC", "XAI"),
    "N43": (2026, "G", "HI HC EA", "XAI NLP"),
    "N44": (2024, "G", "HI HC", "NLP KG"),
    "N45": (2026, "G", "HC RC", "XAI"),
    "N46": (2023, "R", "HI HC EA", "QSAR DL"),
    "N47": (2026, "R", "HI", "ML DL NLP"),
    "N48": (2026, "P", "EA", "DL XAI"),
}

TYPE_LABELS = {
    "P": "Primary study",
    "R": "Review or survey",
    "D": "Database or resource",
    "G": "Report, perspective or governance",
}
