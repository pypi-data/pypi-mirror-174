
v1.2.0 / 2022-11-02
===================

  * chore(version): bump minor
  * Merge pull request #147 from sayanarijit/fix-146
  * Add tests for m4a
  * Try matching audio before video
  * Merge pull request #145 from RSabet/master
  * update README to include avif
  * added image filetype avif
  * Update __init__.py
  * Merge pull request #141 from ferstar/master
  * test: remove unused imported(F401)
  * refactor: duck-typing reading magic string and try to restore the reader position if possible
  * test: fix E275 missing whitespace after keyword
  * test: Use tox pipeline instead of pytest
  * test: ignore E501 error for flake8 check
  * fix: CLI params parser
  * Merge pull request #137 from ferstar/master
  * fix: guess ".docx" func and add another doc file test case
  * fix: guess ".doc" func and add another doc file test case
  * test: skip benchmark test in tox config
  * fix: restore reader position after retrieving signature bytes
  * Merge pull request #136 from ferstar/master
  * test: no need to skip zstd test case
  * Merge pull request #135 from ferstar/master
  * fix: regression for file-like obj file type detection
  * Merge pull request #134 from babenek/actions
  * Merge pull request #129 from ferstar/master
  * Merge branch 'master' into master
  * Merge pull request #133 from magbyr/master
  * Merge pull request #131 from babenek/master
  * CI workflow in github actions
  * Changed to if statements in matching method
  * Changed return method because of coverage calculation problems
  * Extra line at EOF
  * Extra line at EOF
  * Extra line at EOF
  * Apply suggestions from code review
  * README changes
  * Linter changes
  * Added document filetypes for doc, docx, odt, xls, xlsx, ods, ppt, pptx and odp. Added tests and sample documents for document filetypes
  * Fix undocumented exception
  * style: Simplify binary to integer method
  * feat: add zstd skippable frames support
  * test: fix the tox config and missing test sample files
  * test: fix the zst test sample file
  * fix(readme): rst syntax wtf

v1.1.0 / 2022-07-12
===================

  * feat(version): bump minor
  * Merge pull request #127 from ferstar/master
  * Merge pull request #123 from levrik/patch-1
  * Merge pull request #126 from babenek/master
  * docs: add zstd type
  * fix: remove unnecessary duck-typing try
  * feat: add zst(d) type
  * chore: fix lint errors
  * test: fix memoryview test cases
  * BugFix for uncaught exceptions
  * Support PDF with BOM

v1.0.13 / 2022-04-21
====================

  * chore(version): bump patch
  * chore(version): bump patch
  * refactor(apng)
  * refactor(apng)
  * Merge pull request #120 from CatKasha/apng
  * fix typo
  * add APNG support (part 3)
  *  add APNG support (part 2)
  * add APNG support (part 1)

v1.0.12 / 2022-04-19
====================

  * Merge branch 'master' of https://github.com/h2non/filetype.py
  * feat: version bump
  * Merge pull request #118 from smasty/woff-flavors-support
  * fix(font): minimum length check (woff)
  * Add support for more WOFF/WOFF2 flavors

v1.0.10 / 2022-02-03
====================

  * Merge pull request #113 from nottaw/master
  * Use `==` for string comparisons

v1.0.9 / 2021-12-20
===================

  * Update __init__.py
  * Merge pull request #111 from asfaltboy/patch-1
  * Add python 3.9 to version classifiers
  * Merge pull request #108 from hannesbraun/aiff-support
  * Add AIFF support
  * fix(Readme): rst syntax

v1.0.5 / 2019-03-01
===================

  * Merge pull request #36 from JorjMcKie/master
  * Update README.rst
  * add jpx example to fixtures
  * Update image.py
  * support JPEG 2000
  * Merge pull request #35 from papis/master
  * Delete docs since are not linked to anything

v1.0.4 / 2019-02-09
===================

  * Merge pull request #34 from ltrojana3d/add_dicom_type
  * min bugfix
  * add Dcm class to IMAGE
  * adding image.Dcm class

v1.0.3 / 2019-02-01
===================

  * Merge pull request #32 from petergaultney/support-reading-bytes-from-readables
  * Merge pull request #33 from dotlambda/patch-1
  * Include tests in PyPI tarball
  * Support reading bytes directly from duck-typed readables

v1.0.1 / 2019-01-11
===================

  * Merge pull request #31 from david-poirier-csn/master
  * removed py3.3 from travis
  * flake8 killing me
  * fix py2.7 error
  * fix py2.7 error
  * fix flake8 complaints
  * added support for HEIC files
  * added support for HEIC files
  * Merge pull request #28 from amitlissack/expose_webm
  * expose flv and webm matchers
  * Merge pull request #25 from CloudFerro/wip-fix-byte-reading
  * Fixed number of readed bytes in utils.py

v1.0.1 / 2018-04-14
===================

  * Merge pull request #22 from gaul/memoryview
  * Merge pull request #23 from gaul/avoid-bytearray-copy
  * Avoid bytearray copy when guessing bytes input
  * Allow memoryview input to filetype.guess
  * Update README.rst
  * Delete README.md
  * Merge pull request #19 from williamjmorenor/patch-1
  * Create MANIFEST.in

v1.0.0 / 2017-07-26
===================

  * feat(docs): add static documentation
  * feat(version): bump to v1.0.0
  * Merge pull request #15 from geofmureithi/patch-1
  * Correct Flv minetype
  * Merge pull request #14 from vuolter/patch-2
  * Restore tox intro
  * Fix setup.py version
  * Code cosmetics (2)
  * Fix style typo in README.md
  * Code cosmetics

v0.1.6 / 2017-06-25
===================

  * Merge pull request #12 from vuolter/patch-1
  * Update .travis.yml
  * Update .travis.yml
  * Update setup.py
  * feat(version): bump to v0.1.5
  * fix(Makefile): fix command

v0.1.5 / 2017-05-17
===================

  * Merge pull request #11 from pkravetskiy/master
  * fixed naming conflict
  * fixed ICO image extension and mime type
  * fix(setup.py): indentation style
  * fix(setup.py): use single-line package summary
  * feat(version): bump to v0.1.4

v0.1.4 / 2017-04-08
===================

  * Merge pull request #10 from liam-middlebrook/fix-gif-mimetype
  * Fix mimetype for Gif Images
  * Merge pull request #9 from Aluriak/Aluriak-patch-1
  * Fix README API example
  * feat: add tag task in Makefile
  * feat(version): bump
