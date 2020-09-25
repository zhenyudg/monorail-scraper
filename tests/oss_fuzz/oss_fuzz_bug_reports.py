test_input_5 = """Detailed report: https://clusterfuzz-external.appspot.com/testcase?key=6051005141614592

Fuzzer: libFuzzer_libarchive_fuzzer
Job Type: libfuzzer_asan_libarchive
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x60400000deb4
Crash State:
  uudecode_bidder_bid
  choose_filters
  archive_read_open1
  
Recommended Security Severity: Medium


Minimized Testcase (0.02 Kb):
Download: https://clusterfuzz-external.appspot.com/download/AMIfv97UJ_XegpDWBsRbTqTw-2GXGnM9sFyyhbLgIpxY2I5jzNAiwJF8mF_cBinyVep976oB_sAB_UFxDc_pVduWNXhlHryizcDM7MctFvyTv_IRwGzOvsCkBGkK2xF-83gFeQsuAPS9cVpjOVLxuz3my3T6pEG0D3XyduSUqv6VnLTAKGvtp7E
begin 770 _W
0A7M/
~


Filer: ochang

See  for more information."""

# 126 ###############################################################################################

test_input_126 = """Issue 126: pcre2: Heap-buffer-overflow in parse_regex
Reported by ClusterFuzz-External on Mon, Oct 31, 2016, 11:58 PM EDT Project Member
link
Code

more_vert
1 of 21471
Back to list
Detailed report: https://clusterfuzz-external.appspot.com/testcase?key=6544078783119360

Fuzzer: libFuzzer_pcre2_fuzzer
Job Type: libfuzzer_asan_pcre2
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x60300000011c
Crash State:
  parse_regex
  pcre2_compile_8
  _start
  
Recommended Security Severity: Medium

Regressed: https://clusterfuzz-external.appspot.com/revisions?job=libfuzzer_asan_pcre2&range=201610311947:201610312023

Minimized Testcase (0.01 Kb): https://clusterfuzz-external.appspot.com/download/AMIfv94e2eucet3LDQplzG1u73sGldGgS5OJyDfv2uramuXF209jN8Ouy--5rjrrjmsStzerBsPvdYMW0Q4-HM-qvseSDZl1DEqVtGx8Ajwsuvt5Zcql9E42Jt_CACwxxvp0CTz4JeuLyfsdxJPcSop-TKtSb_PNT_X-ONwVEtErCSRsXlAdBg4?testcase_id=6544078783119360

Issue filed automatically.

See https://github.com/google/oss-fuzz/blob/master/docs/reproducing.md for more information."""

# 16307 ###############################################################################################

test_input_16307 = """Issue 16307: lz4/compress_fuzzer: ASSERT: matchIndex < current
Reported by ClusterFuzz-External on Thu, Aug 8, 2019, 7:30 PM EDT Project Member
link
Code

more_vert
1 of 21471
Back to list
Detailed report: https://oss-fuzz.com/testcase?key=5653813716844544

Project: lz4
Fuzzer: afl_lz4_compress_fuzzer
Fuzz target binary: compress_fuzzer
Job Type: afl_asan_lz4
Platform Id: linux

Crash Type: ASSERT
Crash Address: 
Crash State:
  matchIndex < current
  LZ4_compress_destSize_extState
  LZ4_compress_destSize
  
Sanitizer: address (ASAN)

Regressed: https://oss-fuzz.com/revisions?job=afl_asan_lz4&range=201907170234:201907180228

Reproducer Testcase: https://oss-fuzz.com/download?testcase_id=5653813716844544

Issue filed automatically.

See https://github.com/google/oss-fuzz/blob/master/docs/reproducing.md for instructions to reproduce this bug locally.

This bug is subject to a 90 day disclosure deadline. If 90 days elapse
without an upstream patch, then the bug report will automatically
become visible to the public."""

# 19429 ###############################################################################################

test_input_19429 = """Issue 19429: irssi:theme-load-fuzz: Stack-overflow with empty stacktrace
Reported by ClusterFuzz-External on Fri, Dec 13, 2019, 3:43 AM EST Project Member
link
Code

more_vert
Detailed Report: https://oss-fuzz.com/testcase?key=5706035654557696

Project: irssi
Fuzzing Engine: libFuzzer
Fuzz Target: theme-load-fuzz
Job Type: libfuzzer_asan_irssi
Platform Id: linux

Crash Type: Stack-overflow
Crash Address: 0x7ffe43f22ff8
Crash State:
  NULL
Sanitizer: address (ASAN)

Regressed: https://oss-fuzz.com/revisions?job=libfuzzer_asan_irssi&range=201912110235:201912111653

Reproducer Testcase: https://oss-fuzz.com/download?testcase_id=5706035654557696

Issue filed automatically.

See https://google.github.io/oss-fuzz/advanced-topics/reproducing for instructions to reproduce this bug locally.
When you fix this bug, please
  * mention the fix revision(s).
  * state whether the bug was a short-lived regression or an old bug in any stable releases.
  * add any other useful information.
This information can help downstream consumers.

If you need to contact the OSS-Fuzz team with a question, concern, or any other feedback, please file an issue at https://github.com/google/oss-fuzz/issues. Comments on individual Monorail issues are not monitored.

This bug is subject to a 90 day disclosure deadline. If 90 days elapse
without an upstream patch, then the bug report will automatically
become visible to the public.
Comment 1 by ClusterFuzz-External on Fri, Dec 13, 2019, 10:38 AM EST Project Member

more_vert
Status: Verified (was: New)
Labels: ClusterFuzz-Verified

ClusterFuzz testcase 5706035654557696 is verified as fixed in https://oss-fuzz.com/revisions?job=libfuzzer_asan_irssi&range=201912120349:201912130345

If this is incorrect, please file a bug on https://github.com/google/oss-fuzz/issues/new
Comment 2 by sheriffbot@chromium.org on Sun, Jan 12, 2020, 11:38 AM EST Project Member

more_vert
Labels: -restrict-view-commit

This bug has been fixed for 30 days. It has been opened to the public.

- Your friendly Sheriffbot"""

