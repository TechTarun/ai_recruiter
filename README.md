Resume similarity score calculation - 

**Metrics considered** -

* Jaccard Index
* Sorsen's Index
* Cosine Similarity
* Tversky Index

Given the parsed resumes, we are selecting a subset of fields to calculate suitability score.

Resume fields we parse are -

* [ ] name
* [ ] email
* [ ] education (do not consider because it just increase number of tokens, thus decresing score)
* [ ] technology (do not consider since not present in every parsed resume)
* [X] skills (consider because of obvious reason)
* [X] experience (consider because of obvious reason)
* [X] projects (consider because of obvious reason)
* [ ] profiles (not useful at all)
* [ ] positions (not present in all parsed resumes)
* [ ] interests (are primarily non-tech, hence not useful)
* [ ] certification (can be achieved easily, hence is not important)
* [ ] awards (irrelevant)

* Fields ticked are what we are considering for calculating score.
