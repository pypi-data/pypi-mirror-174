# from hello import exp3
# from hello import exp2
# from hello import exp4
# from hello import kmeans
# from hello import naive
# from hello import association
# from hello import pagerank

def exp3():
    print(
        '''
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt

        dataset = pd.read_csv("Data.csv")

        x= dataset.iloc[:,:-1].values
        y= dataset.iloc[:,-1].values
        print(y)
        print(x)

        print(dataset)

        from sklearn.impute import SimpleImputer
        imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
        imputer.fit(x[:,1:3])
        x[:,1:3]=imputer.transform(x[:,1:3])

        """# New Section"""

        print(x)

        from sklearn.compose import ColumnTransformer
        from sklearn.preprocessing import OneHotEncoder
        ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [0])], remainder='passthrough')
        x = np.array(ct.fit_transform(x))

        print(X)

        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        y = np.array(le.fit_transform(y))

        print(y)

        dataset['Age'].describe()

        from sklearn.model_selection import train_test_split
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 1)

        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        x_train[:, 3:] = sc.fit_transform(x_train[:, 3:])
        x_test[:, 3:] = sc.transform(x_test[:, 3:])

        print(x_test)

        from sklearn.tree import DecisionTreeClassifier
        classifier = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
        classifier.fit(x_train, y_train)

        x_predict = np.array(x_test[:,:])
        print(classifier.predict((x_predict)))

        accuracy = classifier.score(x_test,y_test)
        print(accuracy)

        print(y_test)
        '''
    )


def exp4():
    print(
        '''
        import pandas as pd
        import seaborn as sb
        import matplotlib.pyplot as plt

        iris_d = sb.load_dataset("iris")

        iris_d.head()

        iris_d.shape

        plt.scatter(iris_d['petal_length'],iris_d['petal_width'], color='red')
        plt.title("scatter plot")
        plt.xlabel("petal length")
        plt.ylabel("petal width")
        plt.show()

        plt.hist(iris_d['sepal_width'], bins=20)
        plt.title("Histogram")
        plt.xlabel("Sepal width")
        plt.ylabel("Frequency")
        plt.show()

        plt.hist(iris_d['petal_width'], bins=10)
        plt.title("Histogram")
        plt.xlabel("Petal width")
        plt.ylabel("Frequency")
        plt.show()

        sb.boxplot(x="sepal_width", data=iris_d)
        plt.title("Box Plot")

        sb.boxplot(x="sepal_length", data=iris_d)
        plt.title("Box Plot")
        '''
    )

def naive():
    print(
        '''
        import numpy as np
        import pandas as pd

        dataset = pd.read_csv('Social_Network_Ads.csv')
        X = dataset.iloc[:, :-1].values
        y = dataset.iloc[:, -1].values

        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

        print(X_train)

        print(y_train)

        print(X_test)

        print(y_test)

        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)

        from sklearn.naive_bayes import GaussianNB
        classifier = GaussianNB()
        classifier.fit(X_train, y_train)

        print(classifier.predict(sc.transform([[25,100000]])))

        print(classifier.predict(sc.transform([[25,150000]])))

        y_pred = classifier.predict(X_test)

        from sklearn.metrics import confusion_matrix, accuracy_score
        cm = confusion_matrix(y_test, y_pred)
        print(cm)
        accuracy_score(y_test, y_pred)
        '''
    )

def kmeans():
    print(
        '''
        import numpy as np
        import matplotlib.pyplot as plt
        import pandas as pd

        dataset = pd.read_csv('Mall_Customers.csv')
        X = dataset.iloc[:, [3, 4]].values

        from sklearn.cluster import KMeans
        wcss = []
        for i in range(1, 11):
            kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
            kmeans.fit(X)
            wcss.append(kmeans.inertia_)
        plt.plot(range(1, 11), wcss)
        plt.title('The Elbow Method')
        plt.xlabel('Number of clusters')
        plt.ylabel('WCSS')
        plt.show()

        kmeans = KMeans(n_clusters = 5, init = 'k-means++', random_state = 42)
        y_kmeans = kmeans.fit_predict(X)

        plt.scatter(X[y_kmeans == 0, 0], X[y_kmeans == 0, 1], s = 10, c = 'red', label = 'Cluster 1')
        plt.scatter(X[y_kmeans == 1, 0], X[y_kmeans == 1, 1], s = 100, c = 'blue', label = 'Cluster 2')
        plt.scatter(X[y_kmeans == 2, 0], X[y_kmeans == 2, 1], s = 100, c = 'green', label = 'Cluster 3')
        plt.scatter(X[y_kmeans == 3, 0], X[y_kmeans == 3, 1], s = 100, c = 'cyan', label = 'Cluster 4')
        plt.scatter(X[y_kmeans == 4, 0], X[y_kmeans == 4, 1], s = 100, c = 'magenta', label = 'Cluster 5')
        plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s = 300, c = 'yellow', label = 'Centroids')
        plt.title('Clusters of customers')
        plt.xlabel('Annual Income (k$)')
        plt.ylabel('Spending Score (1-100)')
        plt.legend()
        plt.show()
        '''
    )

