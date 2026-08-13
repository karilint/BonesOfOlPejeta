---
title: "Living mammal communities and bone assemblages at Ol Pejeta Conservancy"
subtitle: "Plain-language Materials and Methods, Results, and Discussion based on the A3 analyses"
date: "11 August 2026"
---

# Scope and research questions

This document reports the current A3 analysis of living mammals and surface bone assemblages at Ol Pejeta Conservancy (OPC), Kenya. It addresses four questions:

1. Does the OPC bone assemblage reflect the living mammal community?
2. Does the bone assemblage capture changes in the living community following removal of the internal fence in March 2007?
3. How do long-term dominance patterns compare between the eastern and western sectors in the living and bone records?
4. How do richness, diversity, and evenness vary through time in the two records?

# Materials and Methods

## Study setting

OPC is a 328-km² wildlife conservancy in Laikipia County, central Kenya (approximately 0°N, 36°52′E). Its grassland, woodland, scrub woodland, and riverine habitats support a diverse large-mammal community. The Ewaso Ng’iro River runs broadly north–south between the former Sweetwaters Game Reserve in the east and the former Ol Pejeta Ranch in the west. An internal fence separating these sectors was removed in March 2007. The first living census after removal was conducted in September 2007, and bone fieldwork was conducted in August. We therefore classified observations through 2006 as pre-removal and observations from 2007 onward as post-removal.

## Living-community data

The primary living-community record consists of aerial census counts. Sector-level OPC data span 17 census years from 2005 to 2023 in each sector. Sweetwaters whole-area aerial totals from 2000, 2002, and 2003 were added as historical Eastern observations, producing 20 Eastern and 17 Western aerial years. The early totals have no block-level detail, so they support whole-Sweetwaters composition but not analysis within blocks. Counts were summed by taxon within sector and year. Aerial samples were large: 43,624 animals in the expanded Eastern dataset and 113,891 in the West across all recorded categories.

Sweetwaters ground and Earthwatch counts from 1996–1999 and 2001–2003 were prepared as a separate historical living series. Entries labelled `Earthwatch ?` were treated as valid, and confirmed blank cells were treated as zeros. Ground counts were never added to aerial counts. Instead, ground composition was compared separately with Eastern bone MNI and with aerial composition in the overlapping years 2002 and 2003.

The original aerial survey did not consistently cover birds or carnivores, so these groups were not used in direct living-versus-bone comparisons. Domestic cattle were also excluded. Survey effort information was not used to rescale the current aerial counts. If flight coverage or effort varied substantially, a future sensitivity analysis should standardize counts by surveyed area or flight effort before calculating composition.

## Bone-assemblage data and MNI

Bone abundance was measured as minimum number of individuals (MNI), not as the number of bones. MNI was calculated for each analytical taxonomic category within each transect. Every survey followed the same 1-km transect route: observers walked from a fixed starting point to a turning point 1 km away and returned along the same route. Each survey therefore involved 2 km of walking but covered one 1-km route in both directions. Transects were sufficiently far apart to treat their category-level MNI values as spatially independent. MNI values were summed across contributing transects within each sector and estimated death year.

Because route length and field protocol were standardized, no distance-based correction was applied. However, a sector-year containing more completed transects can have a larger summed MNI. This matters for absolute abundance and for analyses that pool observations, even though relative abundance within a sector-year is less directly affected by the common transect length.

Estimated death years were supplied in `bone-census-data.xlsx` after weathering stages had been grouped using the project’s reviewed weathering rules. The updated workbook contained 973 transect-level MNI records. The primary analysis excluded 54 records from the low-visibility 2024 collection and retained 919 records, producing 14 Eastern and 12 Western sector-year samples before taxonomic matching. The 15 matched taxa were represented in 14 Eastern and 11 Western sector-years, with summed MNI of 293 in the East and 224 in the West. The 2024 collection was restored only in a sensitivity analysis.

## Taxonomic matching

Taxon names were standardized using the current rules exported directly from the database table `bones_mnitaxonrule`. Weathering rules were exported from `bones_mniweatheringrule` as an audit reference. Direct living-versus-bone comparisons included the 15 wild-mammal taxa identifiable in both datasets: impala, hartebeest, black rhinoceros, plains zebra, Thomson’s gazelle, giraffe, waterbuck, African elephant, Grant’s gazelle, beisa oryx, warthog, bohor reedbuck, buffalo, common eland, and bushbuck.

Cattle, birds, carnivores, and unresolved categories were excluded from direct taxon-matched comparisons. In particular, the historical labels `Rhino` and `Zebra Hybrid` were excluded because generic rhino cannot be matched confidently to a species and hybrid zebra is not equivalent to the plains-zebra category. Identified black rhinoceros (*Diceros bicornis*) remained eligible. The 919-record primary dataset contained 415 excluded MNI: unidentified mammal 249, medium bovid 79, large bovid 26, small bovid 20, cattle 12, small bird 7, ostrich 5, unresolved ungulate 5, medium bird 4, hare 2, spotted hyena 2, and one each of vervet monkey, tree hyrax, unresolved rhinoceros, and lion. These categories were retained in separate bone-only descriptive summaries because they still contain information about the bone assemblage. They were not assigned to species without supporting identification evidence.

