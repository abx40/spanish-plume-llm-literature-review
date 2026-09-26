# Systematic search: "Spanish plume" in peer-reviewed meteorological journals (to 13 August 2023)

**Run date:** 13 August 2026
**Model:** Claude Opus 5 (claude-opus-5), Claude Code
**Browser:** Claude in Chrome connector, University of Manchester authenticated session
**Independence:** conducted without reference to Schultz et al.'s review or dataset. The two Schultz et al. papers that surfaced in the searches (MWR 153(5), 2025; QJRMS 151(773), 2025) were recorded as retrieved records only, were not opened, and their reference lists were not consulted. Both post-date the cut-off and are excluded on date.

---

## 1. Databases, queries and result counts

| Database | Query as entered | Fields searched | Date filter | Results |
|---|---|---|---|---|
| Google Scholar | `"Spanish plume"` | full text (incl. citations; patents excluded) | `as_yhi=2023` (to end 2023) | **183** |
| Wiley Online Library (incl. RMetS: *Weather*, *QJRMS*, *Met. Apps*, *Int. J. Climatol.*) | `"Spanish plume"` | Anywhere (AllField) | none (screened manually) | **85** |
| AMS Journals Online | `"Spanish plume"` | All content, full text | none (screened manually) | **17** |
| Web of Science Core Collection | `"Spanish plume"` (All Fields), all editions | title/abstract/keywords/cited-refs | none (screened manually) | **11** |
| | | | **Total retrieved** | **296** |

Wiley journal-title breakdown (facet): *Weather* 49, *QJRMS* 17, *Int. J. Climatology* 6, *Meteorological Applications* 4, Wiley Online Books 5, other titles 4.
AMS journal breakdown (facet): *Mon. Wea. Rev.* 7, *Wea. Forecasting* 7, *J. Climate* 1, *J. Atmos. Sci.* 1, *J. Phys. Oceanogr.* 1.

**After deduplication: 209 unique records.**

| Deduplication step | Records |
|---|---|
| Retrieved across four databases | 296 |
| Google Scholar internal duplicates removed | −6 |
| Wiley records already retrieved by Scholar | −60 |
| AMS records already retrieved by Scholar/Wiley | −12 |
| WoS records already retrieved by Scholar/Wiley/AMS | −9 |
| **Unique records** | **209** |

Contribution by database after deduplication: Google Scholar 177 unique of 183; Wiley 25 records not found by Scholar; AMS 5 not found by Scholar or Wiley; Web of Science 2 not found by any other database.

The six Google Scholar internal duplicates are repository or secondary copies of works already in the set: Allan et al. (ResearchGate copy of the *Int. J. Climatol.* paper), Pinto (academia.edu copy of Mathias et al. 2017), Lhotka & Kyselý (thesis chapter reproducing the 2015 paper), Geerts (second record of Speer & Geerts 1994), Piper (book edition of the Karlsruhe dissertation), and the duplicated Stan/Sussman record for the same book chapter.

The 25 Wiley-only records are mostly non-article journal matter that Scholar does not index — complete issues, Letters to the Editor, Readers' Forum, Society news, volume indexes, Issue Information, TORRO book front/back matter — plus eight genuine articles Scholar missed (Gray & Marshall 1998; Galvin, Bennett & Couchman 1995; Webb 2011; Webb & Blackshaw 2012; Galvin 2003 *Observing the sky*; Förchtgott 1996; Lionetti 1996; Mayes & Wheeler 2013 Part 1; Mayes 2013 Part 2; Field 1999). The 5 AMS-only records are Trömel et al. (2017), Taszarek et al. (2020), Poręba et al. (2022) and the two post-cut-off 2025 papers. The 2 WoS-only records are Worthington (2015, *Weather*) — notably missed by Wiley's own phrase search — and Whitford et al. (2024, post cut-off).

Editions of the same literary work (Thomas Campbell's and Fitz-Greene Halleck's poetry, ten and five records respectively) are counted as distinct bibliographic records rather than merged; treating them as single works would reduce the unique total to about 196. All are excluded as non-meteorological either way.

