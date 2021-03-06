# To get a blank line on Linux we do:
#
#  echo
#
# but the same command on Windows will display the status of the echo
# command. Instead we have to do:
#
#  echo.
#
# Unfortunately, that will cause an error on Linux, so there is no way
# to avoid having OS-specific commands:
#
import platform

blank_line = 'echo' + ('.' if platform.system() == 'Windows' else '')

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

    def is_repo(self):

        '''Determine whether we're in a Git repo or not'''

        working_dir = super(GitmodeCommand, self).get_working_dir()
        in_tree = self.command_to_val('git rev-parse --is-inside-work-tree', working_dir=working_dir)

        return not 'Not a git repository' in in_tree


    def is_enabled(self):

        '''Indicate whether ST should allow this command to run or not'''

        return self.is_repo()


    def is_visible(self):

        '''Indicate whether ST should show this command on the menu or not'''

        return self.is_enabled()


    def get_working_dir(self, root_dir=True):

        '''Get the Git directory.'''

        working_dir = super(GitmodeCommand, self).get_working_dir()
        return self.command_to_val('git rev-parse --show-toplevel', working_dir=working_dir)

    def command_to_val(self, command, working_dir=None):

        return self.run_shell_command_raw(command, None, working_dir=working_dir).rstrip('\n');


class GitmodeOnRegionCommand(GitmodeCommand):

    def run(self, edit, command=None, command_prefix=None, prompt=None, panel=None, title=None, syntax=None, refresh=None):

        GitmodeCommand.run(
            self,
            edit,
            command=command,
            command_prefix=command_prefix,
            prompt=prompt,
            region=True,
            arg_required=True,
            panel=panel,
            title=title,
            syntax=syntax,
            refresh=refresh
        )


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
            blank_line,
            'git log -n1'
        ])

        # Add stash information:
        #
        commands.extend([
            blank_line,
            'echo "Stashes:"',
            'git stash list',
        ])

        # FILE STATUS SECTION:
        #

        # Untracked files:
        #
        commands.extend([
            blank_line,
            'echo "Untracked files:"',
            'git ls-files --other --directory --exclude-standard',
        ])

        # Unstaged changes:
        #
        commands.extend([
            blank_line,
            'echo "Unstaged changes:"',
            'git ls-files --modified --exclude-standard',
        ])

        # Staged changes:
        #
        commands.extend([
            blank_line,
            'echo "Staged changes:"',
            'git diff --name-status --cached',
        ])

        # TRACKING STATUS SECTION:
        #
        if remote is not '':
            commands.extend([
                blank_line,
                'echo "Unpulled commits:"',
                'git log --decorate --pretty=oneline --abbrev-commit ..@{u}',
                blank_line,
                'echo "Unpushed commits:"',
                'git log --decorate --pretty=oneline --abbrev-commit @{u}..'
            ])

        title = title if title else '*GitMode status*'

        ShellCommandCommand.run(self, edit, command=commands, title=title, syntax='GitmodeStatus')