## Python software and biostatistical functions

The analyses were executed with Python 3.12.0. pandas 3.0.3 was used for Excel input, filtering, grouping, pivot tables, joins, and CSV/pickle output; NumPy 2.4.6 supported numerical arrays, proportions, and transformations; and openpyxl 3.1.5 provided Excel workbook access. SciPy 1.18.0 supplied `scipy.spatial.distance.braycurtis` for compositional dissimilarity and `scipy.stats.pearsonr`, `spearmanr`, and `linregress` for correlation, rank correlation, fitted lines, and associated p-values. The Student-t distribution function `scipy.stats.t.ppf` was used for confidence bands around mean fitted relationships. scikit-bio 0.7.3 supplied `skbio.diversity.alpha.shannon` and `simpson`; Hill N1 was calculated as the exponential of Shannon entropy and Hill N2 as the reciprocal of Simpson dominance. Matplotlib 3.11.1 generated the figures. No PERMANOVA or PERMDISP result was used in the A3 report because Western pre-removal replication was insufficient for a common sector-wise inferential design.

## Relative abundance and overall fidelity

Raw aerial counts and bone MNI are not directly comparable: aerial totals are much larger, and the two methods observe animals in different ways. We therefore expressed each taxon as a proportion of the relevant dataset total. For example, 400 aerially counted zebra among 1,000 animals and zebra MNI of 8 within total bone MNI of 20 both represent 40%, although their abundance units are different.

Overall correspondence was summarized with three complementary measures. Bray–Curtis dissimilarity ranges from 0 for identical composition to 1 for no shared proportional structure. Pearson correlation asks whether taxa abundant in the living census also tend to have high bone MNI proportions. Spearman correlation asks whether the ordering of taxa from common to rare is similar. Pearson and Spearman correlations do not measure exact agreement, so Bray–Curtis and the 1:1 line in the figures remain important.

For the overall comparison, counts or MNI were pooled across all primary observations within each dataset and then converted to relative abundance. Sector-specific comparisons were calculated in the same way. Taxa contributing most to the overall mismatch were described by their absolute differences in relative abundance. This is a transparent arithmetic decomposition of Bray–Curtis dissimilarity, not a locally coded SIMPER significance test.

## Change following fence removal

Within each sector and dataset, taxon counts or MNI were pooled separately for the pre-removal period (through 2006) and post-removal period (2007 onward), and each period was converted to relative abundance. Community turnover between periods was described with Bray–Curtis dissimilarity. For each taxon, change was calculated as post-removal minus pre-removal relative abundance. Pearson and Spearman correlations then compared the living and bone change vectors.

Five Eastern aerial years (2000, 2002, 2003, 2005, and 2006) and two Western years (2005 and 2006) were available before removal, compared with 15 afterward in each sector. PERMANOVA was not used as a common primary period test because the West has only two independent pre-removal years. Applying an inferential period test only in the East would make the sector analyses inconsistent, so both sectors were summarized using the same descriptive effect sizes. Blocks were not analytical replicates in any A3 analysis and played no role in this decision. The results describe associations with the pre/post boundary rather than a causal effect of fence removal.

## Dominance and diversity

Long-term dominance was described using each taxon’s mean annual relative abundance, median annual rank when present, and occupancy (the proportion of sampled years in which it occurred). Diversity was summarized with taxon richness and Hill numbers. Richness is simply the number of represented taxa. Hill N1 is the effective number of common taxa, while Hill N2 gives more emphasis to the most abundant taxa. Hill evenness compares Hill N1 with richness and approaches 1 when represented taxa have similar abundances.

Annual bone diversity was interpreted only when summed MNI across eligible matched taxa and contributing transects was at least 10 within one sector × estimated-death-year sample. This threshold does **not** mean 10 skeletal elements, 10 taxa, 10 transects, or 10 aerially counted animals. It is a pragmatic minimum intended to avoid giving strong meaning to percentages and diversity values based on very few represented individuals. Samples below 10 remain in the audit data but are flagged as too small for annual diversity interpretation.

## Sensitivity and reproducibility checks

Checks assessed inclusion of the 2024 bone collection, exclusion of taxa occurring in fewer than 20% of bone sector-years, annual bone-diversity thresholds of summed MNI 5, 10, and 15, and exclusion of the three Earthwatch-labelled ground years. Same-year ground–aerial agreement was described for 2002 and 2003; two pairs are insufficient for a formal method-equivalence test. The source census workbooks were read only. Derived data were written to `data/processed/a3`, and report-ready tables and figures to `outputs/a3`.

## Estimated-year temporal comparisons

Estimated death year is the only available temporal assignment for bone MNI, so it was used directly in supplementary annual comparisons. For each living census year and sector, we compared living relative abundance with bone-MNI relative abundance assigned to the same estimated year. We calculated Bray–Curtis dissimilarity, Pearson correlation, and Spearman rank correlation across the eligible matched taxa. The summed matched-taxon bone MNI for each comparison was reported, and MNI ≥10 was used as a descriptive adequacy flag, as in the diversity analysis.

