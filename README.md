# Data Science Portfolio

### 1. [Segmenting Audiences for Campaign Communications: Cluster Analysis of Americans’ Views on Science](unsupervised-learning-multinomial-classification).
A global public health organization is planning an international public education campaign to promote scientific understanding and support for scientific and technological research and advancement in a number of key markets. The first step will be to gain insight into different audience segments to understand how attitudes toward a range of topics in science vary, to inform messaging strategy.
 - **Data**: Pew Research Center [International Science Survey](https://www.pewresearch.org/science/dataset/international-science-survey/), n=32,330, fielded October 1, 2019 to March 15, 2020.
 - **Methods**: KMeans Cluster Analysis, Factor Analysis, Cross-Validation, Logistic Regression, Hyperparameter Tuning (GridSearchCV), Regularization (Ridge, Lasso, Elasticnet).


### 2. [Natural Language Processing to Advance Automation: What is the Role of the Human Agent in the Customer Journey?](nlp-classification)
Many aspects of customer service are increasingly being automated. Artificial intelligence (AI), combined with customer relationship management (CRM) software, are working in combination to find efficiencies, increase customer satisfaction, and improve the work lives of customer support specialists. Taken together, these emerging technologies can automate routine tasks and support "human agents" by providing them with tools and insights to resolve customer issues quickly and efficiently. *The goal of this natural language processing classification exercise is to to explore the more extreme customer service experiences in two distinct contexts - retail and tech support - to anticipate challenges and facilitate more advanced automation where possible, and employee support where automation is still not possible.*
- **Data**: Obtained using the Pushshift Reddit API.
- **Methods**: Bag-of-words (CountVectorizer, TfidfVectorizer), Text processing (spaCy), Classification (Multinomial Naive Bayes, Random Forest), Cross-Validation, Hyperparameter Tuning (GridSearchCV, RandomizedSearchCV), Pipeline.


 ### 3. [Chartpack: Public Opinion on Child Care in the U.S.](survey-data-viz)
- **Data**: This survey was conducted online within the United States by The Harris Poll in partnership with JUST Capital between August 9-11, 2021 among 2,052 U.S. adults ages 18 and older.
- **Methods**: Data visualization (Matplotlib, Seaborn), Categorical data analysis.