# 22076 ###############################################################################################

test_input_22076 = """Issue 22076: llvm:clang-fuzzer: Stack-overflow in GetFullTypeForDeclarator
Reported by ClusterFuzz-External on Thu, May 7, 2020, 6:26 AM EDT (15 days ago) Project Member
link
Code

more_vert
‹ Prev
54 of 21471
Next ›
Back to list
Detailed Report: https://oss-fuzz.com/testcase?key=5196721950031872

Project: llvm
Fuzzing Engine: libFuzzer
Fuzz Target: clang-fuzzer
Job Type: libfuzzer_asan_llvm
Platform Id: linux

Crash Type: Stack-overflow
Crash Address: 0x7ffeb72c0f48
Crash State:
  GetFullTypeForDeclarator
  clang::Sema::GetTypeForDeclarator
  clang::Sema::ActOnBlockArguments
  
Sanitizer: address (ASAN)

Regressed: https://oss-fuzz.com/revisions?job=libfuzzer_asan_llvm&range=202005030248:202005040645

Reproducer Testcase: https://oss-fuzz.com/download?testcase_id=5196721950031872

Issue filed automatically.

See https://google.github.io/oss-fuzz/advanced-topics/reproducing for instructions to reproduce this bug locally.
When you fix this bug, please
  * mention the fix revision(s).
  * state whether the bug was a short-lived regression or an old bug in any stable releases.
  * add any other useful information.
This information can help downstream consumers.

If you need to contact the OSS-Fuzz team with a question, concern, or any other feedback, please file an issue at https://github.com/google/oss-fuzz/issues. Comments on individual Monorail issues are not monitored.
Comment 1 by ClusterFuzz-External on Fri, May 8, 2020, 12:20 PM EDT (14 days ago) Project Member

more_vert
Status: Verified (was: New)
Labels: ClusterFuzz-Verified

ClusterFuzz testcase 5196721950031872 is verified as fixed in https://oss-fuzz.com/revisions?job=libfuzzer_asan_llvm&range=202005070415:202005080243

If this is incorrect, please file a bug on https://github.com/google/oss-fuzz/issues/new"""

# 24163 ###############################################################################################

test_input_24163 = """Issue 24163: libevt:file_fuzzer: Timeout in file_fuzzer
Reported by ClusterFuzz-External on Wed, Jul 15, 2020, 10:33 AM EDT Project Member
link
Code

more_vert
‹ Prev
94 of 2057
Next ›
Back to list
Detailed Report: https://oss-fuzz.com/testcase?key=5187211973361664

Project: libevt
Fuzzing Engine: libFuzzer
Fuzz Target: file_fuzzer
Job Type: libfuzzer_asan_i386_libevt
Platform Id: linux

Crash Type: Timeout (exceeds 60 secs)
Crash Address: 
Crash State:
  file_fuzzer
  
Sanitizer: address (ASAN)

Crash Revision: https://oss-fuzz.com/revisions?job=libfuzzer_asan_i386_libevt&revision=202007150438

Reproducer Testcase: https://oss-fuzz.com/download?testcase_id=5187211973361664

Issue filed automatically.

See https://google.github.io/oss-fuzz/advanced-topics/reproducing for instructions to reproduce this bug locally.
When you fix this bug, please
  * mention the fix revision(s).
  * state whether the bug was a short-lived regression or an old bug in any stable releases.
  * add any other useful information.
This information can help downstream consumers.

If you need to contact the OSS-Fuzz team with a question, concern, or any other feedback, please file an issue at https://github.com/google/oss-fuzz/issues. Comments on individual Monorail issues are not monitored.

This bug is subject to a 90 day disclosure deadline. If 90 days elapse
without an upstream patch, then the bug report will automatically
become visible to the public.
Comment 1 by joachim....@gmail.com on Wed, Jul 15, 2020, 3:59 PM EDT

more_vert
Related issue https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=24149

Current version of the code allows record data to be wrapped indefinitely, changes to allow wrap only once in the record scan
https://github.com/libyal/libevt/commit/4bbeb0e18ee3d4c1f74cf53f1643cff80a500baa
Comment 2 by ClusterFuzz-External on Thu, Jul 16, 2020, 10:23 AM EDT Project Member

more_vert
Status: Verified (was: New)
Labels: ClusterFuzz-Verified

ClusterFuzz testcase 5187211973361664 is verified as fixed in https://oss-fuzz.com/revisions?job=libfuzzer_asan_i386_libevt&range=202007150438:202007160226

If this is incorrect, please file a bug on https://github.com/google/oss-fuzz/issues/new
Comment 3 by sheriffbot on Sat, Aug 15, 2020, 4:03 PM EDT Project Member

more_vert
Labels: -restrict-view-commit

This bug has been fixed for 30 days. It has been opened to the public.

- Your friendly Sheriffbot"""
