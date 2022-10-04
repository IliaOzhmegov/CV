.PHONY: cv

CC = xelatex
CV_DIR = cv
SECTIONS_DIR = cv/sections
CV_SRCS = $(shell find $(SECTIONS_DIR) -name '*.tex')

cv.pdf: $(CV_DIR)/cv.tex $(CV_SRCS)
	$(CC) -output-directory=$(CV_DIR) $<

clean:
	rm -rf $(CV_DIR)/*.pdf