We repeated the calculation after pooling bone MNI assigned to one year before, the living census year, or one year after (a ±1-year window). This window asks whether small uncertainty in the weathering-derived assignment changes the result. It is a sensitivity analysis rather than a new set of independent samples because neighbouring living years can use some of the same bone MNI. Exact-year comparisons are therefore the main annual description, while pooled historical and pre/post-period comparisons remain the most stable summaries.

# Results

## Sample coverage

The matched aerial record contained 20 Eastern and 17 Western sampled years, with very large annual counts. Weathering-based grouping and taxonomic matching produced fewer bone sector-years and much smaller samples (Table 1). Median summed matched-taxon MNI was 18 in the East and 16 in the West. Three of 14 Eastern and five of 11 Western matched bone sector-years had MNI below 10. Thus, the bone data support broad pooled comparisons better than fine-grained annual inference, especially in the West.

**Table 1. Sampling coverage in the primary matched-taxon datasets. “Below 10” applies only to summed matched-taxon MNI in a bone sector-year.**

| Dataset | Sector | Sector-years | Total count or MNI | Median per sector-year | Range | Bone years below MNI 10 |
|---|---:|---:|---:|---:|---:|---:|
| Aerial census | Eastern | 20 | 42,708 animals | 2,047.5 | 935–3,965 | Not applicable |
| Aerial census | Western | 17 | 113,086 animals | 6,507 | 4,556–9,820 | Not applicable |
| Bone assemblage | Eastern | 14 | MNI 293 | MNI 18 | MNI 2–54 | 3 |
| Bone assemblage | Western | 11 | MNI 224 | MNI 16 | MNI 1–57 | 5 |

## Does the bone assemblage reflect the living community?

Across OPC, the bone assemblage showed a moderately close match to the living community (Bray–Curtis = 0.358; Table 2). Pearson correlation was positive (r = 0.789, p < 0.001), and taxonomic rank correlation was also positive (Spearman rho = 0.763). Taxa common in the living census therefore generally tended to be common in the bone assemblage, but their proportions were not identical.

The correspondence was stronger in the West (Pearson r = 0.821; Bray–Curtis = 0.378) than in the expanded East series (r = 0.631; Bray–Curtis = 0.390). Eastern bone composition was still closer to Western living composition (Bray–Curtis = 0.301) than to Eastern living composition. Because the bone record is time-averaged, this cross-sector comparison is not direct evidence of animal movement.

**Table 2. Correspondence between living relative abundance and bone-MNI relative abundance across 15 matched taxa. Lower Bray–Curtis values indicate closer composition; higher positive correlations indicate stronger association.**

| Comparison | Bray–Curtis | Pearson r | Spearman rho |
|---|---:|---:|---:|
| OPC overall | 0.358 | 0.789 | 0.763 |
| Eastern bones vs Eastern living | 0.390 | 0.631 | 0.828 |
| Western bones vs Western living | 0.378 | 0.821 | 0.668 |
| Eastern bones vs Western living | 0.301 | 0.834 | 0.716 |
| Western bones vs Eastern living | 0.466 | 0.576 | 0.745 |

**Figure 1. Overall living–bone fidelity.**

![Correlation between living-population and bone-assemblage relative abundances for 15 matched wild-mammal taxa at OPC. Pearson r = 0.789, p < 0.001. The solid red line is the least-squares fit, the dashed line is exact 1:1 agreement, and shading is the 95% confidence interval for the mean fitted relationship. Totals cover aerial census years 2000–2023 and estimated bone death years 1978–2014; n(live) = 155,794 matched aerial counts and n(dead) = summed matched-taxon MNI 517. Orange points mark the five largest absolute residuals as descriptive highlights, not formally tested outliers. Taxon codes: AM, impala; AB, hartebeest; DB, black rhinoceros; EB, plains zebra; ET, Thomson’s gazelle; GC, giraffe; KE, waterbuck; LA, African elephant; NG, Grant’s gazelle; OB, beisa oryx; PA, warthog; RR, bohor reedbuck; SC, buffalo; TO, common eland; TS, bushbuck.](../outputs/a3/A3_02_overall_fidelity_scatter.png){width=85%}

Five taxa accounted for most of the overall difference (Table 3). Plains zebra made up 47.8% of matched bone MNI but 32.1% of living counts. Warthog and giraffe were also proportionally more common in the bone record. Impala made up 22.0% of living counts but only 6.0% of bone MNI, while buffalo made up 17.5% and 7.7%, respectively. These differences do not by themselves identify causes.

**Table 3. Taxa contributing most to overall living–bone compositional difference. Percentages are within-dataset relative abundances.**

| Taxon | Living (%) | Bone MNI (%) | Contribution to Bray–Curtis (%) | Direction |
|---|---:|---:|---:|---|
| Impala (*Aepyceros melampus*) | 22.0 | 6.0 | 22.3 | Higher in living record |
| Plains zebra (*Equus burchellii*) | 32.1 | 47.8 | 21.9 | Higher in bone record |
| Buffalo (*Syncerus caffer*) | 17.5 | 7.7 | 13.6 | Higher in living record |
| Warthog (*Phacochoerus africanus*) | 2.7 | 10.3 | 10.5 | Higher in bone record |
| Giraffe (*Giraffa camelopardalis*) | 2.2 | 7.5 | 7.5 | Higher in bone record |
| Thomson’s gazelle (*Eudorcas thomsonii*) | 9.3 | 4.6 | 6.5 | Higher in living record |
| Waterbuck (*Kobus ellipsiprymnus*) | 1.3 | 4.8 | 5.0 | Higher in bone record |
| Grant’s gazelle (*Nanger granti*) | 6.1 | 2.9 | 4.4 | Higher in living record |

