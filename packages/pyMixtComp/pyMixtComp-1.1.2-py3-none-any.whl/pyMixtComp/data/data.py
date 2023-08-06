import pandas as pd
import pkg_resources


def load_iris():
    """ Iris data

    The iris data set gives the measurements in centimeters of the variables sepal length and width and petal length and width,
    respectively, for 50 flowers from each of 3 species of iris. The species are Iris setosa, versicolor, and virginica.

    Returns
    -------
    (DataFrame, dict)
        Data are returned in a dataFrame with 5 columns.
        Model is returned as a dict

    References
    ----------
    Fisher, R. A. (1936) The use of multiple measurements in taxonomic problems. Annals of Eugenics, 7, Part II, 179–188.

    The data were collected by Anderson, Edgar (1935). The irises of the Gaspe Peninsula, Bulletin of the American
    Iris Society, 59, 2–5.

    Examples
    --------
    >>> import pyMixtComp
    >>> data, model = pyMixtComp.data.load_iris()
    """
    stream = pkg_resources.resource_stream(__name__, "iris.csv")
    data = pd.read_csv(stream)
    model = {"sepal length (cm)": "Gaussian", "sepal width (cm)": "Gaussian",
             "petal length (cm)": "Gaussian", "petal width (cm)": "Gaussian"}

    return data, model


def load_purchasing_behavior():
    """ Purchasing-behavior

    The dataset consists of information about the purchasing behavior of 2,000 individuals from a given area when entering a physical 'FMCG' store. All data has been collected through the loyalty cards they use at checkout. The data has been preprocessed and there are no missing values. In addition, the volume of the dataset has been restricted and anonymized to protect the privacy of the customers. 										
    
    Returns
    -------
    (DataFrame, dict)
        Data are returned in a dataFrame with 7 columns.
        Model is returned as a dict

    Notes
    -----
    data contains 2,000 records described by 7 mixed variables:
    - Sex: Biological sex (gender) of a customer. In this dataset there are only 2 different options. (Binary)
    - Marital status: Marital status of a customer. (Binary)
    - Age: The age of the customer in years, calculated as current year minus the year of birth of the customer at the time of creation of the dataset (Continuous)
    - Education: Level of education of the customer (Categorical)
    - Income: Self-reported annual income in US dollars of the customer. (Continuous)
    - Occupation: Category of occupation of the customer. (Categorical)
    - Settlement size: The size of the city that the customer lives in. (Categorical)

    References
    ----------
    https://www.kaggle.com/code/dev0914sharma/customer-clustering-model/data

    Examples
    --------
    >>> import pyMixtComp
    >>> data, model = pyMixtComp.data.load_purchasing_behavior()
    """
    stream = pkg_resources.resource_stream(__name__, "purchasing_behaviour.csv")
    data = pd.read_csv(stream, dtype=object, index_col='ID')
    model = {"Sex": "Multinomial", "Marital status": "Multinomial", "Age": "Gaussian", "Education": "Multinomial",
             "Income": "Gaussian", "Occupation": "Multinomial", "Settlement size": "Multinomial"}

    return data, model


def load_demographic():
    """ Household-level transactions

    This dataset contains household level transactions over two years from a group of 2,500 households who are frequent shoppers at a retailer. It contains all of each household’s purchases, not just those from a limited number of categories. For certain households, demographic information as well as direct marketing contact history are included.

    Due to the number of tables and the overall complexity of The Complete Journey, it is suggested that this database be used in more advanced classroom settings. Further, The Complete Journey would be ideal for academic research as it should enable one to study the effects of direct marketing to customers.
    
    Returns
    -------
    (DataFrame, dict)
        Data are returned in a dataFrame with 7 columns.
        Model is returned as a dict

    Notes
    -----
    data contains 801 records described by 7 mixed variables:
    - AGE_DESC: Age description (Categorical)
    - MARITAL_STATUS_CODE: Marital status (Categorical)
    - INCOME_DESC: Income description (Categorical)
    - HOMEOWNER_DESC: Home owner or not (Binary)
    - HH_COMP_DESC: Individual description (Categorical)
    - HOUSEHOLD_SIZE_DESC: Household size (Categorical)
    - KID_CATEGORY_DESC: How many kinds? (Categorical)

    References
    ----------
    https://www.kaggle.com/datasets/frtgnn/dunnhumby-the-complete-journey?select=hh_demographic.csv

    Examples
    --------
    >>> import pyMixtComp
    >>> data, model = pyMixtComp.data.load_demographic()
    """
    stream = pkg_resources.resource_stream(__name__, "housing.csv")
    data = pd.read_csv(stream, dtype=object, index_col='household_key')
    model = {"AGE_DESC": "Multinomial", "MARITAL_STATUS_CODE": "Multinomial", "INCOME_DESC": "Multinomial", "HOMEOWNER_DESC": "Multinomial",
             "HH_COMP_DESC": "Multinomial", "HOUSEHOLD_SIZE_DESC": "Multinomial", "KID_CATEGORY_DESC": "Multinomial"}

    return data, model


