from ShellCommand.ShellCommand import ShellCommandCommand
import ShellCommand.OsShell as OsShell


class GitmodeCommand(ShellCommandCommand):

    def run(self, edit, command=None, command_prefix=None, prompt=None, region=None, arg_required=None, panel=None, title=None, syntax=None, refresh=None):

        if command_prefix is None:
            command_prefix = 'git'

        if prompt is None:
            prompt = 'Git Command'

        if refresh is None:
            refresh = True

        ShellCommandCommand.run(self,
                                edit,
                                command=command,
                                command_prefix=command_prefix,
                                prompt=prompt,
                                region=region,
                                arg_required=arg_required,
                                panel=panel,
                                title=title,
                                syntax=syntax,
                                refresh=refresh)

    def get_working_dir(self, root_dir=True):

        '''Get the Git directory.'''

        return self.command_to_val('git rev-parse --show-toplevel')

    def command_to_val(self, command):

        return OsShell.process(command).rstrip('\n')


class GitmodeStatusCommand(GitmodeCommand):

    def run(self, edit, title=None):
        commands = []

        # Work out our local and remote branches:
        #
        branch = self.command_to_val('git rev-parse --abbrev-ref HEAD')
        remote = self.command_to_val('git config branch.' + branch + '.remote')

        # If we are tracking a remote branch then add information about it to
        # the first line of the status:
        #
        if remote is not '':
            remote_url = self.command_to_val('git config remote.' + remote + '.url')
            commands.append('echo "Remote: ' + branch + ' @ ' + remote + ' (' + remote_url + ')"')

        # REPOSITORY STATE SECTION:
        #

        # Add information about the local branch:
        #
        commands.append('echo "Local:  ' + branch + '"')

        # Add the latest commit message:
        #
        commands.extend([
            'echo',
            'git log -n1'
        ])

        # Add stash information:
        #
        commands.extend([
            'echo',
            'echo Stashes:',
            'git stash list',
        ])

        # FILE STATUS SECTION:
        #

        # Untracked files:
        #
        commands.extend([
            'echo',
            'echo Untracked files:',
            'git ls-files --other --directory --exclude-standard',
        ])

        # Unstaged changes:
        #
        commands.extend([
            'echo',
            'echo Unstaged changes:',
            'git ls-files --modified --exclude-standard',
        ])

        # Staged changes:
        #
        commands.extend([
            'echo',
            'echo Staged changes:',
            'git diff --name-status --cached',
        ])

        # TRACKING STATUS SECTION:
        #
        if remote is not '':
            commands.extend([
                'echo',
                'echo Unpulled commits:',
                'git log --decorate --pretty=oneline --abbrev-commit ..@{u}',
                'echo',
                'echo Unpushed commits:',
                'git log --decorate --pretty=oneline --abbrev-commit @{u}..'
            ])

        title = title if title else '*GitMode status*'

        ShellCommandCommand.run(self, edit, command=commands, title=title, syntax='GitmodeStatus')
