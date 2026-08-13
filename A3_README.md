# A3 analysis series

The A3 notebooks replace the duplicated A2 analytical branches with one
prespecified path. At the start of every A3 01 run, the validated contents of
the MSSQL tables bones_mnitaxonrule and bones_mniweatheringrule are exported
to Taxa_lookup.xlsx and mniweatheringrule.xlsx. A3 01 then reads the modern
aerial workbook, OPC census 1998-17.xlsx, and bone-census-data.xlsx directly; it does not use
A2-generated pickles. Census workbooks are read-only. Derived tables are
written to data/processed/a3, and report-ready results to outputs/a3.

Run the notebooks from the repository root in this order:

1. notebooks/A3 01 Prepare comparable data.ipynb
2. notebooks/A3 02 Community fidelity and fence change.ipynb
3. notebooks/A3 03 Dominance and diversity through time.ipynb
4. notebooks/A3 04 Sensitivity analyses.ipynb
5. notebooks/A3 05 Historical ground census validation.ipynb
6. notebooks/A3 06 Estimated-year temporal fidelity.ipynb

The executed environment used Python 3.12.0. To reproduce it in a clean
environment, install requirements-a3.txt, register or select that Python
kernel, make the MSSQL environment settings available in
jupyter-env/.env, and execute the notebooks in the sequence above. The
standalone refresh command is:

    python scripts/export_mni_rules.py

Primary analytical rules:

- direct live–bone comparisons use the eligible matched wild-mammal taxa
  generated from the current inputs (15 in the present run);
- Sweetwaters aerial totals for 2000, 2002, and 2003 are historical Eastern
  aerial observations; they extend the Eastern pre-removal series but have no
  block-level detail;
- Sweetwaters ground and Earthwatch counts from 1996–2003 form a separate
  historical living series, confirmed blanks are zeros, and ground counts are
  never added to aerial counts;
- the ground series is compared separately with temporally corresponding
  Eastern bone MNI and with aerial composition in the shared years 2002–2003;
- estimated bone-MNI years are used in exact-year living–bone comparisons;
  a ±1-year bone window is reported only as a sensitivity analysis because
  adjacent windows can reuse the same MNI and are not independent samples;
- cattle, birds, carnivores, and unresolved categories are excluded from
  direct fidelity calculations;
- generic `Rhino` and `Zebra Hybrid` are explicitly excluded from direct
  matching; identified black rhinoceros remains eligible;
- unresolved categories remain in complete bone-only descriptions;
- the low-visibility 2024 collection is excluded from primary analyses and
  restored only as a sensitivity analysis;
- bone abundance is transect-level MNI by analytical category; standardized
  transects follow a 1-km route outward and back, and sufficiently separated
  transects are treated as spatially independent when MNI is summed;
- compositions are compared as relative abundances because aerial counts are
  much larger than summed bone MNI;
- annual bone diversity is interpreted only when one sector ×
  estimated-death-year sample has summed MNI of at least 10 across eligible
  matched taxa and contributing transects; this means represented individuals,
  not skeletal elements, taxa, transects, or aerial-census animals;
- pre-removal is through 2006 and post-removal begins in 2007 because the
  fence was removed in March, before the August bone walks and September
  aerial census;
- post-removal differences are associations with the fence transition, not
  causal estimates of fence removal.

The bone analysis time field is set by BONE_TIME_COLUMN near the start of A3
01. It currently uses Year. A future normalized weathering-derived field can
be selected there after it has been added to the Data sheet and checked to be
numeric. When another field is selected, the workbook Year is retained as
SourceYear in the processed data.

The exported weathering rules are an audit reference. A3 does not assign
normalized weathering stages: those reviewed decisions must already be
present in bone-census-data.xlsx before analysis.
