pushd "fido2-manage-${pkgver}" > /dev/null

# Avoid "Package contains reference to $srcdir" warnings
export CFLAGS+=" -ffile-prefix-map=$srcdir=/usr/src"
export CFLAGS="$CFLAGS -Wno-error"
export LDFLAGS="$LDFLAGS -Wno-error"

cmake \
	-S token2-piv-tool/ \
	-B build/ \
	-G "Unix Makefiles" \
	-DCMAKE_BUILD_TYPE="Release" \
	-DBUILD_STATIC_LIB=OFF \
	-DSKIP_TESTS=ON \
	-DGENERATE_MAN_PAGES=ON \
	-DCMAKE_INSTALL_PREFIX="/usr"

popd > /dev/null