## Did the bone assemblage capture change after fence removal?

The living community changed more between the pre- and post-removal periods in the West (Bray–Curtis = 0.334) than in the East (0.239; Table 4). Bone Bray–Curtis was 0.283 in the East and 0.233 in the West. Similar amounts of turnover do not necessarily mean that the same taxa changed in the same directions.

Taxon-by-taxon change correspondence was moderately strong in the expanded East series (Pearson r = 0.670, p = 0.006; Spearman rho = 0.757) but negative in the West (r = −0.271, p = 0.329). The additional Eastern pre-removal years therefore materially strengthened evidence that the bones tracked period change in that sector. In the West, plains zebra illustrates the mismatch: its living relative abundance declined by 26.9 percentage points, whereas its bone-MNI share increased by 8.4 points. These associations are not formal estimates of the fence’s causal effect.

**Table 4. Pre/post-removal turnover and correspondence of taxon changes.**

| Sector | Living years pre/post | Living Bray–Curtis | Bone Bray–Curtis | Change Pearson r (p) | Change Spearman rho |
|---|---:|---:|---:|---:|---:|
| Eastern | 5 / 15 | 0.239 | 0.283 | 0.670 (0.006) | 0.757 |
| Western | 2 / 15 | 0.334 | 0.233 | −0.271 (0.329) | −0.059 |

**Figure 2. Correspondence of living and bone compositional changes across the 2007 boundary.**

![Correspondence between pre/post-removal changes in living and bone relative abundance for 15 matched taxa. Change is post-removal (2007+) minus pre-removal (through 2006). The fitted lines are descriptive; dashed lines show 1:1 agreement and horizontal and vertical lines mark zero change. Eastern: r = 0.670, p = 0.006. Western: r = −0.271, p = 0.329. Taxon codes are defined in Figure 1.](../outputs/a3/A3_02_change_correspondence_scatter.png){width=95%}

## Dominance, richness, diversity, and evenness

The expanded Eastern living series was led by plains zebra (mean annual relative abundance 23.8%), impala (22.9%), and buffalo (21.4%). Plains zebra was the leading Western living taxon (36.5%), followed by impala (21.1%) and buffalo (15.5%). Bone MNI was more strongly zebra-dominated in both sectors: plains zebra averaged 43.4% in the East and 45.0% in the West. Warthog was second in both bone series (13.3% and 14.9%).

All 20 Eastern and 17 Western living years were suitable for annual description. Eastern richness ranged from 10 to 15 matched taxa and Hill N1 from 5.188 to 7.893; Western richness ranged from 11 to 14 and Hill N1 from 3.758 to 6.755 (Table 5). Applying the primary summed-MNI threshold retained 11 of 14 Eastern bone years but only 6 of 11 Western bone years represented in the annual diversity matrix. Observed bone Hill N1 ranged from 2.401 to 6.918 in the East and from 3.179 to 6.940 in the West. These ranges do not demonstrate a directional time trend.

**Table 5. Annual diversity ranges for samples retained under the primary rules. Bone rows require summed matched-taxon MNI ≥10 per sector-year.**

| Dataset | Sector | Years interpreted | Median count or MNI | Richness range | Hill N1 range | Hill evenness range |
|---|---|---:|---:|---:|---:|---:|
| Living | Eastern | 20 | 2,047.5 animals | 10–15 | 5.188–7.893 | 0.412–0.616 |
| Living | Western | 17 | 6,507 animals | 11–14 | 3.758–6.755 | 0.342–0.550 |
| Bones | Eastern | 11 | MNI 23 | 3–11 | 2.401–6.918 | 0.537–0.939 |
| Bones | Western | 6 | MNI 33.5 | 6–10 | 3.179–6.940 | 0.477–0.694 |

Bone-only summaries that retained unresolved wild-mammal categories but excluded cattle and birds produced Hill N1 ranges of 3.804–9.638 across 12 Eastern years and 4.353–9.070 across seven Western years. These summaries characterize the bones themselves, but they cannot be compared taxon-for-taxon with the aerial record until unresolved categories are assigned reliably.

## Sensitivity and data-availability results

The main overall result was stable when the low-visibility 2024 collection was included: overall Bray–Curtis changed from 0.358 to 0.349 and Pearson r from 0.789 to 0.798 (Table 6). Applying the older 20% occurrence rule retained 10 of 15 taxa and changed Bray–Curtis to 0.351, although Spearman rho declined to 0.539. The full eligible set remained primary.

Changing the annual bone threshold from MNI 10 to 5 added only one Eastern and one Western year; a threshold of 15 retained seven Eastern and six Western years. Lowering the primary threshold to 7, 8, or 9 would not recover additional sector-years beyond those already discussed in the A3 feasibility audit. The MNI ≥10 rule remains a transparent quality flag rather than a formal biological boundary.

