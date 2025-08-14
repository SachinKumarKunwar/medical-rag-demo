# Simple example drug interaction checker (synthetic)
# In a production system, integrate with RxNorm / DrugBank / Lexicomp via proper APIs and licenses.

INTERACTIONS = {
    ('lisinopril', 'spironolactone'): {
        'severity': 'high',
        'message': 'ACE inhibitor + potassium-sparing diuretic -> increased hyperkalemia risk. Monitor K+ and renal function.'
    },
    ('lisinopril', 'potassium_supplement'): {
        'severity': 'high',
        'message': 'ACE inhibitor + potassium supplement -> increased hyperkalemia risk. Avoid unless necessary and monitor K+.'
    },
    ('amlodipine', 'simvastatin'): {
        'severity': 'moderate',
        'message': 'CCB may increase simvastatin levels; consider alternative statin or dose adjustment.'
    }
}

def check_interactions(meds):
    meds = [m.strip().lower() for m in meds if m and m.strip()]
    warnings = []
    for i in range(len(meds)):
        for j in range(i+1, len(meds)):
            pair = (meds[i], meds[j])
            pair_rev = (meds[j], meds[i])
            info = INTERACTIONS.get(pair) or INTERACTIONS.get(pair_rev)
            if info:
                warnings.append({'pair': (meds[i], meds[j]), 'severity': info['severity'], 'message': info['message']})
    return warnings
