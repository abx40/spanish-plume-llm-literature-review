"""Publisher groups for the 102 benchmark articles, from the benchmark's journal names.

A group names the platform a journal is published on. It says nothing about whether an
individual article is free to read. Historical Tellus and other small outlets are "Other".
"""

ORDER = ['Wiley', 'AMS', 'Elsevier', 'Copernicus', 'MDPI', 'Springer', 'Other']


def publisher_group(journal):
    j = journal.lower().strip()
    if j in {'weather and forecasting', 'monthly weather review',
             'journal of climate', 'journal of physical oceanography'}:
        return 'AMS'
    if j in {'natural hazards and earth system sciences', 'weather and climate dynamics',
             'weather and climate dynamics [discussions]'}:
        return 'Copernicus'
    if j in {'atmosphere', 'water'}:
        return 'MDPI'
    if (j == 'weather' or j.startswith('quarterly journal of the royal meteorological society')
            or j.startswith('meteorological applications')
            or j in {'international journal of climatology', 'journal of geophysical research: atmospheres',
                     'geophysical research letters', 'journal of flood risk management'}):
        return 'Wiley'
    if j in {'atmospheric research', 'global and planetary change'}:
        return 'Elsevier'
    if j in {'meteorology and atmospheric physics', 'natural hazards'}:
        return 'Springer'
    return 'Other'
