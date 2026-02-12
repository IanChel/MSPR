import pandas as pd
import numpy as np

# --- CONFIGURATION ---
DEPTS_NA = ['16', '17', '19', '23', '24', '33', '40', '47', '64', '79', '86', '87']

def clean_numeric(s):
    """Nettoie les chaînes avec % et virgules en float"""
    if pd.isna(s): return 0.0
    return float(str(s).replace(',', '.').replace('%', '').strip())

print("🚀 Initialisation du nettoyage : Nouvelle-Aquitaine")

# 1. NETTOYAGE DES ÉLECTIONS
df_raw = pd.read_csv('resultats-definitifs-par-bureau-de-vote.csv', sep=';', dtype={
    'Code département': str, 'Code commune': str, 'Code BV': str
})

# Filtre Régional
df_na = df_raw[df_raw['Code département'].isin(DEPTS_NA)].copy()
print(f"✅ {len(df_na)} bureaux détectés en Nouvelle-Aquitaine.")

# Calcul des blocs (RN, UG, ENS)
blocs = {
    'PCT_RN': ['RN', 'UXD'],
    'PCT_UG': ['UG', 'FI', 'SOC', 'VEC', 'COM'],
    'PCT_ENS': ['ENS', 'RE', 'MODM', 'HOR']
}

for label, nuances in blocs.items():
    scores = np.zeros(len(df_na))
    for i in range(1, 25): # Parcourt les colonnes candidats
        col_n = f'Nuance candidat {i}'
        col_p = f'% Voix/exprimés {i}'
        if col_n in df_na.columns:
            mask = df_na[col_n].isin(nuances)
            scores += df_na[col_p].apply(clean_numeric).values * mask
    df_na[label] = scores

# Clé unique pour la jointure spatiale
df_na['Code_BV_Complet'] = df_na['Code département'] + df_na['Code commune'] + df_na['Code BV']

# 2. EXPORT DU SOCLE PROPRE
cols_finales = ['Code_BV_Complet', 'Libellé commune', 'Exprimés', 'PCT_RN', 'PCT_UG', 'PCT_ENS']
df_na[cols_finales].to_csv('na_elections_clean.csv', index=False, sep=';', encoding='utf-8-sig')

print("✨ Fichier 'na_elections_clean.csv' prêt pour la phase IA.")