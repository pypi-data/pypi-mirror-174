#/bin/sh

KERNEL=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCHITECTURE=$(uname -m | tr '[:upper:]' '[:lower:]')
SYSTEM=$KERNEL.$ARCHITECTURE

cd "$(dirname -- "$0")"


if [ $1 = all ] || [ $1 = libbigwig ] ; then
    [ -d libbigwig ] || mkdir libbigwig
    [ -d libbigwig/$SYSTEM ] && rm -rf libbigwig/$SYSTEM
    curl -LO https://github.com/dpryan79/libBigWig/archive/refs/tags/0.4.7.tar.gz
    tar -xzf 0.4.7.tar.gz -C .
    rm 0.4.7.tar.gz
    mv libBigWig-0.4.7 libbigwig/$SYSTEM
    cd libbigwig/$SYSTEM
    make
    cd ..
    tar -cJf $SYSTEM.tar.xz $SYSTEM
    rm -rf $SYSTEM
    cd ..
fi


if [ $1 = all ] || [ $1 = samtools ] ; then
    [ -d samtools ] || mkdir samtools
    [ -d samtools/$SYSTEM ] && rm -rf samtools/$SYSTEM
    [ -d samtools/$SYSTEM.build ] && rm -rf samtools/$SYSTEM.build
    curl -LO https://github.com/samtools/samtools/releases/download/1.16.1/samtools-1.16.1.tar.bz2
    tar -xjf samtools-1.16.1.tar.bz2 -C .
    rm samtools-1.16.1.tar.bz2
    mv samtools-1.16.1 samtools/$SYSTEM.build
    PREFIX="$(pwd)/samtools/$SYSTEM"
    cd samtools/$SYSTEM.build
    ./configure --prefix="$PREFIX"
    make
    make install
    cd ..
    tar -cJf $SYSTEM.tar.xz $SYSTEM
    rm -rf $SYSTEM $SYSTEM.build
    cd ..
fi


if [ $1 = all ] || [ $1 = ucsc ] ; then
    [ -d ucsc ] || mkdir ucsc
    if [ $KERNEL = linux ] || [ $KERNEL = darwin ] ; then
        [ $KERNEL = darwin ] && LOCAL_TARGET=darwin.x86_64 || LOCAL_TARGET=$KERNEL.x86_64
        [ $KERNEL = darwin ] && DISTANT_TARGET=macOSX.x86_64 || DISTANT_TARGET=$KERNEL.x86_64
        URLS=()
        for FILE in bigWigInfo bedGraphToBigWig bigWigToBedGraph bigBedInfo bedToBigBed ; do
            URLS+=(http://hgdownload.soe.ucsc.edu/admin/exe/$DISTANT_TARGET/$FILE)
        done
        [ -d ucsc/$LOCAL_TARGET ] || rm -rf ucsc/$LOCAL_TARGET ; mkdir ucsc/$LOCAL_TARGET
        cd ucsc/$LOCAL_TARGET
        curl -L -Z --parallel-immediate --remote-name-all "${URLS[@]}"
        cd ..
        tar -cJf $LOCAL_TARGET.tar.xz $LOCAL_TARGET
        rm -rf $LOCAL_TARGET
        cd ..
    fi
fi