**Table 6. Sensitivity of the main conclusions to analytical choices.**

| Check | Data retained | Bray–Curtis | Pearson r | Spearman rho | Interpretation |
|---|---:|---:|---:|---:|---|
| Primary: exclude 2024 | 15 taxa | 0.358 | 0.789 | 0.763 | Main result |
| Include 2024 | 15 taxa | 0.349 | 0.798 | 0.763 | Very similar |
| Apply 20% occurrence filter | 10 taxa | 0.351 | 0.749 | 0.539 | Magnitude stable; ranks more sensitive |

Twelve sector-years occurred in both the aerial and bone series (Table 7). Six of seven shared Eastern years and two of five shared Western years reached matched-taxon MNI 10. No overlapping Western pre-removal year reached the threshold. We therefore did not use the annual pairs for an inferential pre/post or trend test; their year-specific descriptive fidelity is reported below.

**Table 7. Sector-years present in both records. Bone adequacy means summed matched-taxon MNI ≥10.**

| Sector | Year | Period | Living count | Living taxa | Bone MNI | Bone taxa | Adequate bone MNI? |
|---|---:|---|---:|---:|---:|---:|---|
| Eastern | 2002 | Pre-removal | 935 | 11 | 23 | 5 | Yes |
| Eastern | 2003 | Pre-removal | 979 | 10 | 10 | 5 | Yes |
| Eastern | 2006 | Pre-removal | 1,671 | 14 | 13 | 6 | Yes |
| Eastern | 2008 | Post-removal | 3,965 | 14 | 11 | 3 | Yes |
| Eastern | 2010 | Post-removal | 2,417 | 13 | 5 | 3 | No |
| Eastern | 2013 | Post-removal | 2,669 | 14 | 22 | 7 | Yes |
| Eastern | 2014 | Post-removal | 3,506 | 14 | 23 | 6 | Yes |
| Western | 2006 | Pre-removal | 4,556 | 11 | 4 | 3 | No |
| Western | 2008 | Post-removal | 5,944 | 11 | 4 | 3 | No |
| Western | 2010 | Post-removal | 6,625 | 12 | 1 | 1 | No |
| Western | 2013 | Post-removal | 7,711 | 14 | 21 | 7 | Yes |
| Western | 2014 | Post-removal | 6,414 | 12 | 39 | 6 | Yes |

## Independent historical ground-census analysis

Across 14 taxa shared by the ground census and Eastern bones, pooled 1996–2003 ground composition corresponded strongly with Eastern bone MNI assigned to the same estimated-year window (Bray–Curtis = 0.242; Pearson r = 0.919, p < 0.001; Spearman rho = 0.732; ground count = 22,028; bone MNI = 58). Using all Eastern primary bone years strengthened the descriptive match (Bray–Curtis = 0.167; r = 0.953; rho = 0.857). Plains zebra contributed 37.4% of the matched-window difference, buffalo 21.4%, and impala 11.9%.

Ground and aerial compositions agreed moderately in 2002 (Bray–Curtis = 0.421; r = 0.549; rho = 0.461) and strongly in 2003 (Bray–Curtis = 0.237; r = 0.870; rho = 0.897). Pooling the two years gave Bray–Curtis = 0.270, r = 0.884, and rho = 0.795. The methods therefore captured broadly similar dominance but were not interchangeable year by year.

Excluding the three Earthwatch-labelled years changed pooled ground composition only modestly (Bray–Curtis = 0.105; r = 0.980; rho = 0.960), supporting their inclusion. Exact ground-year and estimated bone-year overlap occurred in 1998, 2002, and 2003, with bone MNI 25, 23, and 10. Estimated death year is the only temporal assignment available for these MNI values and was therefore used in the annual analysis below; its uncertainty is the reason for also reporting pooled and ±1-year sensitivity comparisons.

**Figure 3. Independent historical ground–bone and ground–aerial comparisons.**

![Historical method comparisons in Sweetwaters/Eastern OPC. Left: pooled 1996–2003 ground relative abundance versus Eastern bone MNI assigned to estimated years 1996–2003 (14 taxa; r = 0.919, p < 0.001). Right: pooled ground versus aerial relative abundance in shared years 2002–2003 (14 taxa; r = 0.884, p < 0.001). Solid red lines are least-squares fits, dashed lines show 1:1 agreement, and orange points are descriptive residual highlights.](../outputs/a3/A3_05_historical_method_comparisons.png){width=95%}

## Fidelity at estimated bone-MNI years

Exact-year aerial–bone overlap occurred in seven Eastern and five Western years (Table 8). Six Eastern comparisons reached matched-taxon bone MNI ≥10, but only two Western comparisons did. Among the adequate Eastern exact-year comparisons, Bray–Curtis ranged from 0.299 to 0.676 and Pearson r from 0.231 to 0.864. The two adequate Western comparisons, 2013 and 2014, had Bray–Curtis values of 0.376 and 0.411 and Pearson r values of 0.821 and 0.834. Correspondence therefore varied substantially through time, and the Western annual evidence remains concentrated in two recent years.

