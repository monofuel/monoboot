
mono.kpxe:
	cd ipxe/src && make -j 8 bin/undionly.kpxe EMBED=../../mono.ipxe
	cp ipxe/src/bin/undionly.kpxe ./mono.kpxe

