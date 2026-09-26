#!/usr/bin/env bash
# Fixture: paper.txt, a dense passage with citation markers and a reference list.
set -euo pipefail
cat > paper.txt <<'TXT'
Sleep, orexin and glucose control. An umbrella review of 245 observational studies found that a sleep disorder carries the highest prevalence of type 2 diabetes of any mental disorder: 39.7% (95% CI 34.9-44.7) [1]. In type 2 diabetic db/db mice, suvorexant lowered hepatic Pepck and G6Pase mRNA and improved glucose tolerance without changing serum insulin [2]. Lemborexant given in the resting phase lengthened REM and non-REM sleep and improved glucose tolerance, again without more insulin secretion [3]. In adults with type 2 diabetes and insomnia, bedtime suvorexant improved glycemic control on continuous glucose monitoring [4]. Whether these effects are direct or follow from better sleep is unresolved.

References
1. Lindekilde N, et al. Diabetologia. 2022;65(3):440-456.
2. Tsuneki H, et al. Endocrinology. 2016;157(11):4146-4157.
3. Tsuneki H, et al. Eur J Pharmacol. 2023;961:176190.
4. Toi N, et al. J Clin Transl Endocrinol. 2019;15:37-44.
TXT