The three exact-year ground–bone comparisons all reached MNI ≥10. For 1998, 2002, and 2003, respectively, Bray–Curtis was 0.278, 0.399, and 0.362 and Pearson r was 0.901, 0.784, and 0.854. These results show a recognizable living-community signal in estimated-year bone composition, but they do not imply exact agreement.

**Table 8. Coverage and median fidelity at estimated bone-MNI years. “Adequate” means summed matched-taxon bone MNI ≥10. Medians include all available comparisons and should be read with the adequate counts.**

| Living method and sector | Bone window | Available comparisons | Adequate comparisons | Median bone MNI | Median Bray–Curtis | Median Pearson r | Median Spearman rho |
|---|---:|---:|---:|---:|---:|---:|---:|
| Aerial, Eastern | Exact year | 7 | 6 | 13.0 | 0.451 | 0.562 | 0.473 |
| Aerial, Eastern | ±1 year | 12 | 11 | 22.5 | 0.453 | 0.616 | 0.621 |
| Aerial, Western | Exact year | 5 | 2 | 4.0 | 0.411 | 0.821 | 0.527 |
| Aerial, Western | ±1 year | 10 | 4 | 6.5 | 0.373 | 0.828 | 0.577 |
| Ground, Eastern | Exact year | 3 | 3 | 23.0 | 0.362 | 0.854 | 0.617 |
| Ground, Eastern | ±1 year | 6 | 6 | 25.0 | 0.323 | 0.853 | 0.674 |

The ±1-year bone window increased adequate coverage to 11 Eastern aerial, four Western aerial, and six Eastern ground comparisons. It did not consistently improve the similarity values for the exact-year pairs. Because adjacent windows overlap and can reuse the same MNI, these additional points are descriptive sensitivity results rather than independent annual replicates.

The Figure 4 calculations include only the 15 prespecified matched taxa. The primary bone dataset also contained 415 excluded MNI: unidentified mammal 249, medium bovid 79, large bovid 26, small bovid 20, cattle 12, small bird 7, ostrich 5, unresolved ungulate 5, medium bird 4, hare 2, spotted hyena 2, and one each of vervet monkey, tree hyrax, unresolved rhinoceros, and lion. They remain in the bone-only summaries but were not assigned to matched species without identification evidence.

**Figure 4. Living–bone fidelity at estimated bone-MNI years.**

![Bray–Curtis dissimilarity between living relative abundance and bone-MNI relative abundance at estimated bone years. Panels show Eastern aerial, Western aerial, and Eastern ground comparisons. Exact-year results are shown beside ±1-year bone-window sensitivity results. The y-axis is reversed so that lower dissimilarity (greater similarity) plots higher; labels give summed matched-taxon bone MNI, and filled points meet MNI ≥10.](../outputs/a3/A3_06_estimated_year_fidelity.png){width=95%}

# Discussion

## Main interpretation

The OPC bone assemblage contains a clear but filtered signal of the living mammal community. The positive overall correlations and moderate Bray–Curtis dissimilarity show that broadly abundant living taxa tend to be well represented in the bones. Plains zebra was a leading taxon in both records and the strongest bone dominant in both sectors. The bone assemblage should therefore be useful for reconstructing broad community structure and long-term dominance.

The match is not exact. Impala and buffalo were underrepresented in bone MNI relative to the living census, whereas plains zebra, warthog, and giraffe were overrepresented. Several mechanisms could create these differences: variation among taxa in mortality, carcass production, bone survival, scavenger activity, transport, visibility, identification, and recovery. Time averaging can also combine animals that died across many years, whereas an aerial census is a relatively short snapshot. The analysis cannot distinguish these mechanisms, so taxon departures should be treated as hypotheses for further taphonomic and ecological work rather than as direct measures of mortality.

## Fence-removal question

The living census suggests a larger compositional change across the 2007 boundary in the Western sector than in the East. This is consistent with the idea that removal of the internal fence was followed by substantial reorganization in the former ranch sector. However, the analysis does not isolate fence removal from rainfall, habitat change, management, population growth or decline, or other events that occurred at the same time.

The expanded Eastern aerial series changed the earlier interpretation: Eastern bone and living change vectors were moderately strongly aligned. Western alignment remained unsupported and negative. Weathering-based estimated years, time averaging, and modest MNI still make the bones better suited to broad period-level comparisons than precise year-by-year tracking.

Using estimated MNI year nevertheless adds information that would be lost by relying only on pooled comparisons. Exact-year results show that fidelity is not constant: some Eastern years matched the living composition closely, whereas 2008 was notably dissimilar, and adequate Western evidence was limited to 2013–2014. The ground comparisons provide an independent historical check for three Eastern years. The ±1-year analysis improves coverage but cannot solve low Western MNI and must not be interpreted as extra independent replication because windows overlap.

Pre-removal coverage remains spatially uneven: the East now has five aerial years, but the West still has only two. The independent ground series strongly corroborates the Eastern ground–bone relationship, while the 2002–2003 calibration shows that ground and aerial methods can differ in individual years. Ground data therefore strengthen historical inference without being merged into aerial counts.

## Sampling effort and the meaning of MNI