def load_candy():
    """ Halloween Candy Data

    It includes attributes for each candy along with its ranking. For binary variables, 1 means yes, 0 means no. This data set was obtained from Kaggle
    
    Returns
    -------
    (DataFrame, dict)
        Data are returned in a dataFrame with 12 columns.
        Model is returned as a dict

    Notes
    -----
    data contains 85 records described by 12 mixed variables:
    - chocolate: Does it contain chocolate? (Binary)
    - fruity: Is it fruit flavored? (Binary)
    - caramel: Is there caramel in the candy? (Binary)
    - peanutalmondy: Does it contain peanuts, peanut butter or almonds? (Binary)
    - nougat: Does it contain nougat? (Binary)
    - crispedricewafer: Does it contain crisped rice, wafers, or a cookie component? (Binary)
    - hard: Is it a hard candy? (Binary)
    - bar: Is it a candy bar? (Binary)
    - pluribus: Is it one of many candies in a bag or box? (Binary)
    - sugarpercent: The percentile of sugar it falls under within the data set. (Continuous)
    - pricepercent: The unit price percentile compared to the rest of the set. (Continuous)
    - winpercent: The overall win percentage according to 269,000 matchup. (Continuous)

    References
    ----------
    https://www.kaggle.com/code/jonathanbouchet/candies-data-visualization-clustering/data

    Examples
    --------
    >>> import pyMixtComp
    >>> data, model = pyMixtComp.data.load_candy()
    """
    stream = pkg_resources.resource_stream(__name__, "candy.csv")
    data = pd.read_csv(stream, dtype=object, index_col='competitorname')
    model = {"chocolate": "Multinomial", "fruity": "Multinomial", "caramel": "Multinomial", "peanutalmondy": "Multinomial",
             "nougat": "Multinomial", "crispedricewafer": "Multinomial", "hard": "Multinomial", "bar": "Multinomial",
             "pluribus": "Multinomial", "sugarpercent": "Gaussian", "pricepercent": "Gaussian", "winpercent": "Gaussian"}

    return data, model



def load_prostate():
    """ Prostate cancer data

    This data set was obtained from a randomized clinical trial comparing four treatments for n = 506 patients
    with prostatic cancer grouped on clinical criteria into two Stages 3 and 4 of the disease.

    Returns
    -------
    (DataFrame, dict)
        Data are returned in a dataFrame with 12 columns (see Notes).
        Model is returned as a dict

    Notes
    -----
    data contains 506 individuals described by 12 mixed variables:
    - Age: Age (Continuous)
    - HG: Index of tumour stage and histolic grade (Continuous)
    - Wt: Weight (Continuous)
    - AP: Serum prostatic acid phosphatase C (Continuous)
    - BP: Systolic blood pressure (Continuous)
    - PF: Performance rating (Categorical)
    - DBP: Diastolic blood pressure (Continuous)
    - HX: Cardiovascular disease history (Categorical)
    - SG: Serum haemoglobin (Continuous)
    - BM: Bone metastasis (Categorical)
    - SZ: Size of primary tumour (Continuous)
    - EKG: Electrocardiogram code (Categorical)

    References
    ----------
    Yakovlev, Goot and Osipova (1994), The choice of cancer treatment based on covariate information. Statist. Med.,
    13: 1575-1581. doi:10.1002/sim.4780131508

    Examples
    --------
    >>> import pyMixtComp
    >>> data, model = pyMixtComp.data.load_prostate()
    """
    stream = pkg_resources.resource_stream(__name__, "prostate.csv")
    data = pd.read_csv(stream, dtype=object)
    model = {"Age": "Gaussian", "Wt": "Gaussian", "PF": "Multinomial", "HX": "Multinomial",
             "SBP": "Gaussian", "DBP": "Gaussian", "EKG": "Multinomial", "HG": "Gaussian",
             "SZ": "Gaussian", "SG": "Gaussian", "AP": "Gaussian", "BM": "Multinomial"}

    return data, model


def load_simulated_data():
    """ Simulated data

    Data simulated from the different models used in MixtComp.

    Returns
    -------
    (DataFrame, dict)
        Data are returned in a dataFrame with 9 columns: one for each model in pyMixtComp and the true labels (z_class).
        Model is returned as a dict (z_class is not included but can be added to perform supervised clustering).

    Examples
    --------
    >>> import pyMixtComp
    >>> data, model = pyMixtComp.data.load_prostate()
    """
    stream = pkg_resources.resource_stream(__name__, "simulated_data.csv")
    data = pd.read_csv(stream, dtype=object)
    model = {"Poisson1": "Poisson", "Gaussian1": "Gaussian", "Categorical1": "Multinomial",
             "nBinom1": "NegativeBinomial", "Weibull1": "Weibull",
             "Functional1": {"type": "Func_CS", "paramStr": "nSub: 2, nCoeff: 2"},
             "FunctionalSharedAlpha1": {"type": "Func_SharedAlpha_CS", "paramStr": "nSub: 2, nCoeff: 2"},
             "Rank1": "Rank_ISR"}

    return data, model


def load_canadian_weather():
    """ Canadian average annual weather cycle

    Daily temperature and precipitation at 35 different locations in Canada averaged over 1960 to 1994.
    Data from fda R package.

    Returns
    -------
    DataFrame, dict
        Data are returned in a dataFrame with 2 columns: tempav (average temperature in degrees celsius
        for each day of the year) and precav (average rainfall in millimetres for each day of the year).
        Model is returned as a dict

    References
    ----------
    - Ramsay, James O., and Silverman, Bernard W. (2006), Functional Data Analysis, 2nd ed., Springer, New York.
    - Ramsay, James O., and Silverman, Bernard W. (2002), Applied Functional Data Analysis, Springer, New York

    Examples
    --------
    >>> import pyMixtComp
    >>> data, model = pyMixtComp.data.load_canadian_weather()
    """
    stream = pkg_resources.resource_stream(__name__, "canadian_weather.csv")
    data = pd.read_csv(stream, dtype=object)
    model = {"tempav": {"type": "Func_CS", "paramStr": "nSub: 4, nCoeff: 2"},
             "precav": {"type": "Func_CS", "paramStr": "nSub: 4, nCoeff: 2"}}

    return data, model
