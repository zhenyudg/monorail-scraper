test_input_5 = """Issue 5: Heap-buffer-overflow in uudecode_bidder_bid
Reported by ClusterFuzz-External on Fri, May 27, 2016, 6:27 PM EDT Project Member
link
Code

more_vert
1 of 21471
Back to list
Detailed report: https://clusterfuzz-external.appspot.com/testcase?key=6051005141614592

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

See  for more information.
Comment 1 by ochang@google.com on Fri, May 27, 2016, 6:33 PM EDT Project Member

more_vert
Labels: Restrict-View-Commit

Comment 2 by ochang@google.com on Fri, May 27, 2016, 6:39 PM EDT Project Member

more_vert
Labels: Type-Bug-Security

Comment 3 by ClusterFuzz-External on Sat, May 28, 2016, 12:22 AM EDT Project Member

more_vert
ClusterFuzz has detected this issue as fixed in range 201605271439:201605271739.

Detailed report: https://clusterfuzz-external.appspot.com/testcase?key=6051005141614592

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

Fixed: https://clusterfuzz-external.appspot.com/revisions?job=libfuzzer_asan_libarchive&range=201605271439:201605271739

Minimized Testcase (0.02 Kb):
Download: https://clusterfuzz-external.appspot.com/download/AMIfv97UJ_XegpDWBsRbTqTw-2GXGnM9sFyyhbLgIpxY2I5jzNAiwJF8mF_cBinyVep976oB_sAB_UFxDc_pVduWNXhlHryizcDM7MctFvyTv_IRwGzOvsCkBGkK2xF-83gFeQsuAPS9cVpjOVLxuz3my3T6pEG0D3XyduSUqv6VnLTAKGvtp7E
begin 770 _W
0A7M/
~


See  for more information.

If you suspect that the result above is incorrect, try re-doing that job on the tests case report page.
Comment 4 by ochang@google.com on Fri, Jun 3, 2016, 7:22 PM EDT Project Member

more_vert
It looks like this is still reproducing. #3 seems like flake.
Comment 5 by ochang@google.com on Fri, Jun 24, 2016, 2:39 PM EDT Project Member

more_vert
Labels: Library-libarchive

Comment 6 by ClusterFuzz-External on Mon, Jun 27, 2016, 1:16 PM EDT Project Member

more_vert
ClusterFuzz has detected this testcase as flaky and is unable to reproduce it in the original crash revision. Skipping fixed testing check and marking it as potentially fixed.

Detailed report: https://clusterfuzz-external.appspot.com/testcase?key=6051005141614592

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
Download: https://clusterfuzz-external.appspot.com/download/AMIfv97UJ_XegpDWBsRbTqTw-2GXGnM9sFyyhbLgIpxY2I5jzNAiwJF8mF_cBinyVep976oB_sAB_UFxDc_pVduWNXhlHryizcDM7MctFvyTv_IRwGzOvsCkBGkK2xF-83gFeQsuAPS9cVpjOVLxuz3my3T6pEG0D3XyduSUqv6VnLTAKGvtp7E?testcase_id=6051005141614592
begin 770 _W
0A7M/
~


See  for more information.

If you suspect that the result above is incorrect, try re-doing that job on the tests case report page.
Comment 7 by ochang@google.com on Mon, Nov 7, 2016, 5:15 PM EST Project Member

more_vert
Status: Duplicate (was: New)
Mergedinto: 139

Comment 8 by ochang@google.com on Tue, Nov 29, 2016, 4:54 PM EST Project Member

more_vert
Labels: -Library-libarchive Project-libarchive

Comment 9 by ochang@google.com on Tue, Nov 29, 2016, 5:47 PM EST Project Member

more_vert
Labels: -Project-libarchive Proj-libarchive

Comment 10 by sheriffbot@chromium.org on Sun, Dec 11, 2016, 9:02 AM EST Project Member

more_vert
Labels: -restrict-view-commit

This bug has been fixed for 7 days. It has been opened to the public.

- Your friendly Sheriffbot
Comment 11 by ochang@google.com on Thu, Feb 23, 2017, 8:47 PM EST Project Member

more_vert
Labels: Engine-libfuzzer

Comment 12 by kcc@google.com on Thu, Mar 9, 2017, 4:53 PM EST Project Member

more_vert
Cc: -a_deleted_user palmer@google.com"""

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

See https://github.com/google/oss-fuzz/blob/master/docs/reproducing.md for more information.
Comment 1 by kcc@google.com on Tue, Nov 1, 2016, 11:17 AM EDT Project Member

more_vert
Cc: -a_deleted_user -a_deleted_user kcc@google.com philip.h...@gmail.com

Comment 2 by ClusterFuzz-External on Wed, Nov 2, 2016, 3:03 AM EDT Project Member

more_vert
ClusterFuzz has detected this issue as fixed in range 201611010925:201611012030.

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
Fixed: https://clusterfuzz-external.appspot.com/revisions?job=libfuzzer_asan_pcre2&range=201611010925:201611012030

Minimized Testcase (0.01 Kb): https://clusterfuzz-external.appspot.com/download/AMIfv94e2eucet3LDQplzG1u73sGldGgS5OJyDfv2uramuXF209jN8Ouy--5rjrrjmsStzerBsPvdYMW0Q4-HM-qvseSDZl1DEqVtGx8Ajwsuvt5Zcql9E42Jt_CACwxxvp0CTz4JeuLyfsdxJPcSop-TKtSb_PNT_X-ONwVEtErCSRsXlAdBg4?testcase_id=6544078783119360

See https://github.com/google/oss-fuzz/blob/master/docs/reproducing.md for more information.

If you suspect that the result above is incorrect, try re-doing that job on the tests case report page.
Comment 3 by ClusterFuzz-External on Wed, Nov 2, 2016, 4:24 AM EDT Project Member

more_vert
Status: Verified (was: New)
Labels: ClusterFuzz-Verified

ClusterFuzz testcase is verified as fixed, closing issue.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.
Comment 4 by ochang@google.com on Fri, Nov 4, 2016, 7:07 PM EDT Project Member

more_vert
Labels: -Restrict-View-Commit

Derestricting.
Comment 5 by ochang@google.com on Tue, Nov 29, 2016, 4:56 PM EST Project Member

more_vert
Labels: -Library-pcre2 Project-pcre2

Comment 6 by ochang@google.com on Tue, Nov 29, 2016, 5:53 PM EST Project Member

more_vert
Labels: -Project-pcre2 Proj-pcre2

Comment 7 by ochang@google.com on Thu, Feb 23, 2017, 8:47 PM EST Project Member

more_vert
Labels: Engine-libfuzzer"""

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
become visible to the public.
Comment 1 by ClusterFuzz-External on Sat, Aug 10, 2019, 10:24 AM EDT Project Member

more_vert
Status: Verified (was: New)
Labels: ClusterFuzz-Verified

ClusterFuzz testcase 5653813716844544 is verified as fixed in https://oss-fuzz.com/revisions?job=afl_asan_lz4&range=201908090234:201908100233

If this is incorrect, please file a bug on https://github.com/google/oss-fuzz/issues/new
Comment 2 by sheriffbot@chromium.org on Mon, Sep 9, 2019, 11:30 AM EDT Project Member

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
