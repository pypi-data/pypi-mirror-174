import dataclasses
import logging
import statistics
import time
import typing
import torch
import irisml.core
from irisml.tasks.train.build_dataloader import build_dataloader

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Benchmark a given model using a given dataset."""
    VERSION = '0.1.0'
    CACHE_ENABLED = False

    @dataclasses.dataclass
    class Inputs:
        model: torch.nn.Module
        dataset: torch.utils.data.Dataset
        transform: typing.Callable

    @dataclasses.dataclass
    class Config:
        batch_size: int
        device: typing.Optional[typing.Literal['cpu', 'cuda']] = None
        num_iterations: int = 10

    @dataclasses.dataclass
    class Outputs:
        forward_backward_time_per_iteration: float = 0.0
        forward_time_per_iteration: float = 0.0
        backward_time_per_iteration: float = 0.0
        prediction_time_per_iteration: float = 0.0
        max_cuda_memory_in_mb: float = 0.0

    def execute(self, inputs):
        device = self._get_device()
        dataloader = build_dataloader(inputs.dataset, inputs.transform, batch_size=self.config.batch_size, shuffle=False, drop_last=False)
        forward_time_all = []
        backward_time_all = []
        prediction_time_all = []

        model = inputs.model.to(device)
        model.train()

        if device.type == 'cuda':
            torch.cuda.reset_peak_memory_stats(device)
            cuda_memory_at_start = torch.cuda.memory_allocated(device)

        # Measure training forward and backward pass
        for i, batch in enumerate(dataloader):
            inputs, targets = batch
            inputs = self._to_device(inputs, device)
            targets = self._to_device(targets, device)
            forward_time, backward_time = self._training_step(model, inputs, targets)
            forward_time_all.append(forward_time)
            backward_time_all.append(backward_time)
            if i >= self.config.num_iterations:
                break

        model.eval()
        # Measure prediction time.
        for i, batch in enumerate(dataloader):
            inputs, targets = batch
            inputs = self._to_device(inputs, device)
            prediction_time_all.append(self._prediction_step(model, inputs))
            if i >= self.config.num_iterations:
                break

        if len(forward_time_all) < self.config.num_iterations:
            logger.info(f"The dataset is smaller than expected. The actual number of iteration is {len(forward_time_all)}")

        forward_time_per_iteration = statistics.fmean(forward_time_all)
        backward_time_per_iteration = statistics.fmean(backward_time_all)
        forward_backward_time_per_iteration = forward_time_per_iteration + backward_time_per_iteration
        prediction_time_per_iteration = statistics.fmean(prediction_time_all)
        max_cuda_memory_in_mb = ((torch.cuda.max_memory_allocated(device) - cuda_memory_at_start) / 2 ** 20) if device.type == 'cuda' else 0

        logger.info(f"{forward_time_per_iteration=}, {backward_time_per_iteration=}, {forward_backward_time_per_iteration=}, {prediction_time_per_iteration=}")
        if max_cuda_memory_in_mb > 0:
            logger.info(f"{max_cuda_memory_in_mb=}")

        return self.Outputs(forward_backward_time_per_iteration, forward_time_per_iteration, backward_time_per_iteration, prediction_time_per_iteration, max_cuda_memory_in_mb)

    def _get_device(self) -> torch.device:
        """Get a torch device based on the configuration. If not specified explicitly, it uses cuda if available."""
        if self.config.device:
            device_name = self.config.device
        else:
            device_name = 'cuda' if torch.cuda.is_available() else 'cpu'
            logger.info(f"Training device is selected automatically: {device_name}. To specify the device manually, please set Config.device.")

        return torch.device(device_name)

    def _to_device(self, data, device):
        if isinstance(data, list):
            return [self._to_device(d) for d in data]
        elif isinstance(data, tuple):
            return tuple(self._to_device(d) for d in data)
        elif hasattr(data, 'to'):
            return data.to(device, non_blocking=True)
        return data

    @staticmethod
    def _synchronize(device):
        if device.type == 'cuda':
            torch.cuda.synchronize()

    def _training_step(self, model, inputs, targets):
        self._synchronize(inputs.device)

        start = time.time()
        if hasattr(model, 'training_step'):
            loss = model.training_step(inputs, targets)['loss']
        else:
            loss = model.criterion(model(inputs), targets)

        self._synchronize(inputs.device)
        forward_time = time.time() - start

        start = time.time()
        loss.backward()
        self._synchronize(inputs.device)
        backward_time = time.time() - start

        return forward_time, backward_time

    def _prediction_step(self, model, inputs):
        self._synchronize(inputs.device)
        start = time.time()
        if hasattr(model, 'prediction_step'):
            model.prediction_step(inputs)
        elif hasattr(model, 'predictor'):
            model.predictor(model(inputs))
        else:
            model(inputs)
        self._synchronize(inputs.device)
        return time.time() - start
