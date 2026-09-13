# Machine Learning Review Criteria

## Evaluation Dimensions
### 1. Novelty & Contribution (Weight: 20%): Novel algorithm/architecture/approach? Clear improvement over SOTA? Not just incremental? Scoring: 1-5
### 2. Technical Soundness (Weight: 25%): Methodology clearly described? Assumptions reasonable? No obvious flaws? Theoretical claims supported? Scoring: 1-5
### 3. Experimental Evaluation (Weight: 30%): Multiple random seeds (≥5)? Mean ± std reported? Recent baselines (<2 years)? Ablation studies? Fair comparison (same compute)? Statistical significance? Scoring: 1-5
### 4. Reproducibility (Weight: 15%): Code available? Hyperparameters documented? Dataset splits specified? Compute requirements stated? Scoring: 1-5
### 5. Presentation (Weight: 10%): Clear writing? Good figures/tables? Intuition before formalism? Scoring: 1-5

## Required Sections (ML Papers)
1. Abstract (with concrete numbers) / 2. Introduction / 3. Related Work / 4. Method / 5. Experiments / 6. Results (with ablations) / 7. Conclusion / 8. (Optional) Limitations, Broader Impact

## Common Issues
**Major**: Missing ablation studies, only 1-3 seeds, no recent baselines, unfair comparisons, overclaiming
**Minor**: No error bars, missing hyperparameter details, unclear architecture, no code availability

## Paper Types
### Empirical Algorithm: Focus on performance gains, ablations, fair comparisons. Must have: 5+ seeds, recent baselines, ablation study.
### Theoretical: Focus on proof correctness, intuition, practical implications. Must have: complete proofs, clear assumptions.
### Dataset/Benchmark: Focus on data quality, documentation, baseline results. Must have: data statement, license, baseline implementations.
