from unittest import TestCase

from oss_fuzz_issue_parser.issue_parser import *
from tests.oss_fuzz_issue_parser.test_issue_parser_inputs import *


class TestIssueParser(TestCase):

    def test_get_issue_num(self):
        issue_num = get_issue_num(test_input_22076)
        assert issue_num == 22076

    def test_get_title(self):
        title = get_title(test_input_22076)
        assert title == 'llvm:clang-fuzzer: Stack-overflow in GetFullTypeForDeclarator'

    def test_get_proj(self):
        proj = get_project(test_input_22076, 22076)
        assert proj == 'llvm'

    def test_get_fuzzing_engine(self):
        fzeng = get_fuzzing_engine(test_input_22076, 22076)
        assert fzeng == 'libFuzzer'

    def test_get_fuzz_target_binary(self):
        fztgt_22076 = get_fuzz_target_binary(test_input_22076, 22076)
        assert fztgt_22076 == 'clang-fuzzer'
        fztgt_16307 = get_fuzz_target_binary(test_input_16307, 16307)
        assert fztgt_16307 == 'compress_fuzzer'

    def test_get_job_type(self):
        jobtype = get_job_type(test_input_22076)
        assert jobtype == 'libfuzzer_asan_llvm'

    def test_get_platform_id(self):
        platform = get_platform_id(test_input_22076)
        assert platform == 'linux'

    def test_get_crash_type(self):
        crashtype = get_crash_type(test_input_22076)
        assert crashtype == 'Stack-overflow'

    def test_get_crash_address(self):
        addr_16307 = get_crash_address(test_input_16307)
        assert addr_16307 == ''
        addr_22076 = get_crash_address(test_input_22076)
        assert addr_22076 == '0x7ffeb72c0f48'

    def test_get_crash_state(self):
        crashstate = get_crash_state(test_input_22076)
        assert crashstate == ('GetFullTypeForDeclarator', 'clang::Sema::GetTypeForDeclarator', 'clang::Sema::ActOnBlockArguments')

    def test_get_sanitizer(self):
        sanitizer = get_sanitizer(test_input_22076, 22076)
        assert sanitizer == 'address (ASAN)'

    def test_get_regressed_commits_url(self):
        regressed_5 = get_regressed_commits_url(test_input_5)
        assert regressed_5 is None
        regressed_22076 = get_regressed_commits_url(test_input_22076)
        assert regressed_22076 == 'https://oss-fuzz.com/revisions?job=libfuzzer_asan_llvm&range=202005030248:202005040645'

    def test_get_fixed_commits_url(self):
        fixed_5 = get_fixed_commits_url(test_input_5, 5)
        assert fixed_5 == 'https://clusterfuzz-external.appspot.com/revisions?job=libfuzzer_asan_libarchive&range=201605271439:201605271739'
        fixed_22076 = get_fixed_commits_url(test_input_22076, 22076)
        assert fixed_22076 == 'https://oss-fuzz.com/revisions?job=libfuzzer_asan_llvm&range=202005070415:202005080243'

    def test_get_testcase_url(self):
        tst_5 = get_testcase_url(test_input_5, 5)
        assert tst_5 == 'https://clusterfuzz-external.appspot.com/download/AMIfv97UJ_XegpDWBsRbTqTw-2GXGnM9sFyyhbLgIpxY2I5jzNAiwJF8mF_cBinyVep976oB_sAB_UFxDc_pVduWNXhlHryizcDM7MctFvyTv_IRwGzOvsCkBGkK2xF-83gFeQsuAPS9cVpjOVLxuz3my3T6pEG0D3XyduSUqv6VnLTAKGvtp7E'
        tst_126 = get_testcase_url(test_input_126, 126)
        assert tst_126 == 'https://clusterfuzz-external.appspot.com/download/AMIfv94e2eucet3LDQplzG1u73sGldGgS5OJyDfv2uramuXF209jN8Ouy--5rjrrjmsStzerBsPvdYMW0Q4-HM-qvseSDZl1DEqVtGx8Ajwsuvt5Zcql9E42Jt_CACwxxvp0CTz4JeuLyfsdxJPcSop-TKtSb_PNT_X-ONwVEtErCSRsXlAdBg4?testcase_id=6544078783119360'
        tst_22076 = get_testcase_url(test_input_22076, 22076)
        assert tst_22076 == 'https://oss-fuzz.com/download?testcase_id=5196721950031872'