### Access and technical notes
- Manchester authentication was live throughout: "Findit@Manchester" on Scholar records, "University of Manchester Library" on every Wiley record, WoS resolved by institutional IP ([redacted]).
- **Google Scholar rate-limiting.** Requests with `num=20` triggered a reCAPTCHA. No CAPTCHA was solved; reverting to the default 10-results-per-page removed the block and all 183 records were retrieved.
- **Web of Science under-retrieves by design.** WoS does not index article full text, so "All Fields" reaches only title/abstract/keywords/cited references. Since "Spanish plume" almost always appears mid-article, WoS returned 11 records against Scholar's 183. This is a database limitation, not a search failure, and WoS should not be treated as an independent check on recall for this phrase.
- **Verification limitation on older articles.** For *Weather* and *Meteorological Applications* articles published before ~2005, Wiley serves only metadata and the reference list as HTML; the article body exists only as a scanned PDF. Direct in-page verification of where the phrase falls is therefore impossible for that cohort, and a naive HTML check wrongly reports "reference-list only". Those records were judged on Google Scholar's PDF-derived snippets instead. Each row below carries its evidence basis.

**Evidence key:** `V` = verified in publisher full text (occurrence located outside the reference list); `S` = database snippet shows the phrase in running prose; `U` = phrase location not verifiable from available HTML.

---

## 2. Included papers (n = 80)

