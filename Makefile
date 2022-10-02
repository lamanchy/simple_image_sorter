.PHONY: build run interface test clean

define with_os
if [ "$(shell uname)" = "Darwin" ]; then		                                           \
	OS='mac';								                                               \
elif grep -q icrosoft /proc/version; then	                                               \
	OS='wsl';								                                               \
else											                                           \
	OS='linux';								                                               \
fi;											                                               \
$1
endef

define with_trap
$(call with_os, bash -c "trap 'make clean' EXIT; $1")
endef

define compose_with_trap
$(call with_trap, docker-compose                                                           \
    -f docker-compose.yaml $1)
endef

build:
	docker-compose --profile all build

run:
	$(call compose_with_trap, \
		-f docker-compose/main.yaml \
		 --profile main up)

interface:
	$(call compose_with_trap, \
		 --profile interface up)

test:
	$(call compose_with_trap,                                                              \
		-f docker-compose/test.yaml run color_processor test)
	$(call compose_with_trap,                                                              \
		-f docker-compose/test.yaml --profile all run tester test)


clean:
	docker-compose down -t 0 --remove-orphans
