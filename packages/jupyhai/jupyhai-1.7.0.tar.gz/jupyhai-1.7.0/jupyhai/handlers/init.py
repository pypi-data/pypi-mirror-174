import os

from notebook.notebookapp import NotebookApp
from notebook.utils import url_path_join
from valohai_cli.settings import settings

from jupyhai import consts
from jupyhai.handlers.environments import EnvironmentsHandler
from jupyhai.handlers.events import EventsHandler
from jupyhai.handlers.execute import ExecuteHandler
from jupyhai.handlers.execution_url import ExecutionUrlWithTokenHandler
from jupyhai.handlers.executions import ExecutionsHandler
from jupyhai.handlers.hello import HelloHandler
from jupyhai.handlers.images import ImagesHandler
from jupyhai.handlers.login import LoginHandler
from jupyhai.handlers.logout import LogoutHandler
from jupyhai.handlers.notebook_download import NotebookDownloadHandler
from jupyhai.handlers.output_download import OutputDownloadURLHandler
from jupyhai.handlers.outputs import OutputsHandler
from jupyhai.handlers.prepare import PrepareHandler
from jupyhai.handlers.projects import ProjectsHandler
from jupyhai.handlers.settings import SettingsHandler
from jupyhai.handlers.stop import StopHandler
from jupyhai.utils.api import configure_user_agent_header
from jupyhai.utils.auth import do_environment_login


def prepare(nb_server_app: NotebookApp) -> None:
    configure_user_agent_header()
    install_handlers(nb_server_app)

    if consts.NOTEBOOK_INSTANCE_ID:
        nb_server_app.log.info(
            'Jupyhai: Detected hosted notebook mode, updating login information...'
        )
        do_environment_login(nb_server_app.log)

    if consts.PROJECT_ID:
        nb_server_app.log.info(
            "Jupyhai: Using forced project ID %s" % consts.PROJECT_ID
        )
        settings.set_override_project(
            project_id=consts.PROJECT_ID, directory=consts.ROOT_DIRECTORY, mode="local"
        )


def install_handlers(nb_server_app: NotebookApp) -> None:
    web_app = nb_server_app.web_app
    base_url = web_app.settings['base_url']
    root_dir = os.path.expanduser(web_app.settings['server_root_dir'])
    handlers = [
        ('/jupyhai/hello', HelloHandler),
        ('/jupyhai/login', LoginHandler),
        ('/jupyhai/logout', LogoutHandler),
        ('/jupyhai/settings', SettingsHandler),
        ('/jupyhai/executions', ExecutionsHandler),
        ('/jupyhai/executions/(.*)', ExecutionsHandler),
        ('/jupyhai/executions', ExecutionsHandler),
        ('/jupyhai/execution-url-with-token/(.*)', ExecutionUrlWithTokenHandler),
        ('/jupyhai/events/(.*)', EventsHandler),
        ('/jupyhai/outputs/(.*)', OutputsHandler),
        ('/jupyhai/output/(.*)', OutputDownloadURLHandler),
        ('/jupyhai/projects', ProjectsHandler),
        ('/jupyhai/projects/(.*)', ProjectsHandler),
        ('/jupyhai/environments', EnvironmentsHandler),
        ('/jupyhai/environments/(.*)', EnvironmentsHandler),
        ('/jupyhai/images/(.*)', ImagesHandler),
        ('/jupyhai/notebook_download/(.*)', NotebookDownloadHandler, {'root_dir': root_dir}),
        ('/jupyhai/stop/(.*)', StopHandler),
        ('/jupyhai/prepare', PrepareHandler, {'root_dir': root_dir}),
        ('/jupyhai/execute', ExecuteHandler, {'root_dir': root_dir}),
    ]
    web_app.add_handlers('.*$', [(url_path_join(base_url, url), *rest) for url, *rest in handlers])