| # | Title | Authors | Year | Journal | DOI / URL | Database(s) | Ev. |
|---|---|---|---|---|---|---|---|
| 1 | Conditions for the occurrence of severe local storms | Carlson, Ludlam | 1968 | Tellus | 10.1111/j.2153-3490.1968.tb00364.x | GS, Wiley | S |
| 2 | Severe thunderstorms over south-east England, 20/21 July 1992 | McCallum, Waters | 1993 | Weather | 10.1002/j.1477-8696.1993.tb05886.x | GS, Wiley | S |
| 3 | Forecasting thunderstorm initiation in north-west Europe using thermodynamic indices, satellite and radar data | Collier, Lilley | 1994 | Meteorological Applications | 10.1002/j.1469-8080.1994.tb00008.x | GS, Wiley | S |
| 4 | Severe thunderstorms over south-east England on 24 June 1994: a forecasting perspective | Young | 1995 | Weather | 10.1002/j.1477-8696.1995.tb06121.x | GS, Wiley | S |
| 5 | Comparison of traditional and newly developed thunderstorm indices for Switzerland | Huntrieser, Schiesser, Schmid, Waldvogel | 1997 | Weather and Forecasting | 10.1175/1520-0434(1997)012<0108:COTAND>2.0.CO;2 | AMS, GS | S |
| 6 | Monitoring European weather extremes using newspapers and the Internet | Perry | 1997 | Weather | 10.1002/j.1477-8696.1997.tb06279.x | GS, Wiley | S |
| 7 | Thunderstorms and hail on 7 June 1996: an early season 'Spanish plume' event | Webb, Pike | 1998 | Weather | 10.1002/j.1477-8696.1998.tb06391.x | GS, Wiley | S |
| 8 | The synoptic setting of a thundery low and associated prefrontal squall line in western Europe | van Delden | 1998 | Meteorology and Atmospheric Physics | 10.1007/BF01030273 | GS, WoS | S |
| 9 | The synoptic setting of thunderstorms in western Europe | van Delden | 2001 | Atmospheric Research | 10.1016/S0169-8095(00)00071-5 | GS | S |
| 10 | Summer thunderstorms | Galvin | 2003 | Weather | 10.1256/wea.172.02 | GS, Wiley | S |
| 11 | Numerical modeling study of boundary-layer ventilation by a cold front over Europe | Agustí-Panareda, Gray, Methven | 2005 | J. Geophys. Res. | 10.1029/2004JD005555 | GS, Wiley | S |
| 12 | Occurrence of summertime convective precipitation and mesoscale convective systems in Finland during 2000–01 | Punkka, Bister | 2005 | Mon. Wea. Rev. | 10.1175/MWR-2854.1 | AMS, GS | S |
| 13 | A review of cold fronts with prefrontal troughs and wind shifts | Schultz | 2005 | Mon. Wea. Rev. | 10.1175/MWR2987.1 | AMS, GS | S |
| 14 | A review of the initiation of precipitating convection in the United Kingdom | Bennett, Browning, Blyth, Parker, Clark | 2006 | QJRMS | 10.1256/qj.05.54 | GS, Wiley | S |
| 15 | Mesoscale simulations of organized convection: importance of convective equilibrium | Done, Craig, Gray, Clark, Gray | 2006 | QJRMS | 10.1256/qj.04.84 | GS, Wiley | S |
| 16 | On the dependence of boundary layer ventilation on frontal type | Agustí-Panareda, Gray, Methven | 2009 | J. Geophys. Res. | 10.1029/2008JD010694 | GS, Wiley | S |
| 17 | Categorisation of synoptic environments associated with mesoscale convective systems over the UK | Lewis, Gray | 2010 | Atmospheric Research | 10.1016/j.atmosres.2009.10.001 | GS, WoS | S |
| 18 | Violent thunderstorms in the Thames Valley and south Midlands in early June 1910 | Webb | 2011 | Weather | 10.1002/wea.799 | Wiley | **V** |
| 19 | Thunderstorms from a Spanish Plume event on 28 June 2011 | Sibley | 2012 | Weather | 10.1002/wea.1928 | GS, Wiley, WoS | S |
| 20 | Investigation of the passage of a derecho in Belgium | Hamid | 2012 | Atmospheric Research | 10.1016/j.atmosres.2011.12.013 | GS | S |
| 21 | The remarkably thundery month of June 1982 | Prichard | 2012 | Weather | 10.1002/wea.1891 | GS, Wiley | S |
| 22 | Severe thunderstorms disrupt the Diamond Jubilee on Midsummer Day 1897 | Webb | 2012 | Weather | 10.1002/wea.1959 | GS, Wiley | S |
| 23 | Notable Scottish thunderstorms in summer 2011 | Webb, Blackshaw | 2012 | Weather | 10.1002/wea.1953 | Wiley | **V** |
| 24 | A severe hailstorm across the English Midlands on 28 June 2012 | Clark, Webb | 2013 | Weather | 10.1002/wea.2162 | GS, Wiley | S |
| 25 | Analysis of the 18 July 2005 tornadic supercell over the Lake Geneva region | Peyraud | 2013 | Weather and Forecasting | 10.1175/WAF-D-13-00022.1 | AMS, GS | S |
| 26 | Thunderstorms over northern England on 6 August 2011 | Young | 2013 | Weather | 10.1002/wea.1996 | GS, Wiley | S |
| 27 | Regional weather and climates of the British Isles – Part 1: Introduction | Mayes, Wheeler | 2013 | Weather | 10.1002/wea.2041 | Wiley | **V** |
| 28 | Regional weather and climates of the British Isles – Part 2: South East England and East Anglia | Mayes | 2013 | Weather | 10.1002/wea.2073 | Wiley | **V** |
| 29 | A four-year (2007–2010) analysis of long-lasting deep convective systems in the Mediterranean basin | Melani, Pasi, Gozzini, Ortolani | 2013 | Atmospheric Research | 10.1016/j.atmosres.2012.09.008 | GS | S |
| 30 | A climatology of convective available potential energy in Great Britain | Holley, Dorling, Steele, Earl | 2014 | Int. J. Climatology | 10.1002/joc.3976 | GS, Wiley, WoS | S |
| 31 | Flash flooding in southwest England 29 May 2008 | Sibley, Denning | 2014 | Weather | 10.1002/wea.2179 | GS, Wiley | S |
| 32 | Predicting small-scale, short-lived downbursts: case study with the NWP limited-area ALARO model for the Pukkelpop thunderstorm | De Meutter, Gerard, Smet, Hamid, Hamdi, Degrauwe, Termonia | 2015 | Mon. Wea. Rev. | 10.1175/MWR-D-14-00290.1 | AMS, GS | S |
| 33 | An unusual thunderstorm event overnight 13/14 June 2014 | Grahame, Page, Hickman, Pearson | 2015 | Weather | 10.1002/wea.2480 | GS, Wiley, WoS | S |
| 34 | Mesoscale air transport at a midlatitude squall line in Europe – a numerical analysis | Uebel, Bott | 2015 | QJRMS | 10.1002/qj.2610 | GS, Wiley | **V** |
| 35 | Hot Central-European summer of 2013 in a long-term context | Lhotka, Kyselý | 2015 | Int. J. Climatology | 10.1002/joc.4277 | GS, Wiley | **V** |
| 36 | Characterisation of convective regimes over the British Isles | Flack, Plant, Gray, Lean, Keil, Craig | 2016 | QJRMS | 10.1002/qj.2758 | GS, Wiley | **V** |
| 37 | The origin of western European warm-season prefrontal convergence lines | Dahl, Fischer | 2016 | Weather and Forecasting | 10.1175/WAF-D-15-0161.1 | AMS, GS | S |
| 38 | Fronts – Who needs them? | Owens | 2016 | Weather | 10.1002/wea.2741 | GS, Wiley | **V** |
| 39 | Performance of 4D-Var NWP-based nowcasting of precipitation at the Met Office for summer 2012 | Ballard, Li, Simonin, Caron | 2016 | QJRMS | 10.1002/qj.2665 | GS, Wiley | S |
| 40 | A long-lived supercell over mountainous terrain | Scheffknecht, Serafin, Grubišić | 2017 | QJRMS | 10.1002/qj.3127 | GS, Wiley | S |
| 41 | Synoptic analysis and hindcast of an intense bow echo in western Europe: the 9 June 2014 storm | Mathias, Ermert, Kelemen, Ludwig, Pinto | 2017 | Weather and Forecasting | 10.1175/WAF-D-16-0192.1 | AMS, GS | S |
| 42 | Multisensor characterization of mammatus | Trömel, Ryzhkov, Diederich, Mühlbauer, Kneifel, Snyder, Simmer | 2017 | Mon. Wea. Rev. | 10.1175/MWR-D-16-0187.1 | AMS | S |
| 43 | The Met Office convective-scale ensemble, MOGREPS-UK | Hagelin, Son, Swinbank, McCabe, Roberts, Tennant | 2017 | QJRMS | 10.1002/qj.3135 | GS, Wiley | S |
| 44 | Improvements in nowcasting capability: analysis of three structurally distinct severe thunderstorms across northern England on 1 July 2015 | Lewis, Silkstone | 2017 | Weather | 10.1002/wea.2837 | GS, Wiley | S |
| 45 | Spatiotemporal variability of lightning activity in Europe and the relation to the North Atlantic Oscillation teleconnection pattern | Piper, Kunz | 2017 | Nat. Hazards Earth Syst. Sci. | 10.5194/nhess-17-1319-2017 | GS | S |
| 46 | Identification of favorable environments for thunderstorms in reanalysis data | Westermayer, Groenemeijer, Pistotnik, Pucik, Holzer | 2017 | Meteorologische Zeitschrift | 10.1127/metz/2016/0754 | GS | S |
| 47 | Compiling lightning counts for the UK land area and an assessment of the lightning risk facing UK inhabitants | Elsom, Enno, Horseman, Webb | 2018 | Weather | 10.1002/wea.3077 | GS, Wiley | S |
| 48 | Characterising flash flood response to intense rainfall and impacts using historical information and gauged data in Britain | Archer, Fowler | 2018 | J. Flood Risk Management | 10.1111/jfr3.12187 | GS, Wiley | **V** |
| 49 | Quantifying the effect of different urban planning strategies on heat stress for current and future climates in the agglomeration of The Hague | Koopmans, Ronda, Steeneveld, Holtslag | 2018 | Atmosphere | 10.3390/atmos9090353 | GS | S |
| 50 | An objective verification system for thunderstorm risk forecasts | Brown, Buchanan | 2019 | Meteorological Applications | 10.1002/met.1748 | GS, Wiley | S |
| 51 | Investigation of the temporal variability of thunderstorms in central and western Europe and the relation to large-scale flow and teleconnection patterns | Piper, Kunz, Allen, Mohr | 2019 | QJRMS | 10.1002/qj.3647 | GS, Wiley | **V** |
| 52 | Downstream influence of mesoscale convective systems. Part 1: influence on forecast evolution | Clarke, Gray, Roberts | 2019 | QJRMS | 10.1002/qj.3593 | GS, Wiley | S |
| 53 | Downstream influence of mesoscale convective systems. Part 2: influence on ensemble forecast skill and spread | Clarke, Gray, Roberts | 2019 | QJRMS | 10.1002/qj.3613 | GS, Wiley | S |
| 54 | Relationship between atmospheric blocking and warm-season thunderstorms over western and central Europe | Mohr, Wandel, Lenggenhager, Martius | 2019 | QJRMS | 10.1002/qj.3603 | GS, Wiley | **V** |
| 55 | Classification of synoptic conditions of summer floods in Polish Sudeten Mountains | Bednorz, Wrzesiński, Tomczyk, Jasik | 2019 | Water | 10.3390/w11122717 | GS | S |
| 56 | Atmospheric precursors for intense summer rainfall over the United Kingdom | Allan, Blenkinsop, Fowler, Champion | 2020 | Int. J. Climatology | 10.1002/joc.6431 | GS, Wiley | S |
| 57 | Europe extreme heat 22–26 July 2019: was it caused by subsidence or advection? | de Villiers | 2020 | Weather | 10.1002/wea.3717 | GS, Wiley | S |
| 58 | Mesoscale model simulation of a severe summer thunderstorm in the Netherlands | Steeneveld, Peerlings | 2020 | Atmosphere | 10.3390/atmos11080811 | GS | S |
| 59 | Severe convective storms across Europe and the United States. Part II: ERA5 environments associated with lightning, large hail, severe wind, and tornadoes | Taszarek, Allen, Púčik, Hoogewind, Brooks | 2020 | J. Climate | 10.1175/JCLI-D-20-0346.1 | AMS | S |
| 60 | Comparison of short-period daytime convective rainfall accumulations with total column precipitable water | Young, Lamb, Lane, Lattimore | 2020 | Meteorological Applications | 10.1002/met.1903 | GS, Wiley | S |
| 61 | Severe thunderstorms with large hail across Germany in June 2019 | Wilhelm, Mohr, Punge, Mühr, Schmidberger, Daniell, Bedka, Kunz | 2021 | Weather | 10.1002/wea.3886 | GS, Wiley | **V** |
| 62 | Exploring relationships between weather patterns and observed lightning activity for Britain and Ireland | Wilkinson, Neal | 2021 | QJRMS | 10.1002/qj.4099 | GS, Wiley, WoS | S |
| 63 | Severe thunderstorm, Jersey, 25 June 2020 | Winter, Galvin | 2021 | Weather | 10.1002/wea.3949 | GS, Wiley | S |
| 64 | Two hundred years of thunderstorms in Oxford | Burt | 2021 | Weather | 10.1002/wea.3884 | GS, Wiley | S |
| 65 | Reflections of over 40 years in the Met Office – a period of unprecedented change | Young | 2021 | Weather | 10.1002/wea.3956 | GS, Wiley | S |
| 66 | An 8-yr meteotsunami climatology across northwest Europe: 2010–17 | Williams, Schultz, Horsburgh, Hughes | 2021 | J. Physical Oceanography | 10.1175/JPO-D-20-0175.1 | AMS, GS | S |
| 67 | Convective rear-flank downdraft as driver for meteotsunami along English Channel and North Sea coasts 28–29 May 2017 | Sibley, Cox, Tappin | 2021 | Natural Hazards | 10.1007/s11069-020-04443-5 | GS | S |
| 68 | A characterisation of Alpine mesocyclone occurrence | Feldmann, Germann, Gabella, Berne | 2021 | Weather and Climate Dynamics | 10.5194/wcd-2-1225-2021 | GS | S |
| 69 | North Atlantic air pressure and temperature conditions associated with heavy rainfall in Great Britain | Barnes, Svensson, Kjeldsen | 2022 | Int. J. Climatology | 10.1002/joc.7414 | GS, Wiley | S |
| 70 | A regional lightning climatology of the UK and Ireland and sensitivity to alternative detection networks | Hayward, Whitworth, Pepin, Dorling | 2022 | Int. J. Climatology | 10.1002/joc.7680 | GS, Wiley | S |
| 71 | A gridded 30-year days of thunder climatology for the United Kingdom | Stone, Horseman, Odams, Marlton | 2022 | QJRMS | 10.1002/qj.4336 | GS, Wiley | **V** |
| 72 | Reconstruction of violent tornado environments in Europe: high-resolution dynamical downscaling of ERA5 | Pilguj, Taszarek, Kryza, Brooks | 2022 | Geophysical Research Letters | 10.1029/2022GL098242 | GS, Wiley | **V** |
| 73 | Meteotsunamis reported around Britain and Ireland, and northern France, 18–19 June 2022 | Sibley | 2022 | Weather | 10.1002/wea.4271 | GS, Wiley | S |
| 74 | Diurnal and seasonal variability of ERA5 convective parameters in relation to lightning flash rates in Poland | Poręba, Taszarek, Ustrnul | 2022 | Weather and Forecasting | 10.1175/WAF-D-21-0099.1 | AMS | S |
| 75 | The history of UK weather forecasting… Part 2: the birth of operational numerical weather prediction | Young, Grahame | 2023 | Weather | 10.1002/wea.4216 | GS, Wiley | S |
| 76 | The history of UK weather forecasting… Part 3: cumulative progress in forecasting – the 1970s | Young, Grahame | 2023 | Weather | 10.1002/wea.4276 | GS, Wiley | S |
| 77 | The history of UK weather forecasting… Part 6: the late twentieth century: forecasting smaller-scale features | Young, Grahame | 2023 | Weather | 10.1002/wea.4370 | GS, Wiley | S |
| 78 | Thunderstorm tracking in Northwest Europe for enhanced hazard preparedness | Hayward, Whitworth, Pepin, Dorling | 2023 | Int. J. Climatology | 10.1002/joc.8123 | GS, Wiley | S |
| 79 | Meteotsunami in the United Kingdom: the hidden hazard | Lewis, Smyth, Williams, Neumann, Hughes | 2023 | Nat. Hazards Earth Syst. Sci. | 10.5194/nhess-23-2531-2023 | GS | S |
| 80 | Changes in synoptic circulations associated with documented derechos over France in the past 70 years | Fery, Faranda | 2023 | Weather and Climate Dynamics | 10.5194/wcd-2023-19 | GS | S |

