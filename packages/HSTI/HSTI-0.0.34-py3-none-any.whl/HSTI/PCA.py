import numpy as np

class PCA:
    def __init__(self):
        self.loadings = 0
        self.scores = 0
        self.singular_values = 0
        self.expl_var_ratio = 0

    #Calculates the PCA of a matrix with each column representing a variable, and the samples represented by the rows.
    def calculate_pca(self, array_2D):
        cov = np.cov(array_2D.T)
        self.singular_values, self.loadings = np.linalg.eig(cov)
        self.singular_values = np.real(self.singular_values)
        self.loadings = np.real(self.loadings)
        index = self.singular_values.argsort()[::-1] #make sure the singular values are in decending order as well as the loadings
        self.singular_values = self.singular_values[index]
        self.loadings = self.loadings[:,index] #sort the loadings the same way as the singular values
        self.expl_var_ratio = self.singular_values/np.sum(self.singular_values) #calculate the percentage of explained variance for each of the eigen values - this corresponds to the contribution of each PC
        self.scores = array_2D @ self.loadings

    def apply_pca(self, array_2D):
        return array_2D @ self.loadings
