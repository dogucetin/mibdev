# python
a few python utilities

displaymib: A simple SCOS-2000 MIB viewer. Upon selecting a folder, the viewer organizes each MIB file into multiple tabs, providing a clear, structured display. Field names are conveniently shown at the top of the interface, allowing users to quickly verify MIB implementations. Additionally, double-clicking on any item opens it in the log window, enabling copying and pasting. The built-in search functionality allows users to find keywords. Developed with SCOS-2000 v7.2 ICD as the reference, this tool is ideal for quickly reviewing MIB structures.

mergemib: A straightforward utility for merging two SRDB folders. After selecting two source folders and a destination folder, the tool concatenates the files from the SRDBs and saves the combined output in the specified destination. The tool does not perform a consistency check, just concatanes.

md5sum: A simple tool to calculate the MD5 checksum of any input file

bin/x86: precompiled binaries of the utilities for x86 platform
