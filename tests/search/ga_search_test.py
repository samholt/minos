'''
Created on Feb 15, 2017

@author: julien
'''
import tempfile
import unittest

from minos.experiment.experiment import Experiment, ExperimentParameters
from minos.experiment.ga import run_ga_search_experiment
from minos.experiment.training import Training, EpochStoppingCondition
from minos.model.model import Layout, Objective, Metric, Optimizer
from minos.train.utils import CpuEnvironment
from tests.fixtures import get_reuters_dataset


class GaSearchTest(unittest.TestCase):

    def test_ga_search(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            batch_size = 50
            batch_iterator, test_batch_iterator, nb_classes = get_reuters_dataset(batch_size, 1000)
            layout = Layout(
                input_size=1000,
                output_size=nb_classes,
                output_activation='softmax')
            training = Training(
                objective=Objective('categorical_crossentropy'),
                optimizer=Optimizer(optimizer='Adam'),
                metric=Metric('categorical_accuracy'),
                stopping=EpochStoppingCondition(10),
                batch_size=batch_size)
            experiment_parameters = ExperimentParameters(use_default_values=False)
            experiment_parameters.layout_parameter('rows', 2)
            experiment_parameters.layout_parameter('blocks', 3)
            experiment_parameters.layout_parameter('layers', 5)
            experiment = Experiment(
                'test__reuters_experiment',
                layout,
                training,
                batch_iterator,
                test_batch_iterator,
                CpuEnvironment(n_jobs=2, data_dir=tmp_dir),
                parameters=experiment_parameters)
            run_ga_search_experiment(experiment)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()