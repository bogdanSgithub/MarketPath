## Project Overview 🚀
Navigating the stock market can be both exciting and daunting. With its potential for significant financial gain comes the risk, especially for those who are new to investing. **MarketPath** aims to simplify this journey, making the stock market more accessible and less intimidating for beginners. By providing intuitive insights and predictions, MarketPath helps users make informed investment decisions with confidence.

## Problem Identification 🔍
**Objective:**  
Develop a model to predict which S&P 500 stocks will outperform the market over the next 12 months. Leveraging advanced machine learning techniques, the model provides actionable insights to guide investment strategies.

**Why It Matters:**  
Identifying stocks poised to beat the market can significantly enhance investment decisions, leading to potential financial growth and a more secure future.

## Target Audience 🎯
Designed for both novice and seasoned investors, the tool offers valuable data-driven predictions on which S&P 500 stocks are likely to outperform the market, helping users refine their investment strategies.

## Scope and Constraints 📊
The AI tool will analyze financial data from S&P 500 stocks to forecast which ones may exceed the market's performance by 10% over the next year.

### DISCLAIMER
**Past performance does not guarantee future results.** Use MarketPath AI to enhance your investment strategy, but be mindful of the risks involved in stock market investing.

## Datasets 📁
Three datasets are used:
- **Training/Testing:** 2003-2013 from [Python Programming](https://pythonprogramming.net/data-acquisition-machine-learning/)
- **Testing:** 2017-2018 from the same source
- **Prediction:** 2024 from [Yahoo Finance](https://ca.finance.yahoo.com/quote/NVDA/)

## Data Collection and Exploration 🔎
- Searched the web and scraped data to gather financial information.
- Iteratively refined features to enhance model performance.
- Removed features with high percentages of missing values (NaN).
- Conducted exploratory data analysis to understand data patterns and distributions.

## Model Selection and Training 🔧
**Models Tested:**  
Logistic Regression, K-Nearest Neighbors (KNN), Decision Tree Classifier, Random Forest Classifier

**Training Process:**  
- Handled NaN values, converted features to integers, and performed feature engineering to optimize the model. 
- Split the initial dataset (2003-2013) into 80% training and 20% testing, while using subsequent datasets (2017-2018 and 2024) for further testing and predictions.

**Evaluation Metrics:**  
- Used confusion matrix and compared the average percent change of predicted stocks to the market over 12 months.

**Success Criteria:**  
- Stocks predicted to beat the market should indeed outperform it.

**Results:**  
- The Random Forest Classifier proved to be the most accurate model.

## Ethical Considerations 🤝
- **Transparency:** Past performance does not guarantee future results. Use MarketPath AI to enhance your investment strategy, but be mindful of the risks involved in stock market investing.
- **Data Privacy:** Data used was open source and free to use.

## Future Steps 🚀
- **Enhance Feature Engineering:** Refine feature selection and transformation to boost model accuracy.
- **Update Data:** Collect and integrate data from more recent years to keep predictions relevant and accurate.
