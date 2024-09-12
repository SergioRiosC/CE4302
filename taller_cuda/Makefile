default: help

.PHONY: help
help: ## Show help for each of the Makefile recipes. 
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[1m\033[35m%-13s\033[0m %s\n\033[0m", $$1, $$2}'
	@printf "\033[5m\033[1m%-13s\n\033[0m" "Please define the TEST variable when executing test commands!"
	@printf "\033[1m%-13s\033[36m %s\n\033[0m" "Supported TEST values: [1,2,3,4,5]";
	@printf "\033[1m%-13s\033[36m %s\n\033[0m" "Example:" 'make test TEST=1';

build_all: scalar neon cuda ## build all codes 

clean: ## clean build files
	rm -rf build 
	mkdir build

scalar: ## compile scalar code
	gcc scalar/scalar.c -o build/scalar -lm

neon: ## compile code using neon intrinsics
	gcc neon/neon.c -o build/scalar -lm

cuda: ## compile cuda code 
	nvcc cuda/cuda.c -o build/cuda 

test: build_all ## executes all codes for one test image, saves result pngs in build folder
	python3 img2file.py -i imagenes/test$(TEST).png -o build/test$(TEST).txt 
	./build/scalar test$(TEST).txt -o test$(TEST)s.txt
	./build/neon test$(TEST).txt -o test$(TEST)n.txt
	./build/cuda test$(TEST).txt -o test$(TEST)c.txt
	python3 file2img.py -i build/test$(TEST)s.txt -o build/test$(TEST)_scalar.png 
	python3 file2img.py -i build/test$(TEST)n.txt -o build/test$(TEST)_neon.png 
	python3 file2img.py -i build/test$(TEST)c.txt -o build/test$(TEST)_cuda.png 
	xdg-open build/test$(TEST)_scalar.png
	xdg-open build/test$(TEST)_neon.png
	xdg-open build/test$(TEST)_cuda.png
