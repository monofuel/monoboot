
mono.kpxe: mono.ipxe
	cd ipxe/src && make -j 8 bin/undionly.kpxe EMBED=../../mono.ipxe
	cp ipxe/src/bin/undionly.kpxe ./mono.kpxe

.PHONY: check
check:
	python3 -m py_compile setup-chroots.py

.PHONY: check
chroots:
	python3 setup-chroots.py

.PHONY: update-local
update-local:
	ansible-playbook --become ./playbooks/dev-local.yml