def association():
    print(
        '''
        import numpy as np
        import matplotlib.pyplot as plt
        import pandas as pd

        dataset = pd.read_csv('Market_Basket_Optimisation.csv', header = None)
        transactions = []
        for i in range(0, 7501):
        transactions.append([str(dataset.values[i,j]) for j in range(0, 20)])

        dataset

        transactions

        !pip install apyori

        from apyori import apriori
        rules = apriori(transactions = transactions, min_support = 0.003, min_confidence = 0.2)

        results = list(rules)

        results
        '''
    )

def exp2():
    print(
        '''
        select p.product_name,  t.quarter, b.branchname, sum(s.total_sales) as 'total sales', sum(s.profit) as 'profit' 
        from product p, sales s, time t, branch b
        where p.product_id= s.prod_id and t.time_id = s.time_id and b.branchid = s.branch_id
        group by p.product_name, t.quarter, b.branchname


        select p.product_name, sum(s.total_sales) as 'total sales', t.quarter, b.branchname
        from product p, sales s, time t, branch b
        where p.product_id= s.prod_id and t.time_id = s.time_id and b.branchid = s.branch_id and quarter=2
        group by p.product_name, t.quarter, b.branchname

        select p.product_name, sum(s.total_sales) as 'total sales', t.quarter, b.branchname
        from product p, sales s, time t, branch b
        where p.product_id= s.prod_id and t.time_id = s.time_id and b.branchid = s.branch_id and quarter=2 and branch_id=1
        group by p.product_name, t.quarter, b.branchname

        select t.year, sum(s.total_sales) as 'total sales'
        from sales s, time t
        where t.time_id = s.time_id 
        group by t.year

        select t.month, sum(s.total_sales) as 'total sales'
        from sales s, time t
        where t.time_id = s.time_id 
        group by t.month
        '''
    )

def pagerank():
    print(
        '''
        import java.util.*;
        import java.io.*;
        public class PageRank {
        public int path[][] = new int[10][10];
        public double pagerank[] = new double[10];

        public void calc(double totalNodes) {

        double InitialPageRank;

        double OutgoingLinks = 0;

        double DampingFactor = 0.85;

        double TempPageRank[] = new double[10];

        int ExternalNodeNumber;

        int InternalNodeNumber;

        int k = 1; // For Traversing

        int ITERATION_STEP = 1;

        InitialPageRank = 1 / totalNodes;

        System.out.printf(" Total Number of Nodes :" + totalNodes + "\t Initial PageRank  of All Nodes :" + InitialPageRank + "\n");

        // 0th ITERATION  _ OR _ INITIALIZATION PHASE //

        for (k = 1; k <= totalNodes; k++) {

        this.pagerank[k] = InitialPageRank;

        }

        System.out.printf("\n Initial PageRank Values , 0th Step \n");

        for (k = 1; k <= totalNodes; k++) {

        System.out.printf(" Page Rank of " + k + " is :\t" + this.pagerank[k] + "\n");

        }

        while (ITERATION_STEP <= 2) // Iterations

        {

        // Store the PageRank for All Nodes in Temporary Array

        for (k = 1; k <= totalNodes; k++) {

            TempPageRank[k] = this.pagerank[k];

            this.pagerank[k] = 0;

        }

        for (InternalNodeNumber = 1; InternalNodeNumber <= totalNodes; InternalNodeNumber++) {

            for (ExternalNodeNumber = 1; ExternalNodeNumber <= totalNodes; ExternalNodeNumber++) {

            if (this.path[ExternalNodeNumber][InternalNodeNumber] == 1) {

            k = 1;

            OutgoingLinks = 0; // Count the Number of Outgoing Links for each ExternalNodeNumber

            while (k <= totalNodes) {

            if (this.path[ExternalNodeNumber][k] == 1) {

                OutgoingLinks = OutgoingLinks + 1; // Counter for Outgoing Links

            }

            k = k + 1;

            }

            // Calculate PageRank    

            this.pagerank[InternalNodeNumber] += TempPageRank[ExternalNodeNumber] * (1 / OutgoingLinks);

            }

            }

        }

        System.out.printf("\n After " + ITERATION_STEP + "th Step \n");

        for (k = 1; k <= totalNodes; k++)

            System.out.printf(" Page Rank of " + k + " is :\t" + this.pagerank[k] + "\n");

        ITERATION_STEP = ITERATION_STEP + 1;

        }

        // Add the Damping Factor to PageRank

        for (k = 1; k <= totalNodes; k++) {

        this.pagerank[k] = (1 - DampingFactor) + DampingFactor * this.pagerank[k];

        }

        // Display PageRank

        System.out.printf("\n Final Page Rank : \n");

        for (k = 1; k <= totalNodes; k++) {

        System.out.printf(" Page Rank of " + k + " is :\t" + this.pagerank[k] + "\n");

        }

        }

        public static void main(String args[]) {

        int nodes, i, j, cost;

        Scanner in = new Scanner(System.in);

        System.out.println("Enter the Number of WebPages \n");

        nodes = in .nextInt();

        PageRank p = new PageRank();

        System.out.println("Enter the Adjacency Matrix with 1->PATH & 0->NO PATH Between two WebPages: \n");

        for (i = 1; i <= nodes; i++)

        for (j = 1; j <= nodes; j++) {

            p.path[i][j] = in .nextInt();

            if (j == i)

            p.path[i][j] = 0;

        }

        p.calc(nodes);

        }

        }
        '''
    )

    
