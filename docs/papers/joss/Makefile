# =============================================================================
# @file    Makefile
# @brief   Makefile for generating previews of the paper
# @author  Michael Hucka <mhucka@caltech.edu>
# @license Please see the file named LICENSE in the project directory
# @website https://github.com/casics/nostril
# =============================================================================

input	= paper.md
output	= paper.pdf
bib	= paper.bib

title	= "Nostril: a nonsense string evaluator written in Python"
author	= "Michael Hucka"
repo	= "https://github.com/casics/nostril"

$(output): $(input) $(bib) Makefile
	pandoc \
	-V paper_title=$(title) \
	-V citation_author=$(author) \
	-V repository=$(repo) \
	-V archive_doi="http://dx.doi.org/00.00000/zenodo.0000000" \
	-V formatted_doi="00.00000/joss.00000" \
	-V paper_url="http://joss.theoj.org/papers/" \
	-V review_issue_url="http://joss.theoj.org/papers/" \
	-V issue="0" \
	-V volume="00" \
	-V year="2018" \
	-V submitted="00 January 0000" \
	-V published="00 January 0000" \
	-V page="00" \
	-V graphics="true" \
	-V joss_logo_path="whedon/resources/joss-logo.png" \
	-V geometry:margin=1in \
	-o $(output) \
	--pdf-engine=xelatex \
	--filter pandoc-citeproc $(input) \
	--from markdown+autolink_bare_uris \
	--template "whedon/resources/latex.template"

autorefresh:;
	((ls $(input) $(bib) | entr make $(output)) &)