Notes on borderline inclusions, flagged rather than silently resolved:
- **#13 Schultz (2005)** and **#59 Taszarek et al. (2020)** are not exclusively European — both are global/transatlantic in scope but treat the Spanish plume as a European phenomenon in running text. Retained; a stricter reading of "studies of weather outside Europe" would drop them.
- **#48 Archer & Fowler**, **#55 Bednorz et al.**, **#66 Williams et al.**, **#67 Sibley et al.** sit in flood-risk, hydrology, oceanography and hazards journals rather than strictly meteorological ones. All are meteorologically driven studies of European weather. Retained with this caveat.
- **#77 Young & Grahame Part 6** carries a November 2023 issue date but was published online 27 February 2023, inside the cut-off. **#78, #79, #80** are 2023 papers published before 13 August 2023.
- **#65 Young (2021)** and **#10 Galvin (2003)** are reflective/instructional pieces in *Weather* rather than primary research, but are bylined peer-reviewed articles rather than editorial matter.

---

## 3. Candidates meeting all other criteria, phrase location unverified (n = 11)

Retrieved as journal articles within scope, but I could not confirm from available full text whether "Spanish plume" appears in the body or only in the reference list. Listed separately rather than folded into the count.

| Title | Authors | Year | Journal | DOI |
|---|---|---|---|---|
| Case study of a tornado in the Upper Rhine valley | Hannesen, Dotzek, Gysi, Beheng | 1998 | Meteorologische Zeitschrift | 10.1127/metz/7/1998/163 |
| Tornadoes in Germany | Dotzek | 2001 | Atmospheric Research | 10.1016/S0169-8095(00)00076-4 |
| Climatology of severe hailstorms in Great Britain | Webb, Elsom, Reynolds | 2001 | Atmospheric Research | 10.1016/S0169-8095(00)00068-5 |
| Characterization of plumes on top of deep convective storm using AVHRR imagery and radiative transfer simulations | Melani, Cattani, Torricella, Levizzani | 2003 | Atmospheric Research | 10.1016/S0169-8095(03)00069-4 |
| Tornadoes in Germany 1950–2003 and their relation to particular weather conditions | Bissolli, Grieser, Dotzek, Welsch | 2007 | Global and Planetary Change | 10.1016/j.gloplacha.2006.11.007 |
| Stratosphere–troposphere transport in a numerical simulation of midlatitude convection | Chagnon, Gray | 2007 | J. Geophys. Res. | 10.1029/2007JD008645 |
| High-resolution assessment of the hail hazard over complex terrain from radar and insurance data | Kunz, Puskeiler | 2010 | Meteorologische Zeitschrift | 10.1127/0941-2948/2010/0452 |
| Extreme hail day climatology in Southwestern France | Berthet, Wesolek, Dessens, Sanchez | 2013 | Atmospheric Research | 10.1016/j.atmosres.2013.01.008 |
| Extreme precipitation events in the Polish Carpathians and their synoptic determinants | Wypych, Ustrnul, Czekierda, Palarz, Sulikowska | 2018 | Int. J. Climatology | 10.1002/joc.5379 |
| Ambient conditions prevailing during hail events in central Europe | Kunz, Wandel, Fluck, Baumstark, Mohr, Schemm | 2020 | Nat. Hazards Earth Syst. Sci. | 10.5194/nhess-20-1867-2020 |
| The global weather enterprise, part 3: an evolving picture | Thorpe | 2023 | Weather | 10.1002/wea.4423 |

