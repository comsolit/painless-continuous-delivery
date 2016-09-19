"""Post-generate hook for cookiecutter."""
import logging
import os
import shutil
import sys


def shell(command):
    """Portable system call that aborts generation in case of failure."""
    exit_code = os.system(command)
    if exit_code:
        LOG.error('Project generation failed.')
        sys.exit(exit_code)


def remove_temporary_files():
    """Remove files and folders only needed as input for generation."""
    LOG.info('Removing input data folder ...')
    shutil.rmtree('_')


def init_version_control():
    """Initialize a repository, commit the code, and prepare for pushing."""
    vcs_info = {
        'platform_name': '{{ cookiecutter.vcs_platform }}',
        'platform': '{{ cookiecutter.vcs_platform.lower() }}',
        'account': '{{ cookiecutter.vcs_account }}',
        'project': '{{ cookiecutter.project_slug }}',
    }
    vcs_info['remote_uri'] = \
        'git@{platform}:{account}/{project}.git'.format(**vcs_info)
    vcs_info['web_url'] = \
        'https://{platform}/{account}/{project}'.format(**vcs_info)

    LOG.info('Initializing version control ...')
    shell('git init --quiet')
    shell('git add .')
    shell('git commit --quiet '
          '-m "Initial commit by Painless Continuous Delivery"')
    shell('git remote add origin {remote_uri}'.format(**vcs_info))
    LOG.info("You can now create a project '{project}' on {platform_name}."
             " {web_url}".format(**vcs_info))
    LOG.info('Then push the code to it: $ git push -u origin --all')


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    LOG = logging.getLogger('post_gen_project')

    remove_temporary_files()
    init_version_control()
