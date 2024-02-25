#!/bin/bash

cd ../SOURCES/
rm -f eFa-5.0.0.tar.gz
tar czvf eFa-5.0.0.tar.gz eFa-5.0.0
cd ../SPECS
rpmbuild -ba eFa5.spec
