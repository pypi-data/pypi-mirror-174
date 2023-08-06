import jupyhai
from jupyhai.handlers.base import JupyhaiHandler


class HelloHandler(JupyhaiHandler):
    def get(self) -> None:
        self.finish(
            {
                "version": jupyhai.__version__,
            }
        )
