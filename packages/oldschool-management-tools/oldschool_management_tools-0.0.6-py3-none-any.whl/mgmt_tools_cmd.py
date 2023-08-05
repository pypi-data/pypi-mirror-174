import cmd
from oldschool_management_tools import parse_day, show_day_sched, prompt_day_tasks


class MgmtToolsCmd(cmd.Cmd):
    intro = "Welcome to Old School Management Tools"
    prompt = "(mgmt) "

    def do_prompt_tasks(self, day):
        parsed_day = parse_day(day)
        prompt_day_tasks(parsed_day)

    def do_show_sched(self, day):
        parsed_day = parse_day(day)
        show_day_sched(parsed_day)

    def do_die(self, args):
        return True

    def do_EOF(self, args):
        return True


if __name__ == "__main__":
    MgmtToolsCmd().cmdloop()
