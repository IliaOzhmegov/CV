.PHONY: cv

CC = xelatex
CV_DIR = cv
CV_SRCS = cv/sections.tex

cv.pdf: $(CV_DIR)/cv.tex $(CV_SRCS)
	$(CC) -output-directory=$(CV_DIR) $<

clean:
	rm -rf $(CV_DIR)/*.pdf
