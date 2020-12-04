from altwalker.reporter import Reporter
from junit_xml import TestSuite, TestCase

import json
import datetime
import time
import pdb
import sys

def _add_timestamp(string):
    return "[{}] {}".format(datetime.datetime.now(), string)


def _format_step(step):
    if step.get("modelName"):
        string = "{}.{}".format(step["modelName"], step["name"])
    else:
        string = "{}".format(step["name"])

    return string


def _format_step_info(step):
    string = ""

    if step.get("data"):
        data = json.dumps(step["data"], sort_keys=True, indent=4)
        string += "\nData:\n{}\n".format(data)

    if step.get("unvisitedElements"):
        unvisited_elements = json.dumps(step["unvisitedElements"], sort_keys=True, indent=4)
        string += "\nUnvisited Elements:\n{}\n".format(unvisited_elements)

    return string


class _Formater(Reporter):
    """Format the message for reporting."""

    def step_start(self, gstep):
        """Report the starting execution of a step.

        Args:
            gstep (:obj:`dict`): The step that will be executed next.
        """

        message = "{} Running".format(_format_step(gstep))
        message += _format_step_info(gstep)

        self._log(_add_timestamp(message))

        if ('modelName' in gstep) and ('name' in gstep):
            if gstep['modelName'] not in self.models:
                self.models[gstep['modelName']] = {}
            self.models[gstep['modelName']]['step_started_at'] = time.time()

    def step_end(self, gstep, step_result):
        """Report the result of the step execution.

        Args:
            gstep (:obj:`dict`): The step just executed.
            step_result (:obj:`dict`): The result of the step.
        """

        error = step_result.get("error")
        status = "FAIL" if error else "PASSED"
        message = "{} Status: {}\n".format(_format_step(gstep), status)
        error_message = ""

        output = step_result.get("output")
        result = step_result.get("result")

        if output:
            message += "Output:\n{}".format(output)

        if result:
            message += "\nResult: {}\n".format(json.dumps(result, sort_keys=True, indent=4))

        if error:
            error_message += "\nError: {}\n".format(error["message"])

            if error.get("trace"):
                error_message += "\n{}\n".format(error["trace"])

        self._log(_add_timestamp(message))
        self._log(_add_timestamp(error_message))

        #self.debugger.set_trace()
        #gstep['type']
        #gstep['modelName']
        #gstep['name']
        #gstep['properties'] 
        #gstep['data']

        if ('modelName' in gstep) and ('name' in gstep):
            if gstep['modelName'] not in self.models:
                self.models[gstep['modelName']] = {}

            self.models[gstep['modelName']]['status'] = status
            total_elapsed_time = 0
            if 'total_elapsed_time' in self.models[gstep['modelName']]:
                total_elapsed_time = self.models[gstep['modelName']]['total_elapsed_time']

            elapsed_time = 0
            if 'step_started_at' in self.models[gstep['modelName']]:
                elapsed_time = time.time() - self.models[gstep['modelName']]['step_started_at']
            self.models[gstep['modelName']]['total_elapsed_time'] = total_elapsed_time + elapsed_time

            #if output:
            if 'output' not in self.models[gstep['modelName']]:
                self.models[gstep['modelName']]['output'] = ''
            self.models[gstep['modelName']]['output'] = self.models[gstep['modelName']]['output'] + "\n" + _add_timestamp(message)

            if error:
                if 'error' not in self.models[gstep['modelName']]:
                    self.models[gstep['modelName']]['error'] = ''

                # self.models[gstep['modelName']]['error'] = self.models[gstep['modelName']]['error'] + "\n" + error.get('message', '') + error.get('trace', '')
                self.models[gstep['modelName']]['error'] = self.models[gstep['modelName']]['error'] + "\n" + _add_timestamp(error_message)

    def error(self, step, message, trace=None):
        """Report an unexpected error.

        Args:
            step (:obj:`dict`): The step executed when the error occurred.
            message (:obj:`str`): The message of the error.
            trace (:obj:`str`): The traceback.
        """
        if step:
            string = "Unexpected error occurred while running {}.\n".format(_format_step(step))
        else:
            string = "Unexpected error occurred.\n"
        string += "{}\n".format(message)

        if trace:
            string += "\n{}\n".format(trace)

        self._log(_add_timestamp(string))


class CustomJunitReporter(_Formater):
    """This reporter builds a custom JUnit XML report, with one testcase per model or a single testcase for the whole execution."""

    def __init__(self):
        self.debugger = pdb.Pdb(skip=['altwalker.*'], stdout=sys.stdout)
        self.models = {}
        self.statistcs = None

    def _log(self, string):
        """Prints the string using the buildin :func:`print` function."""

        print(string)

    def set_statistics(self, statistics):
        self.statistics = statistics

    def _format_statistics(self):
        """Pretty-print statistics."""

        s = "== Global Statistics ==\n"

        total_models = self.statistics["totalNumberOfModels"]
        completed_models = self.statistics["totalCompletedNumberOfModels"]
        model_coverage = "{}%".format(completed_models * 100 // total_models)

        s += "Model Coverage: {}%\n".format(model_coverage)
        s += "Number of Models: {}\n".format(str(total_models))
        s += "Completed Models: {}\n".format(str(completed_models))
        s += "Failed Models: {}\n".format(self.statistics["totalFailedNumberOfModels"])
        s += "Incomplete Models: {}\n".format(self.statistics["totalIncompleteNumberOfModels"])
        s += "Not Executed Models: {}\n".format(self.statistics["totalNotExecutedNumberOfModels"])
        s += "====\n"
        return s

    def to_xml_string(self, testsuite_name="AltWalker", generate_single_testcase=False, single_testcase_name="whole_model"):
        test_cases = []

        if not generate_single_testcase:
            for model in self.models:
                output = self.models[model].get('output', None)
                error_output = self.models[model].get('error', None)
                testcase = TestCase(model, "models", self.models[model]['total_elapsed_time'], output, error_output)
                if error_output:
                    testcase.add_failure_info("failure", error_output)
                test_cases.append(testcase)
        else:
            output = self._format_statistics()
            error_output = ""
            total_elapsed_time = 0
            for model in self.models:
                output += self.models[model].get('output', "")
                error_output += self.models[model].get('error', "")
                total_elapsed_time += self.models[model].get('total_elapsed_time', 0)

            testcase = TestCase(single_testcase_name, "models", total_elapsed_time, output, error_output)
            if error_output:
                testcase.add_failure_info("failure", error_output)
            test_cases.append(testcase)            

        ts = TestSuite(testsuite_name, test_cases)
        # pretty printing is on by default but can be disabled using prettyprint=False
        return TestSuite.to_xml_string([ts])