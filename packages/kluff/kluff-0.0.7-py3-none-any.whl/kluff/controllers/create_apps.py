import os
import sys
import shutil
from cement.utils.version import get_version_banner
from ..core.version import get_version
from cement import Controller, ex
from ..utils.utils import CommandError

VERSION_BANNER = """
Build and Deploy with Kluff %s
%s
""" % (get_version(), get_version_banner())


class AppSetup(Controller):
    class Meta:
        label = 'items'
        stacked_type = 'embedded'
        stacked_on = 'base'

    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()

    @ex(
        help='create plugin',
        arguments=[
            (['plugin_name'], 
                            {'help': 'plugin name'}
            ),

            ( ['--language'],
                            {'help': 'Backend language i.e Python, Go, Javascript'}
            ),
        ],
    )
    def create(self):
        plugin_name = self.app.pargs.plugin_name
        language = self.app.pargs.language or 'python'
        self.app.log.info(f'creating plugin {plugin_name} using language {language}')
        try:
            templates = self.app.config.get('kluff', 'templates')
            backend_template = os.path.join(templates, language)
            frontend_template = os.path.join(templates, 'react')
            target_backend_app = os.path.join(os.getcwd(), plugin_name, 'backend')
            target_frontend_app = os.path.join(os.getcwd(), plugin_name, 'frontend')
            shutil.copytree(backend_template, target_backend_app, dirs_exist_ok=True)
            shutil.copytree(frontend_template, target_frontend_app, dirs_exist_ok=True)
        except OSError as e:
            raise CommandError(e)


    @ex(
        help='run plugin',
        )
    def run(self):
        try:
            plugin_name = os.path.basename(os.getcwd())

            self.app.log.info(f'running plugin: {plugin_name}')

            backend = os.path.join(os.getcwd(), 'backend')
            frontend = os.path.join(os.getcwd(), 'frontend')

            if not os.path.exists(backend):
                print('Unable to find backend dir. Are you running kluff from inside your plugin dir?')
                sys.exit()

            if not os.path.exists(frontend):
                print('Unable to find frontend dir. Are you running kluff from inside your plugin dir?')
                sys.exit()

            backend_docker_tag = f'{plugin_name}:backend'
            frontend_docker_tag = f'{plugin_name}:frontend'

            os.system(f'cd {backend}')
            os.system(f'docker rm $(docker stop $(docker ps -a -q --filter ancestor={backend_docker_tag} --format="{{.ID}}"))')
            os.system(f'docker build -t {backend_docker_tag} .')
            os.system(f'docker run -it -p 5000:5000 -d {backend_docker_tag}')

            os.system(f'cd {frontend}')
            os.system(f'docker rm $(docker stop $(docker ps -a -q --filter ancestor={frontend_docker_tag} --format="{{.ID}}"))')
            os.system(f'docker build -t {frontend_docker_tag} .')
            os.system(f'docker run -it -p 3000:3000 -d {frontend_docker_tag}')

        except OSError as e:
            raise CommandError(e)
    
    @ex(
        help='deploy plugin',
        arguments=[
        (['plugin_name'], 
                        {'help': 'plugin name'}
        ),
        ],
        )
    def deploy(self):
        plugin_name = self.app.pargs.plugin_name
        self.app.log.info(f'deploying plugin: {plugin_name}')
        try:
            os.system(f'cd {plugin_name}')
            os.system('git push')
        except OSError as e:
            raise CommandError(e)
