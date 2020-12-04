# altwalker-petclinic-example
AltWalker model-based testing example, implemented in Python, using the demo PetClinic site as target.

## Intro

This is a MBT (Model-Based Testing) example for AltWalker, based on the "famous" [PetClinic](https://github.com/spring-projects/spring-petclinic).
This tutorial is basically a port of a [Java example made for GraphWalker](https://github.com/GraphWalker/graphwalker-example/tree/master/java-petclinic) with some adaptions and cleanup.
The models are a bit described in [GraphWalker docs](https://github.com/GraphWalker/graphwalker-project/wiki/PetClinic).


## Pre-requisites

- Python3
- Firefox (or other browser)
- PetClinic

Install the python dependencies:

```pip install -r requirements.txt```

Start the PetClinic demo app.

```
# git clone https://github.com/SpringSource/spring-petclinic.git
cd spring-petclinic
# git reset --hard 482eeb1c217789b5d772f5c15c3ab7aa89caf279
mvn tomcat7:run
```

## Running

Just run run.sh :) in (Lin)unix...

```./run.sh```

or

```bash
altwalker check -m models/petclinic_full.json "random(vertex_coverage(100))"
altwalker verify -m models/petclinic_full.json tests
altwalker online tests -m models/petclinic_full.json "random(vertex_coverage(100))"
```

If you want to run this in a CI/CD pipeline or even integrate it with a test management tool (e.g. [Xray](https://getxray.app)), you can generate a Junit XML report. Since AltWalker, as of v0.2.7, does not provide the ability to generate JUnit XML reports by itself, we need to implement our own report. Besides, we need to invoke AltWalker programmatically so we can pass our custom reporter object.
Please check [custom_junit_reporter.py](custom_junit_reporter.py) and [run_with_custom_junit_report.py](run_with_custom_junit_report.py) for more details.
To

```bash
./run_with_custom_junit_report.py
```

## About the porting

I used the model provided in the upstream project with a small change, since AltWalker doesnt support unnamed edges (as of v0.2.7) yet.
I also made some common vertices available in a BaseModel, that other models will inherit from.

## Credits

Credits go to GraphWalker team and the team behind the PetClinic example, along with the [AltWalker](https://altom.gitlab.io/altwalker/altwalker/index.html) team that inspired myself and also parts of this code. I would recommend having a look at some [examples provided by AltWalker](https://altom.gitlab.io/altwalker/altwalker/examples.html).

## Contact

You can find me on [Twitter](https://twitter.com/darktelecom).

## LICENSE

[MIT](LICENSE).
