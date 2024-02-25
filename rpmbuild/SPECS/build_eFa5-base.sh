#!/bin/bash

cd ../SOURCES/
rm -f eFa-base-5.0.0.tar.gz
tar czvf eFa-base-5.0.0.tar.gz eFa-base-5.0.0
cd ../SPECS
rpmbuild -ba eFa5-base.spec