Also unresolved, and excluded above on other grounds or left pending: *Mesoscale convective systems over the UK, 1981–97* (Gray & Marshall, *Weather* 1998, 10.1002/j.1477-8696.1998.tb06352.x) — the only HTML-visible occurrence is the Morris (1986) reference entry, but the article body is not in HTML, so a body mention cannot be ruled out; *Two thunderstorms in summer 1994 at Birmingham* (Galvin, Bennett & Couchman, *Weather* 1995, 10.1002/j.1477-8696.1995.tb06120.x); *Observing the sky – how do we recognise clouds?* (Galvin, *Weather* 2003, 10.1256/wea.218.02); *The slope of isentropes constituting a frontal zone* (van Delden, *Tellus A* 1999, 10.1034/j.1600-0870.1999.00005.x); *Anomalous cloud and precipitation systems* (Förchtgott, *Weather* 1996); *The Italian floods of 4–6 November 1994* (Lionetti, *Weather* 1996); *Diary of a frustrated allotment-holder* (Turnbull, *Weather* 1997).

---

## 4. Screening totals

| Stage | Count |
|---|---|
| Records retrieved across four databases | **296** |
| Duplicate records removed | **87** |
| Unique records after deduplication | **209** |
| Excluded at screening | **118** |
| Held as unverified candidates (not counted in the 80) | **11** |
| **Included** | **80** |

