from altwalker.planner import create_planner
from altwalker.executor import create_executor
from altwalker.walker import create_walker
from custom_junit_reporter import CustomJunitReporter
import sys
import pdb
import click

def _percentege_color(percentage):
    if percentage < 50:
        return "red"

    if percentage < 80:
        return "yellow"

    return "green"


def _style_percentage(percentege):
    return click.style("{}%".format(percentege), fg=_percentege_color(percentege))


def _style_fail(number):
    color = "red" if number > 0 else "green"

    return click.style(str(number), fg=color)


def _echo_stat(title, value, indent=2):
    title = " " * indent + title.ljust(30, ".")
    value = str(value).rjust(15, ".")

    click.echo(title + value)

def _echo_statistics(statistics):
    """Pretty-print statistics."""

    click.echo("Statistics:")
    click.echo()

    total_models = statistics["totalNumberOfModels"]
    completed_models = statistics["totalCompletedNumberOfModels"]
    model_coverage = _style_percentage(completed_models * 100 // total_models)

    _echo_stat("Model Coverage", model_coverage)
    _echo_stat("Number of Models", click.style(str(total_models), fg="white"))
    _echo_stat("Completed Models", click.style(str(completed_models), fg="white"))

    _echo_stat("Failed Models", _style_fail(statistics["totalFailedNumberOfModels"]))
    _echo_stat("Incomplete Models", _style_fail(statistics["totalIncompleteNumberOfModels"]))
    _echo_stat("Not Executed Models", _style_fail(statistics["totalNotExecutedNumberOfModels"]))
    click.echo()


debugger = pdb.Pdb(skip=['altwalker.*'], stdout=sys.stdout)
reporter = None

if __name__ == "__main__": 
    try:
        planner = None
        executor = None
        statistics = {}
        models = [("models/petclinic_full.json","random(vertex_coverage(100))")]
        steps = None
        graphwalker_port = 5000
        start_element=None
        url="http://localhost:5000/"
        verbose=False
        unvisited=False
        blocked=False
        tests = "tests"
        executor_type = "python"
        planner = create_planner(models=models, steps=steps, port=graphwalker_port, start_element=start_element,
                                verbose=True, unvisited=unvisited, blocked=blocked)
        executor = create_executor(tests, executor_type, url=url)
        reporter = CustomJunitReporter() 

        walker = create_walker(planner, executor, reporter=reporter)
        walker.run()
        statistics = planner.get_statistics()
    finally:
        print(statistics)
        _echo_statistics(statistics)
        reporter.set_statistics(statistics)
        junit_report = reporter.to_xml_string()
        print(junit_report)
        with open('output.xml', 'w') as f:
            f.write(junit_report)
        with open('output_allinone.xml', 'w') as f:
            f.write(reporter.to_xml_string(generate_single_testcase=True, single_testcase_name="PetClinicAllinOne"))

        #debugger.set_trace()
        if planner:
            planner.kill()

        if executor:
            executor.kill()
    
