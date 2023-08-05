from pyfiglet import Figlet
import argparse
from OntimDevTool import version
from OntimDevTool.diag_port_controller import open_diag_port, close_diag_port
from OntimDevTool.auth_controller import authorise

FUNCTIONLIST = ["open_diag", "close_diag", "authorise"]

def print_logo():
    logo = Figlet().renderText(f"Ontim Tool      {version}")
    print(logo)

def main():
    """
    Command line main entry

    Start OntimDevTool

    * list all functions supported.
    ```
    otdev-tool -l
    ```

    * open diag port
    ```
    otdev-tool -p sunfire -f open_diag_port
    ```

    * close diag port
    ```
    otdev-tool -p sunfire -f close_diag_port
    ```
 
    * authorise
    ```
    otdev-tool -p sunfire -f authorise
    ```
    """
    print_logo()
    parser = argparse.ArgumentParser(prog='otdev-tool')

    parser.add_argument('-l', '--list', dest='list_functions', action='store_true', help='List all functions supported.')
    parser.add_argument('-p', '--project', dest='project', default='sunfire', help='Set project, default is sunfire.')
    parser.add_argument('-f', '--function', dest='function', help="Set function you'd like to call.")

    args = parser.parse_args()

    if args.list_functions:
        print(f"Functions supported: {FUNCTIONLIST}")
        parser.print_usage()
        return

    if args.project:
        project = args.project

    if args.function:
        function = args.function
        function_hub(project, function)
    else:
        parser.print_help()
        return

def function_hub(project, function):
    print(f"start run tools, project: {project}, function: {function}")
    if function == FUNCTIONLIST[0]:
        open_diag_port(project)
    elif function == FUNCTIONLIST[1]:
        close_diag_port()
    elif function == FUNCTIONLIST[2]:
        authorise()
    else:
        print(f"unsupport function: {function}")


if __name__ == "__main__":
    main()
