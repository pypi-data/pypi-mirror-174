from typing import List, Dict, Tuple, Any, Iterator
from random import Random

class DatasetReader:
    """An abstract class for reading data from some location and construction of a dataset."""


    def __init__(self, seed=None):
        self.data=None
        self.shuffle=False
        self.random = Random(seed)

    def read(self, data_path: str, *args, **kwargs) -> Dict[str, List[Tuple[Any, Any]]]:
        """Reads a file from a path and returns data as a list of tuples of inputs and correct outputs
         for every data type in ``train``, ``valid`` and ``test``.
        """
        raise NotImplementedError


    def get_instances(self, sub_set: str = 'train') -> Tuple[tuple, tuple]:
        """Get all data for a selected data type

        Args:
            sub_set (str): can be either ``'train'``, ``'test'``, ``'valid'`` or ``'all'``

        Returns:
             a tuple of all inputs for a data type and all expected outputs for a data type
        """
        if hasattr(self, "data"):
            data = self.data[sub_set]
            return tuple(zip(*data))


    def gen_batches(self, batch_size: int, data_type: str = 'train',
                    shuffle: bool = None) -> Iterator[Tuple[tuple, tuple]]:
        """Generate batches of inputs and expected output to train neural networks

        Args:
            batch_size: number of samples in batch
            data_type: can be either 'train', 'test', or 'valid'
            shuffle: whether to shuffle dataset before batching

        Yields:
             a tuple of a batch of inputs and a batch of expected outputs
        """
        if shuffle is None:
            shuffle = self.shuffle

        data = self.data[data_type]
        data_len = len(data)

        if data_len == 0:
            return

        order = list(range(data_len))
        if shuffle:
            self.random.shuffle(order)

        if batch_size < 0:
            batch_size = data_len

        for i in range((data_len - 1) // batch_size + 1):
            yield tuple(zip(*[data[o] for o in order[i * batch_size:(i + 1) * batch_size]]))