---

## 5. Exclusion reasons

Counts below are approximate where a record could fall under more than one reason (a German-language thesis, for example, is both non-English and a thesis); each record is assigned to its single most decisive reason, and the column sums to the 118 excluded. The duplicate row is listed for completeness but those records were removed at deduplication, before screening, and are not part of the 118.

| Reason | Approx. n | Examples |
|---|---|---|
| Not meteorological | ~35 | Thomas Campbell's and Fitz-Greene Halleck's poetry (multiple editions; "Spanish plume" = a hat feather), Sir John Moore Peninsular War histories, *Kansas in Literature*, costume-history text, grasshopper conservation, migration-poetry criticism, an art-history thesis |
| Books and book chapters | ~14 | TORRO *Extreme Weather* chapters (Webb; Webb & Elsom; Clark & Smart) and its index/supplementary matter; *Regional Climates of the British Isles* chapters; *A Dictionary of Weather*; *Weather Wise* |
| Theses and dissertations | ~14 | Williams (2020); Dey (2016); Tijssen (2015); Hulton (2022); Pizzuti (2021); Proksch (2017); Budde (2017); Bos & Kroon (2014); Burton (2011); Özdemir (2016) |
| Non-peer-reviewed serials, reports, proceedings, newsletters, preprints | ~13 | **Morris (1986)**, *Meteorological Magazine* (see note); Dotzek (2002), *J. Meteorology*; Elsom & Webb (2017) and Webb (2014), *Int. J. Meteorology*; THORPEX science plan; COST-75 proceedings; ALADIN-HIRLAM newsletter; EUMeTrain training material; SSRN preprint |
| Non-article journal matter | ~13 | *Weather* complete issues (77(7), 77(8), 78(1), 78(3), 78(11), 79(1)); Readers' Forum; Letters to the Editor (×2); Society news; volume Index; QJRMS Issue Information; book reviews (Gray 2011; LePere 2023); obituary (Campbell-Wright 2021) |
| Non-English | ~7 | Mathias (2015) and Piper (2017), German; Huntrieser (1995), German; Kapsch (2011), German; Dotzek et al. (1999), German; Púčik (2013), Czech; Özdemir et al. (2015), Turkish; Álvarez (1995), Spanish |
| Weather outside Europe | ~5 | Hanstrum, Wilson & Barrell (1990) Parts I & II, southern Australia; Speer & Geerts (1994), Sydney; Charney & Fritsch (1999) and Bryan & Fritsch (2000), United States; Özdemir & Deniz (2016) and Tuncay & Ali (2020), Turkish airports (Anatolia) |
| Published after 13 August 2023 | 5 | Schultz, Young & Kirshbaum (2025) *MWR*; Schultz et al. (2025) *QJRMS*; Pilguj et al. (2025) *MWR*; Whitford, Blenkinsop & Fowler (2024) *Climate Dynamics*; *Weather* 79(1) complete issue (Jan 2024) |
| Phrase appears only in the reference list | 5 confirmed | Spengler, Reeder & Smith (2005) *QJRMS* — verified: single occurrence is the Morris (1986) entry; Jones & Macpherson (1997) *Meteorological Applications* — verified likewise; Charney & Fritsch (1999) *MWR*; Bryan & Fritsch (2000) *JAS*; Webb (2005) "Hailstorms", *Weather* |
| Duplicate records | ~12 | Repository/preprint copies indexed separately by Scholar (ResearchGate, academia.edu, institutional repositories); thesis chapters reproducing published articles; one Scholar record with garbled metadata merging Sibley's *Weather* 2022 article with a *Lancet* record |

### Note on Morris (1986)
*The Spanish plume — testing the forecaster's nerve*, Morris, *Meteorological Magazine* 115(1372), 349–357 is the origin of the term and the most-cited item in this literature (44 WoS citations, 68 Scholar). It is excluded here because the *Meteorological Magazine* was the UK Met Office's house periodical, not a peer-reviewed journal, and the criteria exclude non-peer-reviewed material. This is the single most consequential exclusion decision in the set and is flagged for your judgement rather than buried in the table.

---

## 6. Search reproducibility

```
Google Scholar   https://scholar.google.com/scholar?hl=en&as_sdt=0,5&q=%22Spanish+plume%22&as_yhi=2023
Wiley            https://onlinelibrary.wiley.com/action/doSearch?AllField=%22Spanish+plume%22&startPage=0&pageSize=100
AMS              https://journals.ametsoc.org/search?q1=%22Spanish%20plume%22&fl_SiteID=1&pageSize=50&sort=relevance
Web of Science   WoS Core Collection, Advanced Search, ALL=("Spanish plume"), Editions: All
```

Raw per-database record lists: `raw_scholar.md`, `raw_wiley.md`, `raw_ams.md`, `raw_wos.md`.
