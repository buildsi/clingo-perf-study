PYTHON = python3

TARGETS = \
	figs/deps_quartz_total_fig.pdf \
	figs/deps_quartz_solve_fig.pdf \
	figs/deps_quartz_ground_fig.pdf \
	figs/cdf_quartz_total_fig.pdf \
	figs/cdf_quartz_old_vs_clingo.pdf \
	figs/cdf_e4s_cache_quartz_total_fig.pdf \
	figs/cdf_e4s_cache_quartz_solve_fig.pdf \
	figs/cdf_e4s_cache_quartz_setup_fig.pdf

CSV = out_log_full_complete.csv
OLD_CSV = log_old_concretizer.csv

DEPS_VS_TIME_SCRIPT = ../container/analyze_deps_vs_time.py
CDF_SCRIPT = ../container/analyze_times_cdf.py
OLD_VS_CLINGO_SCRIPT = ../container/analyze_old_vs_asp.py
CACHE_SCRIPT = analyze_caches.py
#CSV = out_log_full_crs_0.csv
#CSV = out_log_full_crs_1.csv

all: $(TARGETS)



figs/deps_quartz_ground_fig.pdf: $(CSV) $(DEPS_VS_TIME_SCRIPT)
	$(PYTHON) $(DEPS_VS_TIME_SCRIPT) $< ground $@

figs/deps_quartz_solve_fig.pdf: $(CSV) $(DEPS_VS_TIME_SCRIPT)
	$(PYTHON) $(DEPS_VS_TIME_SCRIPT) $< solve $@

figs/deps_quartz_total_fig.pdf: $(CSV) $(DEPS_VS_TIME_SCRIPT)
	$(PYTHON) $(DEPS_VS_TIME_SCRIPT) $< total $@

figs/cdf_quartz_total_fig.pdf: $(CSV) $(CDF_SCRIPT)
	$(PYTHON) $(CDF_SCRIPT) $< $@

figs/cdf_quartz_old_vs_clingo.pdf: $(CSV) $(OLD_CSV) $(OLD_VS_CLINGO_SCRIPT)
	$(PYTHON) $(OLD_VS_CLINGO_SCRIPT) $(OLD_CSV) $(CSV) $@

figs/cdf_e4s_cache_quartz_total_fig.pdf: $(CSV) $(CACHE_SCRIPT)
	$(PYTHON) $(CACHE_SCRIPT) total $@

figs/cdf_e4s_cache_quartz_solve_fig.pdf: $(CSV) $(CACHE_SCRIPT)
	$(PYTHON) $(CACHE_SCRIPT) solve $@

figs/cdf_e4s_cache_quartz_setup_fig.pdf: $(CSV) $(CACHE_SCRIPT)
	$(PYTHON) $(CACHE_SCRIPT) setup $@

clean:
	rm -f $(TARGETS)

