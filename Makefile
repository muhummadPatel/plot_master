PROCESSING_JAVA = /usr/local/bin/processing-java
BUILD_OUTPUT_DIR = build_out
RUN_OUTPUT_DIR = run_out
EXPORT_MAC_OUTPUT_DIR = export_mac_out

run:
	rm -r -f `pwd`/$(RUN_OUTPUT_DIR)
	$(PROCESSING_JAVA) --sketch=`pwd` --output=`pwd`/$(RUN_OUTPUT_DIR) --run

build:
	rm -r -f `pwd`/$(BUILD_OUTPUT_DIR)
	$(PROCESSING_JAVA) --sketch=`pwd` --output=`pwd`/$(BUILD_OUTPUT_DIR) --build

export_mac:
	rm -r -f `pwd`/$(EXPORT_MAC_OUTPUT_DIR)
	$(PROCESSING_JAVA) --sketch=`pwd` --output=`pwd`/$(EXPORT_MAC_OUTPUT_DIR) --export --platform macosx
