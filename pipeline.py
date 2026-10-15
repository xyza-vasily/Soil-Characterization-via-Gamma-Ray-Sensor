import pandas as pd
import numpy as np
from scipy import stats


def transfer(reference, new_site, texture, predictor):
    """Fit a line at the reference site, apply it to the new site, and score it.

    reference : table of the reference site (for example HOAL)
    new_site  : table of the new site (for example Raasdorf_2024)
    texture   : the column to predict, for example "Clay"
    predictor : the gamma-ray column to predict it from, for example "U238"

    Returns the predicted values and a dictionary of scores.
    """
    # 1. Fit the line at the reference site
    fit = stats.linregress(reference[predictor], reference[texture])

    # 2. Put the new site's gamma-ray values into that line (nothing is refitted)
    predicted = fit.intercept + fit.slope * new_site[predictor]

    # 3. Compare with the lab values
    observed = new_site[texture]
    error = predicted - observed

    scores = {
        "texture": texture,
        "predictor": predictor,
        "bias": error.mean(),
        "RMSE": np.sqrt((error ** 2).mean()),
        "baseline RMSE": np.sqrt(((reference[texture].mean() - observed) ** 2).mean()),
        "R2 transfer": 1 - (error ** 2).sum() / ((observed - observed.mean()) ** 2).sum(),
    }
    return predicted, scores


def load_data():
    """Load and prepare the three tables used in the analysis.

    Returns hoal, raasdorf_2024 and raasdorf_2026.
    """
    hoal = pd.read_csv("data/HOAL.csv")
    raasdorf_2024 = pd.read_csv("data/Raasdorf_2024.csv")
    raasdorf_2026 = pd.read_csv("data/Raasdorf_2026.csv")

    hoal = pd.read_csv("data/HOAL.csv")
    hoal = hoal.rename(columns={"Sand_2023": "Sand", "Clay_2023": "Clay", "Silt_2023": "Silt"})
    raasdorf_2024 = pd.read_csv("data/Raasdorf_2024.csv")
    raasdorf_2026 = pd.read_csv("data/Raasdorf_2026.csv")

    # Same names for the isotopes in all three tables
    raasdorf_2026 = raasdorf_2026.rename(
        columns={"40-K": "K40", "238-U": "U238", "232-Th": "Th232"}
    )

    # Drop survey rows where an isotope is zero (see the exploratory data analysis page)
    isotopes = ["K40", "U238", "Th232"]
    raasdorf_2026 = raasdorf_2026[(raasdorf_2026[isotopes] > 0).all(axis=1)].copy()

    # Ratio of U238 to Th232
    for table in [hoal, raasdorf_2024, raasdorf_2026]:
        table["Ratio"] = table["U238"] / table["Th232"]

    return hoal, raasdorf_2024, raasdorf_2026