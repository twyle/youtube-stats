## How To Contribute

<!-- [fork]: https://github.com/github/youtube-video-stats/fork
[pr]: https://github.com/github/youtube-video-stats/compare
[code-of-conduct]: CODE_OF_CONDUCT.md -->

Hi there! We're thrilled that you'd like to contribute to this project. Your help is essential for keeping it great.

We accept pull requests for bug fixes and features where we've discussed the approach in an issue and given the go-ahead for a community member to work on it. We'd also love to hear about ideas for new features as issues.

We track issues on our project board [here](https://github.com/orgs/github/projects/9557/views/1).

Please do:

* Check existing issues to verify that the [bug][bug issues] or [feature request][feature request issues] has not already been submitted.
* Open an issue if things aren't working as expected.
* Open an issue to propose a significant change.
* Open a pull request to fix a bug.
* Open a pull request to fix documentation about a command.
* Open a pull request for any issue labelled [`help wanted`][hw] or [`good first issue`][gfi].

- To report a bug, check the [bug template](.github/issues/bug.md)

- To ask for a feature,check the [feature template](.github/issues/feature.md)

Please avoid:

* Opening pull requests for issues marked `needs-design`, `needs-investigation`, or `blocked`.

Contributions to this project are [released](https://help.github.com/articles/github-terms-of-service/#6-contributions-under-repository-license) to the public under the [project's open source license](LICENSE).

Please note that this project is released with a [Contributor Code of Conduct][code-of-conduct]. By participating in this project you agree to abide by its terms.

## Prerequisites for running and testing code

These are one time installations required to be able to test your changes locally as part of the pull request (PR) submission process.

1. Install [Python](https://www.python.org/downloads/) for your platform
2. Install ``PIP`` for your platform:
```sh
sudo apt install python3-pip
```
3. Install ``Python3 Venv`` for your platform

```sh
sudo apt install python3-venv
```
4. Create the virtual environment. Ensure you are in the root directory of your local repo.
```sh
python3 -m venv venv
```
5. Activate the created virtual environment:
```sh
source venv/bin/activate
```
6. Install the requirements. There is a ``Makefile`` in the project root that you should use for this step:
```sh
make install-dev # Install development dependencies
make install-prod # Install production dependencies
```

## Dev loop & Testing changes

Once the development environment is setup, you can start making changes to the code. To test the changes, just run the application and navigate to the browser; from the project root, with the ``venv`` activated:
```sh
python3 services/app/manage.py run
```
Then check ``http://localhost:5000/apidocs``

## Useful commands:
Here are some commands that come in handy:

### Build the Development container
```sh
make build-dev
```

### Run Development Container
```sh
make run-dev
```

### Run tests
```sh
make test
```

### Lint code
```sh
make lint
```

## Submitting a pull request

1. [Fork][fork] and clone the repository
2. Configure and install the dependencies (in the repository root folder)
3. Create a new branch: `git checkout -b my-branch-name`
4. Make your change, add tests, and make sure the tests and linter still pass
5. Push to your fork and [submit a pull request][pr]

Here are a few things you can do that will increase the likelihood of your pull request being accepted:

- Format your code with [prettier](https://prettier.io/).
- Write tests.
- Keep your change as focused as possible. If there are multiple changes you would like to make that are not dependent upon each other, consider submitting them as separate pull requests.
- Write a [good commit message](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html).

## Resources

- [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/)
- [Using Pull Requests](https://help.github.com/articles/about-pull-requests/)
- [GitHub Help](https://help.github.com)

[bug issues]: https://github.com/github/vscode-github-actions/labels/bug
[feature request issues]: https://github.com/github/vscode-github-actions/labels/enhancement
[hw]: https://github.com/github/vscode-github-actions/labels/help%20wanted
[gfi]: https://github.com/github/vscode-github-actions/labels/good%20first%20issue
