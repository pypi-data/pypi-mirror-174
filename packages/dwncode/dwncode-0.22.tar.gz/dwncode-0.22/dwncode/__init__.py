# def pretty(a):
a = """
    #### Slice Operation \n
    SELECT Prod_name ,Total_sales \n
    FROM Fact_sales  \n
    INNER JOIN Product_dw \n
    ON Fact_sales.prod_id =Product_dw.prod_id  WHERE prod_name='Rice'; \n
 
    #### Dice Operation  \n
    Select Prod_name ,Fact_sales.total_sales \n
    from((Product_dw INNER JOIN  Fact_sales ON Product_dw.prod_id=Fact_sales.prod_id)  \n
    JOIN Time_dw ON  Fact_sales.time_id=Time_dw.time_id) where Prod_name='Rice' and qt='Q1'; \n

    ### Roll Up Operation \n
    SELECT yr, SUM(total_sales) \n
    FROM (Fact_sales NATURAL JOIN  Product_dw) \n
    JOIN Time_dw ON Fact_sales.time_id=Time_dw.time_id \n
    WHERE Prod_name='Rice' GROUP BY yr; \n
    
    ###Drill Down Operation \n
    SELECT qt,SUM(total_sales) \n
    FROM (Fact_sales NATURAL JOIN  Product_dw) \n
    JOIN Time_dw ON Fact_sales.time_id=Time_dw.time_id \n
    WHERE Prod_name='Rice' GROUP BY qt; \n
    
    #####	Pivot Operation
        SELECT YR, [January], [February], [May], [June]
        FROM (Select YR, MONTH, QT
        FROM Time_dw as source_table  PIVOT
        (Max(Value)  For
        MONTH in ([January], [February], [May], [June]) as PIVOT_TABLE
        
        
        
    #### Ext 4 ############ \n
    
    from csv import reader   \n
        from random import seed   \n
        from random import randrange   \n
        from math import sqrt   \n
        from math import exp   \n
        from math import pi   \n
           \n
        # Load a CSV file   \n
        def load_csv(filename):   \n
        	dataset = list()   \n
        	with open(filename, 'r') as file:   \n
        		csv_reader = reader(file)   \n
        		for row in csv_reader:   \n
        			if not row:   \n
        				continue   \n
        			dataset.append(row)   \n
        	return dataset   \n
           \n
        # Convert string column to float   \n
        def str_column_to_float(dataset, column):   \n
        	for row in dataset:   \n
        		row[column] = float(row[column].strip())   \n
           \n
        # Convert string column to integer   \n
        def str_column_to_int(dataset, column):   \n
        	class_values = [row[column] for row in dataset]   \n
        	unique = set(class_values)   \n
        	lookup = dict()   \n
        	for i, value in enumerate(unique):   \n
        		lookup[value] = i   \n
        	for row in dataset:   \n
        		row[column] = lookup[row[column]]   \n
        	return lookup   \n
           \n
        # Split a dataset into k folds   \n
        def cross_validation_split(dataset, n_folds):   \n
        	dataset_split = list()   \n
        	dataset_copy = list(dataset)   \n
        	fold_size = int(len(dataset) / n_folds)   \n
        	for _ in range(n_folds):   \n
        		fold = list()   \n
        		while len(fold) < fold_size:   \n
        			index = randrange(len(dataset_copy))   \n
        			fold.append(dataset_copy.pop(index))   \n
        		dataset_split.append(fold)   \n
        	return dataset_split   \n
           \n
        # Calculate accuracy percentage   \n
        def accuracy_metric(actual, predicted):   \n
        	correct = 0   \n
        	for i in range(len(actual)):   \n
        		if actual[i] == predicted[i]:   \n
        			correct += 1   \n
        	return correct / float(len(actual)) * 100.0   \n
           \n
        # Evaluate an algorithm using a cross validation split   \n
        def evaluate_algorithm(dataset, algorithm, n_folds, *args):   \n
        	folds = cross_validation_split(dataset, n_folds)   \n
        	scores = list()   \n
        	for fold in folds:   \n
        		train_set = list(folds)   \n
        		train_set.remove(fold)   \n
        		train_set = sum(train_set, [])   \n
        		test_set = list()   \n
        		for row in fold:   \n
        			row_copy = list(row)   \n
        			test_set.append(row_copy)   \n
        			row_copy[-1] = None   \n
        		predicted = algorithm(train_set, test_set, *args)   \n
        		actual = [row[-1] for row in fold]   \n
        		accuracy = accuracy_metric(actual, predicted)   \n
        		scores.append(accuracy)   \n
        	return scores   \n
           \n
        # Split the dataset by class values, returns a dictionary   \n
        def separate_by_class(dataset):   \n
        	separated = dict()   \n
        	for i in range(len(dataset)):   \n
        		vector = dataset[i]   \n
        		class_value = vector[-1]   \n
        		if (class_value not in separated):   \n
        			separated[class_value] = list()   \n
        		separated[class_value].append(vector)   \n
        	return separated   \n
           \n
        # Calculate the mean of a list of numbers   \n
        def mean(numbers):   \n
        	return sum(numbers)/float(len(numbers))   \n
           \n
        # Calculate the standard deviation of a list of numbers   \n
        def stdev(numbers):   \n
        	avg = mean(numbers)   \n
        	variance = sum([(x-avg)**2 for x in numbers]) / float(len(numbers)-1)   \n
        	return sqrt(variance)   \n
           \n
        # Calculate the mean, stdev and count for each column in a dataset   \n
        def summarize_dataset(dataset):   \n
        	summaries = [(mean(column), stdev(column), len(column)) for column in zip(*dataset)]   \n
        	del(summaries[-1])   \n
        	return summaries   \n
           \n
        # Split dataset by class then calculate statistics for each row   \n
        def summarize_by_class(dataset):   \n
        	separated = separate_by_class(dataset)   \n
        	summaries = dict()   \n
        	for class_value, rows in separated.items():   \n
        		summaries[class_value] = summarize_dataset(rows)   \n
        	return summaries   \n
           \n
        # Calculate the Gaussian probability distribution function for x   \n
        def calculate_probability(x, mean, stdev):   \n
        	exponent = exp(-((x-mean)**2 / (2 * stdev**2 )))   \n
        	return (1 / (sqrt(2 * pi) * stdev)) * exponent   \n
           \n
        # Calculate the probabilities of predicting each class for a given row   \n
        def calculate_class_probabilities(summaries, row):   \n
        	total_rows = sum([summaries[label][0][2] for label in summaries])   \n
        	probabilities = dict()   \n
        	for class_value, class_summaries in summaries.items():   \n
        		probabilities[class_value] = summaries[class_value][0][2]/float(total_rows)   \n
        		for i in range(len(class_summaries)):   \n
        			mean, stdev, _ = class_summaries[i]   \n
        			probabilities[class_value] *= calculate_probability(row[i], mean, stdev)   \n
        	return probabilities   \n
           \n
        # Predict the class for a given row   \n
        def predict(summaries, row):   \n
        	probabilities = calculate_class_probabilities(summaries, row)   \n
        	best_label, best_prob = None, -1   \n
        	for class_value, probability in probabilities.items():   \n
        		if best_label is None or probability > best_prob:   \n
        			best_prob = probability   \n
        			best_label = class_value   \n
        	return best_label   \n
           \n
        # Naive Bayes Algorithm   \n
        def naive_bayes(train, test):   \n
        	summarize = summarize_by_class(train)   \n
        	predictions = list()   \n
        	for row in test:   \n
        		output = predict(summarize, row)   \n
        		predictions.append(output)   \n
        	return(predictions)   \n
           \n
        # Test Naive Bayes on Iris Dataset   \n
        seed(1)   \n
        filename = 'iris.csv'   \n
        dataset = load_csv(filename)   \n
        for i in range(len(dataset[0])-1):   \n
        	str_column_to_float(dataset, i)   \n
        # convert class column to integers   \n
        str_column_to_int(dataset, len(dataset[0])-1)   \n
        # evaluate algorithm   \n
        n_folds = 5   \n
        scores = evaluate_algorithm(dataset, naive_bayes, n_folds)   \n
        print('Scores: %s' % scores)   \n
        print('Mean Accuracy: %.3f%%' % (sum(scores)/float(len(scores))))   \n
           \n
           \n
        #Output   \n
           \n
        Scores: [93.33333333333333, 96.66666666666667, 100.0, 93.33333333333333, 93.33333333333333]   \n
        Mean Accuracy: 95.333%   \n



        ##### Expt 5 ########### \n
        
        # Implementation of Binning by means technique \n
        import numpy as np  \n
        from sklearn.linear_model import LinearRegression  \n
        from sklearn import linear_model  \n
        # import statsmodels.api as sm  \n
        import statistics  \n
        import math  \n
        from collections import OrderedDict  \n
          \n
        x =[]  \n
        print("enter the data")  \n
        x = list(map(float, input().split()))  \n
          \n
        print("enter the number of bins")  \n
        bi = int(input())  \n
          \n
        # X_dict will store the data in sorted order  \n
        X_dict = OrderedDict()  \n
        # x_old will store the original data  \n
        x_old ={}  \n
        # x_new will store the data after binning  \n
        x_new ={}  \n
          \n
          \n
        for i in range(len(x)):  \n
        	X_dict[i]= x[i]  \n
        	x_old[i]= x[i]  \n
          \n
        x_dict = sorted(X_dict.items(), key = lambda x: x[1])  \n
          \n
        # list of lists(bins)  \n
        binn =[]  \n
        # a variable to find the mean of each bin  \n
        avrg = 0  \n
        i = 0  \n
        k = 0  \n
        num_of_data_in_each_bin = int(math.ceil(len(x)/bi))  \n
          \n
        # performing binning  \n
        for g, h in X_dict.items():  \n
        	if(i<num_of_data_in_each_bin):  \n
        		avrg = avrg + h  \n
        		i = i + 1  \n
        	elif(i == num_of_data_in_each_bin):  \n
        		k = k + 1  \n
        		i = 0  \n
        		binn.append(round(avrg / num_of_data_in_each_bin, 3))  \n
        		avrg = 0  \n
        		avrg = avrg + h  \n
        		i = i + 1  \n
        rem = len(x)% bi  \n
        if(rem == 0):  \n
        	binn.append(round(avrg / num_of_data_in_each_bin, 3))  \n
        else:  \n
        	binn.append(round(avrg / rem, 3))  \n
          \n
        # store the new value of each data  \n
        i = 0  \n
        j = 0  \n
        for g, h in X_dict.items():  \n
        	if(i<num_of_data_in_each_bin):  \n
        		x_new[g]= binn[j]  \n
        		i = i + 1  \n
        	else:  \n
        		i = 0  \n
        		j = j + 1  \n
        		x_new[g]= binn[j]  \n
        		i = i + 1  \n
        print("number of data in each bin")  \n
        print(math.ceil(len(x)/bi))  \n
          \n
        for i in range(0, len(x)):  \n
        	print('index {2} old value {0} new value {1}'.format(x_old[i], x_new[i], i))  \n
          \n
        # Output  \n
          \n
        enter the data  \n
        10 5 9 8 3 2 14 20 33 19 20  \n
        enter the number of bins  \n
        3  \n
        number of data in each bin  \n
        4  \n
        index 0 old value 10.0 new value 8.0  \n
        index 1 old value 5.0 new value 8.0  \n
        index 2 old value 9.0 new value 8.0  \n
        index 3 old value 8.0 new value 8.0  \n
        index 4 old value 3.0 new value 9.75  \n
        index 5 old value 2.0 new value 9.75  \n
        index 6 old value 14.0 new value 9.75  \n
        index 7 old value 20.0 new value 9.75  \n
        index 8 old value 33.0 new value 36.0  \n
        index 9 old value 19.0 new value 36.0  \n
        index 10 old value 20.0 new value 36.0  \n

        # Implementation of Visualization technique ( BoxPlot )   \n
           \n
        # Import libraries   \n
        import matplotlib.pyplot as plt   \n
        import numpy as np   \n
           \n
        # Creating dataset   \n
        np.random.seed(10)   \n
           \n
        data_1 = np.random.normal(100, 10, 200)   \n
        data_2 = np.random.normal(90, 20, 200)   \n
        data_3 = np.random.normal(80, 30, 200)   \n
        data_4 = np.random.normal(70, 40, 200)   \n
        data = [data_1, data_2, data_3, data_4]   \n
           \n
        fig = plt.figure(figsize =(10, 7))   \n
           \n
        # Creating axes instance   \n
        ax = fig.add_axes([0, 0, 1, 1])   \n
           \n
        # Creating plot   \n
        bp = ax.boxplot(data)   \n
           \n
        # show plot   \n
        plt.show()   \n


    ##### K-Means Clustering ######   \n
        ## Implementation of K-means Clustering Algorithm
        ## Initialisation    \n
        import pandas as pd    \n
        import numpy as np    \n
        import matplotlib.pyplot as plt    \n
            \n
        df = pd.DataFrame({    \n
            'x': [12, 20, 28, 18, 29, 33, 24, 45, 45, 52, 51, 52, 55, 53, 55, 61, 64, 69, 72],    \n
            'y': [39, 36, 30, 52, 54, 46, 55, 59, 63, 70, 66, 63, 58, 23, 14, 8, 19, 7, 24]    \n
        })    \n
        np.random.seed(200)    \n
        k = 3    \n
        # centroids[i] = [x, y]    \n
        centroids = {    \n
            i+1: [np.random.randint(0, 80), np.random.randint(0, 80)]    \n
            for i in range(k)    \n
        }    \n
        fig = plt.figure(figsize=(5, 5))    \n
        plt.scatter(df['x'], df['y'], color='k')    \n
        colmap = {1: 'r', 2: 'g', 3: 'b'}    \n
        for i in centroids.keys():    \n
            plt.scatter(*centroids[i], color=colmap[i])    \n
        plt.xlim(0, 80)    \n
        plt.ylim(0, 80)    \n
        plt.show()    \n
        ## Assignment Stage    \n
        def assignment(df, centroids):    \n
            for i in centroids.keys():    \n
                # sqrt((x1 - x2)^2 - (y1 - y2)^2)    \n
                df['distance_from_{}'.format(i)] = (    \n
                    np.sqrt(    \n
                        (df['x'] - centroids[i][0]) ** 2    \n
                        + (df['y'] - centroids[i][1]) ** 2    \n
                    )    \n
                )    \n
            centroid_distance_cols = ['distance_from_{}'.format(i) for i in centroids.keys()]    \n
            df['closest'] = df.loc[:, centroid_distance_cols].idxmin(axis=1)    \n
            df['closest'] = df['closest'].map(lambda x: int(x.lstrip('distance_from_')))    \n
            df['color'] = df['closest'].map(lambda x: colmap[x])    \n
            return df    \n
        df = assignment(df, centroids)    \n
        print(df.head())    \n
        fig = plt.figure(figsize=(5, 5))    \n
        plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.5, edgecolor='k')    \n
        for i in centroids.keys():    \n
         plt.scatter(*centroids[i], color=colmap[i])    \n
        plt.xlim(0, 80)    \n
        plt.ylim(0, 80)    \n
        plt.show()    \n
            \n
        ## Update Stage    \n
        import copy    \n
        old_centroids = copy.deepcopy(centroids)    \n
        def update(k):    \n
            for i in centroids.keys():    \n
                centroids[i][0] = np.mean(df[df['closest'] == i]['x'])    \n
                centroids[i][1] = np.mean(df[df['closest'] == i]['y'])    \n
            return k    \n
            \n
        centroids = update(centroids)    \n
        fig = plt.figure(figsize=(5, 5))    \n
        ax = plt.axes()    \n
        plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.5, edgecolor='k')    \n
        for i in centroids.keys():    \n
        plt.scatter(*centroids[i], color=colmap[i])    \n
        plt.xlim(0, 80)    \n
        plt.ylim(0, 80)    \n
        for i in old_centroids.keys():    \n
            old_x = old_centroids[i][0]    \n
            old_y = old_centroids[i][1]    \n
        dx = (centroids[i][0] - old_centroids[i][0]) * 0.75    \n
            dy = (centroids[i][1] - old_centroids[i][1]) * 0.75    \n
            ax.arrow(old_x, old_y, dx, dy, head_width=2, head_length=3, fc=colmap[i], ec=colmap[i])    \n
        plt.show()    \n
            \n
        ## Repeat Assigment Stage    \n
        df = assignment(df, centroids)    \n
        # Plot results    \n
        fig = plt.figure(figsize=(5, 5))    \n
        plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.5, edgecolor='k')    \n
        for i in centroids.keys():    \n
            plt.scatter(*centroids[i], color=colmap[i])    \n
        plt.xlim(0, 80)    \n
        plt.ylim(0, 80)    \n
        plt.show()    \n
        # Continue until all assigned categories don't change any more    \n
        while True:    \n
            closest_centroids = df['closest'].copy(deep=True)    \n
            centroids = update(centroids)    \n
            df = assignment(df, centroids)    \n
            if closest_centroids.equals(df['closest']):    \n
                break    \n
        fig = plt.figure(figsize=(5, 5))    \n
        plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.5, edgecolor='k')    \n
        for i in centroids.keys():    \n
        plt.scatter(*centroids[i], color=colmap[i])    \n
        plt.xlim(0, 80)    \n
        plt.ylim(0, 80)    \n
        plt.show()    \n
        
        
        
        
        # Implementation of Apriori Algorithm    \n
        # Tools used : Anaconda 3 , needs to install apyori library     \n
        # Dataset : Retail stores data with 7501 tuples    \n

        import numpy as np    \n
        import matplotlib.pyplot as plt    \n
        import pandas as pd    \n


        dataset = pd.read_csv('store_data.csv', header = None)     \n
        transactions = []    \n
        for i in range(0,7501):    \n
            transactions.append([str(dataset.values[i,j]) for j in range(0,20)])    \n


        from apyori import apriori    \n

        rules= apriori(transactions,    \n
                       min_support = 0.003,    \n
                       min_confidence = 0.2,    \n
                       min_lift = 3,    \n
                       min_length = 2)        \n

        MB = list(rules)    \n

        Result = [list(MB[i][0]) for i in range(0,len(MB))]    \n

        #print(Result)    \n

        for item in Result:    \n
            # first index of the inner list    \n
            # Contains base item and add item    \n
            pair = item[0]     \n
            items = [x for x in pair]    \n
            print("Rule: " + item[0] + " -> " + item[1])    \n

            #second index of the inner list    \n
            print("Support: " + str(item[1]))    \n

            #third index of the list located at 0th    \n
            #of the third index of the inner list    \n

            print("Confidence: " + str(item[1][2][0]))    \n
            print("Lift: " + str(item[1][2][0]))    \n
            print("=====================================")    \n
            
            
            


##### Hits Algorithm  #####   \n
# Implementation of Page Rank Algorithm   \n
# Tools used : Anaconda 3 jupyter   \n
   \n
import numpy as np   \n
from scipy.sparse import csc_matrix   \n
   \n
def pageRank(G, s = .85, maxerr = .0001):   \n
    "   \n
    Computes the pagerank for each of the n states   \n
   \n
    Parameters   \n
    ----------   \n
    G: matrix representing state transitions   \n
       Gij is a binary value representing a transition from state i to j.   \n
   \n
    s: probability of following a transition. 1-s probability of teleporting   \n
       to another state.   \n
   \n
    maxerr: if the sum of pageranks between iterations is bellow this we will   \n
            have converged.   \n
    "   \n
    n = G.shape[0]   \n
   \n
    # transform G into markov matrix A   \n
    A = csc_matrix(G,dtype=np.float)   \n
    rsums = np.array(A.sum(1))[:,0]   \n
    ri, ci = A.nonzero()   \n
    A.data /= rsums[ri]   \n
   \n
    # bool array of sink states   \n
    sink = rsums==0   \n
   \n
        # Compute pagerank r until we converge    \n
        ro, r = np.zeros(n), np.ones(n)  \n
        while np.sum(np.abs(r-ro)) > maxerr:  \n
            ro = r.copy()  \n
            # calculate each pagerank at a time  \n
            for i in range(0,n):  \n
                # inlinks of state i  \n
                Ai = np.array(A[:,i].todense())[:,0]  \n
                # account for sink states  \n
                Di = sink / float(n)  \n
                # account for teleportation to state i  \n
                Ei = np.ones(n) / float(n)  \n
      \n
                r[i] = ro.dot( Ai*s + Di*s + Ei*(1-s) )  \n
      \n
        # return normalized pagerank  \n
        return r/float(sum(r))  \n
    if __name__=='__main__':  \n
        # Example extracted from 'Introduction to Information Retrieval'  \n
        G = np.array([[0,0,1,0,0,0,0],  \n
                      [0,1,1,0,0,0,0],  \n
                      [1,0,1,1,0,0,0],  \n
                      [0,0,0,1,1,0,0],  \n
                      [0,0,0,0,0,0,1],  \n
                      [0,0,0,0,0,1,1],  \n
                      [0,0,0,1,1,0,1]])  \n
        print(pageRank(G,s=.86))  \n
          \n
          \n
    #Output  \n
    Ranks of each Connected Page  \n
    [0.12727557 0.03616954 0.12221594 0.22608452 0.28934412 0.03616954  \n
     0.16274076]  \n
      \n
      \n
      \n
      \n
     #  Implementation of HITS algorithm.  \n
      \n
    # Implementation of HITS algorithm   \n
    #Tools used : Anaconda 3  \n
    # importing modules   \n
    import networkx as nx   \n
    import matplotlib.pyplot as plt   \n
      \n
    G = nx.DiGarph()   \n
      \n
    G.add_edges_from([('A', 'D'), ('B', 'C'), ('B', 'E'), ('C', 'A'),   \n
    				('D', 'C'), ('E', 'D'), ('E', 'B'), ('E', 'F'),   \n
    				('E', 'C'), ('F', 'C'), ('F', 'H'), ('G', 'A'),   \n
    				('G', 'C'), ('H', 'A')])   \n
      \n
    plt.figure(figsize =(10, 10))   \n
    nx.draw_networkx(G, with_labels = True)   \n
      \n
    hubs, authorities = nx.hits(G, max_iter = 50, normalized = True)   \n
      \n
    # The in-built hits function returns two dictionaries keyed by nodes   \n
    # containing hub scores and authority scores respectively.   \n
      \n
    print("Hub Scores: ", hubs)   \n
    print("Authority Scores: ", authorities)  \n
      \n
      \n
    #Output  \n
      \n
    Hub Scores:  {'A': 0.04642540386472174, 'D': 0.133660375232863,  \n
                  'B': 0.15763599440595596, 'C': 0.037389132480584515,   \n
                  'E': 0.2588144594158868, 'F': 0.15763599440595596,  \n
                  'H': 0.037389132480584515, 'G': 0.17104950771344754}  \n
      \n
    Authority Scores:  {'A': 0.10864044085687284, 'D': 0.13489685393050574,   \n
                        'B': 0.11437974045401585, 'C': 0.3883728005172019,  \n
                        'E': 0.06966521189369385, 'F': 0.11437974045401585,  \n
                        'H': 0.06966521189369385, 'G': 0.0}  \n
    
"""
print(a)
# return a
