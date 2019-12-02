from learner import get_data
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from sklearn.tree import export_graphviz
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA

X_train, X_test, y_train, y_test = get_data()

pca = PCA(n_components=10)
pca.fit(X_train)
print(pca.explained_variance_ratio_)

exit(0)

rf = RandomForestClassifier(max_depth=5, n_estimators=10)
rf.fit(X_train, y_train)

print(rf.score(X_test, y_test))

estimator = rf.estimators_[5]

export_graphviz(estimator, out_file='tree.dot')

# Convert to png using system command (requires Graphviz)
from subprocess import call
call(['dot', '-Tpng', 'tree.dot', '-o', 'tree.png', '-Gdpi=600'])

# Display in jupyter notebook
from IPython.display import Image
Image(filename = 'tree.png')