# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
## [0.6.4] 2022-10-31
- improve context handling

## [0.6.4] 2022-10-31
- template plugins now get global/plugin context
- add/fix tests

## [0.6.0] 2022-10-29
- add template tag plugin support (awesome!)
- deprecate vue/js frontend support

## [0.5.2] 2022-04-21
- add some type annotations (for IDE helpers)

## [0.5.1] 2021-07-30
- create cookiecutter created plugins in CWD now
- remove unneeded default_app_config
- better guessing/extracting of project metadata 

## [0.5.0]
### Changed
- move template engine to cookiecutter
- fix PROJECT_TITLE usage

## [0.4.22]
- deprecate Interface.plugins() method. Iterate directly over interfaces.

## [0.4.21]
- fix URL namespaces
- log submodule import errors as errors
- add urls.py example

## [0.4.20]
- fix check if class is an Interface or Implementation
- add plugins method to Interface, to allow using Interfaces in Django templates

## [0.4.19]
- improve Router support a bit

## [0.4.18] - 2021-01-09
- make auto-included URLs namespaced
- fix install prereqs of IFrontendEngines

## [0.4.17] - 2020-05-13
- require PROJECT_NAME as global settings variable
- let GDAPS user override index.html

## [0.4.16] - 2020-05-09
- fix copy path for frontend plugin templates
- more debug logging

## [0.4.15] - 2020-04-25
- fix version number source

## [0.4.14] - 2020-04-25
- change API: add check_runtime_prereq / check_install_prereq hooks
- define PROJECT_NAME in plugin settings
- obligatory namespaced settings in plugins

## [0.4.13] - 2020-03-29
- revert everything to monolithic gdaps package including frontend base

## [0.4.12] - 2020-03-28
- fix some nasty errors

## [0.4.11] - 2020-03-28
- rename gdaps app to gdaps.core to enable namespace packages
- split frontend-vue and frontend-pyside into own package
- small docs improvements

## [0.4.7] - 2019-12-22

- bugfix release
- drastically reduce package size by deleting "_build" directory.

## [0.4.6] - 2019-12-22

- deeply integrate vue-extensions package into gdaps frontend

## [0.4.5] - 2019-12-02

- make frontend engines more generic
- add stub implementation of pyside frontend
- let frontend set default package manager

## [0.4.4] - 2019-11-13

- automatically link frontend plugins for dynamic import
- various bugfixes and improvements

## [0.4.3] - 2019-11-01

- use Porterstemmer to get correct singular fontend plugin name
- ease package creation
- make license configureable at startplugin time

## [0.4.2] - 2019-10-16

- allow using variables in template file/dir names
- provide pluggable Javascript (and other) package manager support
- simple working syncplugin support
- improve frontend plugin creation
- generate frontend plugin names from entry point group by stemming

## [0.4.0] - 2019-10-12

- Change API to an easier one, following Marty Alchin's Simple Plugin Framework
- add some tests

## [0.3.5] - 2019-06-xx

### Added

- GDAPS plugins need to be Django AppConfig classes now.
