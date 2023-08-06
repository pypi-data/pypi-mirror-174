import numpy as np
from vidis_algorithms_api import Task


class Algorithm(Task):
    def run(self, hyperspecter: np.ndarray, **kwargs) -> np.ndarray:
        return np.zeros(hyperspecter.shape)

    def get_type_name(self) -> str:
        """
        Should return plain string contains a name of the algorithm.
        Just try not to use names which may already be taken (e.g. pca, kmeans)
        :return:
        """
        return 'test'


if __name__ == '__main__':
    alg = Algorithm()
    print(alg.get_type_name())
    alg.serve()
