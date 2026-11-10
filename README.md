# StackWise


StackWise is a planned two-person project that builds and analyzes a knowledge network from Stack Overflow. It combines social network analysis and text analysis to study who helps whom, the cognitive levels of questions and the toxicity of answers.

StackWise is a project focused on building a Stack Overflow knowledge system that helps developers discover relevant programming solutions from historical Q&A data.


## Project Goal and Scope

The project follows the assignment's two-person option: all one-person requirements, plus verb set expansion and answer toxicity labeling. This replaces the previous search and recommendation proposal. Both partners will submit the same shared plan and confirm the scope with the instructor after reading week.

Research questions:

- Which users are active askers, answer providers, hubs, and authorities?
- How do user interactions differ across Bloom's taxonomy levels?
- How does answer toxicity vary with the level of questions asked?

## 1. Data Collection and Preparation

- Use the official [Stack Exchange API](https://api.stackexchange.com/) to collect questions and their answers for the `python` tag.
- Run a pilot collection, then document a feasible date window and sample size based on API limits and available interactions.
- Export question and answer CSVs with post IDs, user IDs, titles, bodies, tags, timestamps, and accepted-answer indicators where available.
- Document collection parameters, pagination, quota/backoff handling, and missing records. Exclude interactions without identifiable asker or answerer IDs from the graph and report the exclusions.
- Clean HTML and separate code from prose so code tokens do not dominate verb matching or toxicity scoring. Preserve raw text for review.

## 2. User Interaction Network

- Represent users as nodes, with directed edges from answerer to asker.
- Weight edges by the number of distinct questions answered between each user pair. Multiple answers by one user to the same question count once toward this weight.
- Size nodes by combined asking and answering activity in the collected dataset; scale edge thickness by edge weight.
- Analyze the full collected network and display an induced subgraph of approximately 20 users selected by activity. Document the selection rule and omitted interactions.
- Calculate in-degree centrality, out-degree centrality, HITS hub scores, and HITS authority scores. Report full-network metrics for the displayed users, with weighted interaction totals reported separately from degree centrality.
- Interpret scores according to the edge direction: incoming edges indicate receiving answers and outgoing edges indicate providing answers. Explain the structural meaning of hubs and authorities without assuming these scores directly measure expertise.

## 3. Bloom's Taxonomy Classification

- Use the supplied [Bloom's verbs table for computing](https://ccecc.acm.org/assessment/blooms-for-computing) to classify question titles and prose as Remembering, Understanding, Applying, Analyzing, Evaluating, or Creating.
- Extract verbs and preserve the matching evidence and classification method for each question.
- Document a consistent rule for questions matching multiple levels. Manually review ambiguous or unmatched questions and record the final label and rationale instead of silently assigning a default level.
- Audit a sample of question labels and discuss the limitations of using verbs as a proxy for cognitive level.
- Create a separate edge for each user pair and Bloom's level, weighted by distinct questions answered at that level. Present the original network plus six level-specific graphs if parallel edges become cluttered.

## 4. Verb Set Expansion — Two-Person Requirement

- Lemmatize extracted verbs using NLTK WordNet morphology, such as Morphy, and match their base forms against the supplied table.
- Use [WordNet](https://www.nltk.org/howto/wordnet.html) verb synonyms for verbs still unmatched after lemmatization.
- Document how ambiguous senses and synonyms matching multiple levels are resolved.
- Export the remaining unmatched verbs and create a manual fallback lookup mapping them to Bloom's levels, with a rationale for each mapping.
- Report coverage from direct matching, lemmatization, synonym expansion, and manual fallback separately.

## 5. Answer Toxicity — Two-Person Requirement

- Use a pretrained model such as [Detoxify](https://github.com/unitaryai/detoxify) to score each answer from 0 (neutral) to 1 (toxic).
- Record the model/version and preprocessing procedure. Treat scores as model estimates rather than definitive judgments about users.
- Compute average answer toxicity for each directed user-pair edge and each user-pair/Bloom's-level edge. Report the number of scored answers alongside each mean.
- Keep edge frequency based on distinct questions and toxicity means based on individual answers; document these different denominators.
- Compare toxicity distributions and sample counts across Bloom's levels. Discuss uncertainty, class imbalance, model errors, and the limits of drawing conclusions from observational data.

## Deliverables

- Reproducible API collection and preprocessing scripts.
- Raw and processed CSVs, with collection notes and a data dictionary.
- Seed verbs, expanded mappings, unmatched verb list, and manual fallback lookup.
- Question labels with classification evidence and answer-level toxicity scores.
- Original and Bloom's-level network visualizations, edge tables, and centrality/HITS results.
- Analysis notebook or report covering methods, label validation, findings, and limitations.
- Shared final report and presentation video explaining both partners' contributions.

## Work Plan

| Phase | Work | Completion criterion |
| --- | --- | --- |
| Scope alignment | Agree on the shared proposal and meet the instructor after reading week | Both partners submit the same plan and record instructor feedback |
| Collection | Pilot the API, choose the collection window, and export data | Question/answer CSVs, collection notes, and exclusion counts |
| Network analysis | Build the graph, calculate metrics, and select the display subset | Full-network metrics and a readable approximately 20-user graph |
| Text analysis | Implement Bloom's matching, verb expansion, and manual fallback | Traceable labels, coverage results, and a manually audited sample |
| Toxicity analysis | Score answers and aggregate by edge and Bloom's level | Answer scores, edge means, and comparisons across levels |
| Integration | Combine results and prepare the final deliverables | Reproducible analysis, shared report, and presentation |

## Proposed Partner Responsibilities

- **Partner 1:** Lead API collection, data documentation, graph construction, network metrics, and visualization.
- **Partner 2:** Lead text preprocessing, Bloom's classification, verb expansion, manual mappings, and toxicity scoring.
- **Both partners:** Agree on schemas and labeling rules, audit classifications, interpret results, integrate the pipeline, and prepare the report and presentation. Confirm names and responsibilities together before submission.

## Planned Tech Stack

Python, pandas, NumPy, requests, NetworkX, NLTK/WordNet, Matplotlib, Jupyter, and a pretrained toxicity model such as Detoxify. Dependencies will be updated as the corresponding components are implemented.

## Repository Status

The repository is currently a scaffold. Existing search-related code belongs to the earlier proposal; the network and text-analysis pipeline described here is planned work. Search, embeddings, answer recommendation, and a web interface are outside the required project scope.

## Getting Started

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

These commands install the current scaffold dependencies; they do not yet run the planned analysis pipeline.

## License

This project is for academic and portfolio use. Document source attribution and applicable Stack Overflow content licensing when distributing collected data.