The standardized 1-km out-and-back routes make transect distance comparable, and the spatial separation of transects supports summing transect-level MNI. Nevertheless, summed MNI can increase when more transects contribute to a sector-year. Relative abundance removes differences in total sample magnitude, but it does not automatically correct uneven numbers of transects or differences in detection among taxa. A useful future sensitivity analysis would compare pooled results with results that first calculate composition for each transect or sector-year and then give those units equal weight.

MNI must also be kept conceptually separate from skeletal-element abundance. An MNI of 10 means that the observed remains require at least ten individuals across the included matched categories; it does not mean that ten bones were found. Consistent use of MNI terminology is important for reproducible reporting.

## Diversity and unresolved taxa

Living diversity could be described in every sampled year, but annual bone diversity was constrained by small samples, particularly in the West. The MNI ≥10 rule prevents the smallest samples from being discussed as though they were equally precise. It is not a guarantee of accuracy, and annual bone diversity remains descriptive because estimated years are unevenly represented and derived from weathering groups.

Excluding unresolved bovids from direct taxon matching avoids pretending that a broad category is equivalent to a species. Retaining these records in bone-only summaries preserves valid information. Future assignment of small, medium, and large bovid categories may increase matched MNI and taxonomic coverage, but assignments should be made before analysis using explicit identification rules. Buffalo can be handled separately where identification is sufficiently reliable.

## Conclusions

The present evidence supports a cautious answer to the main research questions. First, the OPC bone assemblage broadly reflects living-community composition and dominance, but not exact proportional abundance; the separate ground census supports this conclusion for historical Sweetwaters. Second, living composition changed more strongly in the West across the 2007 boundary, while taxon-specific bone change tracked the expanded Eastern series but not the Western series. Third, plains zebra dominated the bone record in both sectors, whereas living dominance was shared more among zebra, impala, and buffalo. Fourth, both records show variation in richness and diversity, but annual bone patterns are limited by MNI and temporal coverage.

The strongest use of these data is therefore a long-term, time-averaged comparison of community composition, supported by transparent sensitivity analyses. Precise causal claims about fence removal and fine annual trends should await additional pre-removal living data, improved temporal resolution, or more bone MNI in underrepresented sector-years.

# References cited in the methods

Behrensmeyer, A. K. (1978). Taphonomic and ecologic information from bone weathering. *Paleobiology*, 4, 150–162.

Bray, J. R., & Curtis, J. T. (1957). An ordination of the upland forest communities of southern Wisconsin. *Ecological Monographs*, 27, 325–349.

Hill, M. O. (1973). Diversity and evenness: a unifying notation and its consequences. *Ecology*, 54, 427–432.

Jost, L. (2006). Entropy and diversity. *Oikos*, 113, 363–375.

Patton, F., Mulama, M. S., Mutisya, S., & Campbell, P. E. (2010). The effect of removing a dividing fence between two populations of black rhinos. *Pachyderm*, 47, 55–58.

# Data provenance note

Numerical results and figures in this draft were taken from the executed A3 notebooks and the files in `outputs/a3` on 11 August 2026. The document should be regenerated after any change to `bone-census-data.xlsx`, taxonomic rules, weathering assignments, or census inputs.

# Supplementary material: catalogue of generated A3 output files

The following files were present in `outputs/a3` when this document was generated. CSV files are analysis-ready or copy-ready tables; PNG files are high-resolution raster figures; PDF files are vector versions suitable for publication layout. The catalogue records available supplementary products but does not imply that every file must be included in a paper.

## Input files

| File | Role in the A3 analyses |
|---|---|
| `data/import/excel/Aerial_Census_Data_BPedited_foranalysis.xlsx` | Primary modern aerial-census source. A3 reads the 2005–2010, 2012–2017, and 2019–2023 year sheets and retains Ol Pejeta Eastern and Western records. |
| `data/import/excel/OPC census 1998-17.xlsx` | Historical Sweetwaters source. A3 reads the `OPC ground and aerial` sheet for aerial totals in 2000, 2002, and 2003 and the separate ground/Earthwatch series for 1996–1999 and 2001–2003. |
| `data/import/excel/bone-census-data.xlsx` | Transect-level bone-MNI source. A3 reads the `Data` sheet, uses `Year` as the estimated death-year field, and identifies the low-visibility 2024 collection from `Date`. |
| `data/import/excel/Taxa_lookup.xlsx` | Taxonomic alias and canonical-name rules exported at the start of A3 01 from the validated MSSQL `bones_mnitaxonrule` table; used to standardize source names and define eligible matches. |
| `data/import/excel/mniweatheringrule.xlsx` | Weathering-rule audit workbook exported at the start of A3 01 from the validated MSSQL `bones_mniweatheringrule` table. Reviewed year assignments are already present in the bone source workbook; A3 does not reassign weathering stages. |

## A3 01 — Data preparation

| File | Short description |
|---|---|
| `A3_01_excluded_bone_taxa.csv` | Bone taxa omitted from direct matched analyses, with primary-dataset record and excluded-MNI counts. |

## A3 02 — Community fidelity and fence-period change

