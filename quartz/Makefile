PYTHON = python3

TARGETS = \
	figs/deps_quartz_total_fig.pdf \
	figs/deps_quartz_solve_fig.pdf \
	figs/deps_quartz_ground_fig.pdf \
	figs/cdf_quartz_total_fig.pdf
# cdf_quartz_old_vs_clingo.pdf
# cdf_e4s_cache_quartz_total_fig.pdf
# cdf_e4s_cache_quartz_solve_fig.pdf
# cdf_e4s_cache_quartz_setup_fig.pdf

CSV = out_log_full_complete.csv
#CSV = out_log_full_crs_0.csv
#CSV = out_log_full_crs_1.csv

all: $(TARGETS)



figs/deps_quartz_ground_fig.pdf: $(CSV)
	$(PYTHON) ../container/analyze_deps_vs_time.py $< ground $@

figs/deps_quartz_solve_fig.pdf: $(CSV)
	$(PYTHON) ../container/analyze_deps_vs_time.py $< solve $@

figs/deps_quartz_total_fig.pdf: $(CSV)
	$(PYTHON) ../container/analyze_deps_vs_time.py $< total $@

figs/cdf_quartz_total_fig.pdf: $(CSV)
	$(PYTHON) ../container/analyze_times_cdf.py $< $@


clean:
	rm -f $(TARGETS)
