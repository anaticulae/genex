# changelog

Every noteable change is logged here.

## v0.23.0

### Feature

* add cli to rerun log file (144ab2cc7303)
* add method to parse log file (945586ce5a27)
* number steps to select steps for rerunning (07b343780e93)

### Fix

* use correct title page section class (8129ab358f25)

## v0.22.1

### Fix

* do not use global pages (389fecee6527)

## v0.22.0

### Feature

* run table detector on section pages (1b1d5cb0307a)
* replace outdated approach with JobMaker (84308ccae9ad)
* use automate approach to reduce complexity (d5c87c87e300)

## v0.21.4

### Fix

* skip step if area is not found (383e56439473)
* split figureo steps (63155d32152c)

### Documentation

* adjust modules path (f090bd084fb4)
* Happy New Year! (8741e00a6807)

## v0.21.3

### Feature

* improve path shorten (77c88b9d5a0d)

### Fix

* run caption before magic (4ef571ccb8e0)

## v0.21.2

## v0.21.1

### Fix

* adjust interface (6df182f6cac1)

## v0.21.0

### Feature

* add option to overwrite rawmaker layout config (b0f5fb27107d)

### Fix

* run caption before words (9e61ec64ac2e)

## v0.20.2

### Fix

* use Todo to avoid creating wrong output path (4adeb737284e)
* add missing steps (94f13a898e2b)

## v0.20.1

### Fix

* ensure that local is updated (9749b6128c46)

## v0.20.0

### Feature

* overwrite configured step by new config dict (2e341407418f)
* use new resource definition (05d48dd73e26)
* introduce name to fix name of generated name (776bc15ae7ed)
* add method to convert files todo (cdd881e67e38)
* add todo to create more resource information (7189b3d48f7a)

## v0.19.1

### Feature

* shrink example generator (52082c6c01a1)

## v0.19.0

### Feature

* replace with findings --optimize feature (491b65d3e4bd)

## v0.18.1

### Feature

* create optimized findings (0ffcb7ed45b4)

## v0.18.0

### Feature

* add codero step (ab2f5b3aaaec)

## v0.17.1

### Fix

* shrink formulero to given pages (1c359804bf71)

## v0.17.0

### Feature

* add formulero runner (e4fdf976248d)

### Fix

* handle sections selection correctly (8b81fa9ef323)
* log run command before run (ab8705bfe10d)

## v0.16.0

### Feature

* log runtime (32fb3482df30)
* add pdf as sections source (aafb0d3eecef)

### Fix

* add missing newline (3f3e86adc617)

## v0.15.0

### Feature

* log final execution time (8cab6124f7cd)
* add cleanup runner (1554246664b4)

### Fix

* log stderr after stdout (e6c33b9a3595)

## v0.14.0

### Feature

* use --table parameter to run tablero (b42ac74e17b9)

### Fix

* shrink tablero and figureo to given pages (ecca7e43222e)

## v0.13.1

### Fix

* add missing pdf discover path (44ef49e5b877)

## v0.13.0

### Feature

* add option to run figureo (be0aa5ef61e3)

### Fix

* do not fail on passing test.tmpdir as dest (8feeecda4be2)
* use zero base indexing (8e7f6d3e43f2)

## v0.12.1

### Feature

* run area again to use tablero data (587b651c3b4e)
* log number of started job (d9b67a09b617)

## v0.12.0

### Feature

* add tablero extraction step (5409395e385f)

## v0.11.2

### Feature

* add option to make generation more specific (1b8cf17c17e9)

### Fix

* convert \n to /n in path (c05ab06ee524)
* add missing newline (7eb4132a761e)

## v0.11.1

### Fix

* do not fail if dir is already created (bbcf8a19714e)

## v0.11.0

### Feature

* add option to run with specialized groupme config (4deaf969c8a6)
* run magic to use in words (812b1120d146)
* use live logging (a2cedf93f149)

## v0.10.0

### Feature

* run pdfinfo (8a9d5cdb04e0)

## v0.9.0

### Feature

* add extraction with remove step (606c08ff5434)

## v0.8.0

### Feature

* gather and write generated log (ad0b73b5a4df)

## v0.7.3

### Fix

* avoid side effect to global config (2e0d470ce9ce)

## v0.7.2

## v0.7.1

### Fix

* disable groupme --abbreviations if sections is not given (ba1a22d4adf6)

## v0.7.0

### Feature

* shrink abbreviation table extractor to section (7387e74a7d62)
* shrink abbreviation parser (4952b0281bf3)

## v0.6.2

### Fix

* add missing pages parameter (f56e6464db60)

## v0.6.1

### Fix

* adjust order to required resources (4d8a516cc053)

## v0.6.0

### Feature

* add spacestation to example generator (c7750021aa9e)

## v0.5.7

### Feature

* externalize job run method (32e400dee348)

### Documentation

* Happy New Year! (f7a281baa399)
* fix return type information (34dcc2d16987)

## v0.5.6

### Fix

* add base path to improve auto name generator (8d9f7df7c4af)

## v0.5.5

### Fix

* add default repo to avoid single resource error (3107f159ddba)

## v0.5.4

## v0.5.3

### Feature

* use verbose level to provide more information (02f6ffbb250f)

### Fix

* adjust logging after changing data type (7d97ae862fcf)

## v0.5.2

### Fix

* add missing import (a5ea3f98d2f8)

## v0.5.1

### Feature

* add optional features (7a42b39d3cac)

## v0.5.0

### Feature

* use sections to select correct ranges (5389da38f523)

### Fix

* forward missing smarty flag (58342d13cfbb)

## v0.4.1

## v0.4.0

### Feature

* add smarty application (71e6038647e0)

## v0.3.0

### Feature

* add docref to example generator (6282d7aacf47)

## v0.2.1

## v0.2.0

### Feature

* prepare using cache generator (f3876c51fed1)

## v0.1.5

## v0.1.4

## v0.1.3

## v0.1.2

## v0.1.1

### Feature

* extend public API (c46ec300a16d)

## v0.1.0

### Feature

* move example generator from hey project (6afff6846a09)

## v0.0.0 Initial release