| File | Short description |
|---|---|
| `A3_02_aerial_period_summary.csv` | Pre/post aerial-year counts and Bray–Curtis turnover by sector. |
| `A3_02_aerial_period_taxon_changes.csv` | Post-minus-pre aerial relative-abundance change for every matched taxon and sector. |
| `A3_02_change_correspondence_scatter.pdf` | Vector version of the Eastern/Western change-correspondence figure. |
| `A3_02_change_correspondence_scatter.png` | High-resolution raster version of the change-correspondence figure. |
| `A3_02_change_tracking_results.csv` | Living-versus-bone change correlations and pre/post turnover by sector. |
| `A3_02_fidelity_results.csv` | Overall, within-sector, and cross-sector living–bone fidelity statistics. |
| `A3_02_overall_fidelity_scatter.pdf` | Vector version of the overall living–bone fidelity figure. |
| `A3_02_overall_fidelity_scatter.png` | High-resolution raster version of the overall fidelity figure. |
| `A3_02_sampling_adequacy.csv` | Numbers of years, totals, medians, ranges, and small bone samples by dataset and sector. |
| `A3_02_scatter_figure_statistics.csv` | Regression equations, correlations, p-values, sample sizes, and highlighted taxa used in A3 02 figures. |
| `A3_02_taxon_change_vectors.csv` | Living and bone pre/post change values for each matched taxon and sector. |
| `A3_02_taxon_contributions.csv` | Taxon-specific contributions to overall Bray–Curtis living–bone difference. |

## A3 03 — Dominance and diversity

| File | Short description |
|---|---|
| `A3_03_complete_bone_diversity.csv` | Annual bone-only diversity retaining eligible unresolved wild-mammal categories. |
| `A3_03_diversity_summary.csv` | Sector-level ranges and medians for interpretable living and matched-bone diversity. |
| `A3_03_matched_annual_diversity.csv` | Annual richness, Hill diversity, evenness, totals, and interpretation flags for matched taxa. |
| `A3_03_matched_taxon_dominance.csv` | Mean annual relative abundance, median rank, and occupancy for each matched taxon. |

## A3 04 — Sensitivity and feasibility

| File | Short description |
|---|---|
| `A3_04_2024_sensitivity.csv` | Fidelity statistics with and without the low-visibility 2024 bone collection. |
| `A3_04_analysis_data_scope.csv` | Plain-language statement of which observations and thresholds support each analysis. |
| `A3_04_analysis_feasibility.csv` | Available years and years reaching MNI ≥10 by sector and fence period or overlap scope. |
| `A3_04_bone_threshold_sensitivity.csv` | Numbers of retained bone years at MNI thresholds 5, 10, and 15. |
| `A3_04_overlapping_live_bone_years.csv` | Living counts, bone MNI, richness, and adequacy for sector-years present in both records. |
| `A3_04_rare_taxon_sensitivity.csv` | Overall fidelity using all matched taxa and the 20% bone-occurrence subset. |

## A3 05 — Historical ground-census validation

| File | Short description |
|---|---|
| `A3_05_figure_statistics.csv` | Regression statistics and highlighted taxa for the historical-method figure. |
| `A3_05_ground_aerial_comparison.csv` | Ground–aerial fidelity for 2002, 2003, and the pooled two-year composition. |
| `A3_05_ground_annual_diversity.csv` | Annual richness, Hill diversity, and evenness for the historical ground series. |
| `A3_05_ground_bone_fidelity.csv` | Historical ground versus temporally matched and all-Eastern bone-MNI fidelity. |
| `A3_05_ground_bone_taxon_contributions.csv` | Taxon contributions to the historical ground–bone Bray–Curtis difference. |
| `A3_05_ground_bone_year_coverage.csv` | Exact-year ground counts and corresponding estimated-year bone MNI availability. |
| `A3_05_ground_source_sensitivity.csv` | Effect of excluding Earthwatch-labelled years from the ground composition. |
| `A3_05_ground_taxon_dominance.csv` | Mean abundance, median rank, and occupancy of taxa in the ground census. |
| `A3_05_historical_method_comparisons.pdf` | Vector version of the ground–bone and ground–aerial comparison figure. |
| `A3_05_historical_method_comparisons.png` | High-resolution raster version of the historical-method comparison figure. |

## A3 06 — Estimated-year temporal fidelity

| File | Short description |
|---|---|
| `A3_06_estimated_year_fidelity.csv` | Exact-year and ±1-year living–bone fidelity statistics, coverage, and MNI adequacy for every available comparison. |
| `A3_06_estimated_year_fidelity.pdf` | Vector version of the estimated-year temporal-fidelity figure. |
| `A3_06_estimated_year_fidelity.png` | High-resolution raster version of the estimated-year temporal-fidelity figure. |
| `A3_06_estimated_year_taxon_compositions.csv` | Taxon-level living and bone relative abundances underlying every temporal comparison. |
| `A3_06_exact_vs_window_sensitivity.csv` | Direct comparison of exact-year results with the corresponding ±1-year sensitivity result. |
| `A3_06_temporal_fidelity_summary.csv` | Copy-ready summary of comparison counts, adequate MNI counts, and median fidelity statistics. |

## Rule-workbook previews

| File | Short description |
|---|---|
| `rule_preview/mniweatheringrule.xlsx` | Preview copy of the database-derived MNI weathering rules for audit and review. |
| `rule_preview/Taxa_lookup.xlsx` | Preview copy of the database-derived taxonomic alias and canonical-name rules. |
