# AI Recruiter

## An AI based intelligent way to find out best among the crowd

#### This is the source code of our BTech final year Project

## Team members -

* Tarun Agarwal
* Sandeep Kumar Shukla
* Sahyog Saini

### Steps to get backend running

```
1. git clone <repo>
2. pip install virtualenv
   python3 -m venv aienv (for linux)
   virtualenv aienv (for windows)
3. pip install -r requirements.txt
4. python manage.py migrate
5. python manage.py createsuper
6. python manage.py runserver
```

## Resume similarity score calculation -

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
