from unittest import TestCase

from issue.issue_scraper import IssueScraper
from oss_fuzz.oss_fuzz_bug_report_parser import *
from oss_fuzz.oss_fuzz_bug_report_parser import _get_project, _get_fuzzing_engine, _get_fuzz_target_binary, \
    _get_job_type, _get_platform_id, _get_crash_type, _get_crash_address, _get_crash_state, _get_sanitizer, \
    _get_regressed_commits_url, _get_fixed_commits_url, _get_testcase_url
from tests.oss_fuzz.oss_fuzz_bug_reports import *


class TestIssueParser(TestCase):

    def test_attach_oss_fuzz_bug_report(self):
        # smoke test
        scraper = IssueScraper()
        url_22076 = 'https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=22076'
        issue_22076 = scraper.scrape(url_22076) # bug report

        successful = attach_oss_fuzz_bug_report(issue_22076)
        self.assertTrue(successful)
        self.assertIsNotNone(issue_22076.oss_fuzz_bug_report)


    def test_is_oss_fuzz_bug_report(self):
        scraper = IssueScraper()
        url_22076 = 'https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=22076'
        issue_22076 = scraper.scrape(url_22076) # bug report

        url_25371 = 'https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=25371'
        issue_25371 = scraper.scrape(url_25371) # build failure

        url_projzero = 'https://bugs.chromium.org/p/project-zero/issues/detail?id=9&q=&can=1'
        issue_projzero = scraper.scrape(url_projzero)


        self.assertTrue(is_oss_fuzz_bug_report(issue_22076))
        self.assertFalse(is_oss_fuzz_bug_report(issue_25371))
        self.assertFalse(is_oss_fuzz_bug_report(issue_projzero))


    def test_parse_oss_fuzz_issue_details(self):
        scraper = IssueScraper()
        url_22076 = 'https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=22076'
        issue_22076 = scraper.scrape(url_22076)
        oss_fuzz_issue_details_22076 = parse_oss_fuzz_bug_report_details(issue_22076)
        self.assertEqual(oss_fuzz_issue_details_22076.project, 'llvm')
        self.assertEqual(oss_fuzz_issue_details_22076.fuzzing_engine, 'libFuzzer')
        self.assertEqual(oss_fuzz_issue_details_22076.fuzz_target_binary, 'clang-fuzzer')
        self.assertEqual(oss_fuzz_issue_details_22076.job_type, 'libfuzzer_asan_llvm')
        self.assertEqual(oss_fuzz_issue_details_22076.platform_id, 'linux')
        self.assertEqual(oss_fuzz_issue_details_22076.crash_type, 'Stack-overflow')
        self.assertEqual(oss_fuzz_issue_details_22076.crash_addr, '0x7ffeb72c0f48')
        self.assertEqual(oss_fuzz_issue_details_22076.crash_state, ('GetFullTypeForDeclarator',
                                                                    'clang::Sema::GetTypeForDeclarator',
                                                                    'clang::Sema::ActOnBlockArguments'))
        self.assertEqual(oss_fuzz_issue_details_22076.sanitizer, 'address (ASAN)')
        self.assertEqual(oss_fuzz_issue_details_22076.regressed_commits_url,
                         'https://oss-fuzz.com/revisions?job=libfuzzer_asan_llvm&range=202005030248:202005040645')
        self.assertEqual(oss_fuzz_issue_details_22076.fixed_commits_url,
                         'https://oss-fuzz.com/revisions?job=libfuzzer_asan_llvm&range=202005070415:202005080243')
        self.assertEqual(oss_fuzz_issue_details_22076.testcase_url,
                         'https://oss-fuzz.com/download?testcase_id=5196721950031872')

    def test_get_proj(self):
        proj_5 = _get_project(test_input_5, 5)
        self.assertEqual(proj_5, 'libarchive')
        proj_22076 = _get_project(test_input_22076, 22076)
        self.assertEqual(proj_22076, 'llvm')

    def test_get_fuzzing_engine(self):
        fzeng_5 = _get_fuzzing_engine(test_input_5, 5)
        self.assertEqual(fzeng_5, 'libFuzzer')
        fzeng_16307 = _get_fuzzing_engine(test_input_16307, 16307)
        self.assertEqual(fzeng_16307, 'afl')
        fzeng_22076 = _get_fuzzing_engine(test_input_22076, 22076)
        self.assertEqual(fzeng_22076, 'libFuzzer')


    def test_get_fuzz_target_binary(self):
        fztgt_5 = _get_fuzz_target_binary(test_input_5, 5)
        self.assertEqual(fztgt_5, 'libarchive_fuzzer')
        fztgt_16307 = _get_fuzz_target_binary(test_input_16307, 16307)
        self.assertEqual(fztgt_16307, 'compress_fuzzer')
        fztgt_22076 = _get_fuzz_target_binary(test_input_22076, 22076)
        self.assertEqual(fztgt_22076, 'clang-fuzzer')

    def test_get_job_type(self):
        jobtype = _get_job_type(test_input_22076)
        assert jobtype == 'libfuzzer_asan_llvm'

    def test_get_platform_id(self):
        platform = _get_platform_id(test_input_22076)
        assert platform == 'linux'

    def test_get_crash_type(self):
        crashtype = _get_crash_type(test_input_22076)
        assert crashtype == 'Stack-overflow'

    def test_get_crash_address(self):
        addr_16307 = _get_crash_address(test_input_16307)
        assert addr_16307 == ''
        addr_22076 = _get_crash_address(test_input_22076)
        assert addr_22076 == '0x7ffeb72c0f48'

    def test_get_crash_state(self):
        crashstate_19429 = _get_crash_state(test_input_19429)
        self.assertEqual(crashstate_19429, ('NULL',))
        crashstate_22076 = _get_crash_state(test_input_22076)
        self.assertEqual(crashstate_22076,
                         ('GetFullTypeForDeclarator', 'clang::Sema::GetTypeForDeclarator', 'clang::Sema::ActOnBlockArguments'))

    def test_get_sanitizer(self):
        sanitizer_5 = _get_sanitizer(test_input_5, 5)
        self.assertEqual(sanitizer_5, 'address (ASAN)')
        sanitizer_22076 = _get_sanitizer(test_input_22076, 22076)
        self.assertEqual(sanitizer_22076, 'address (ASAN)')

    def test_get_regressed_commits_url(self):
        regressed_5 = _get_regressed_commits_url(test_input_5)
        self.assertIsNone(regressed_5)
        regressed_22076 = _get_regressed_commits_url(test_input_22076)
        self.assertEqual(regressed_22076, 'https://oss-fuzz.com/revisions?job=libfuzzer_asan_llvm&range=202005030248:202005040645')
        regressed_24163 = _get_regressed_commits_url(test_input_24163)
        self.assertEqual(regressed_24163, 'https://oss-fuzz.com/revisions?job=libfuzzer_asan_i386_libevt&revision=202007150438')

    def test_get_fixed_commits_url(self):
        scraper = IssueScraper()
        url_5 = 'https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=5'
        issue_5 = scraper.scrape(url_5)
        comments_5 = issue_5.comments
        fixed_5 = _get_fixed_commits_url(comments_5, 5)
        assert fixed_5 == 'https://clusterfuzz-external.appspot.com/revisions?job=libfuzzer_asan_libarchive&range=201605271439:201605271739'

        url_22076 = 'https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=22076'
        issue_22076 = scraper.scrape(url_22076)
        comments_22076 = issue_22076.comments
        fixed_22076 = _get_fixed_commits_url(comments_22076, 22076)
        assert fixed_22076 == 'https://oss-fuzz.com/revisions?job=libfuzzer_asan_llvm&range=202005070415:202005080243'

    def test_get_testcase_url(self):
        tst_5 = _get_testcase_url(test_input_5, 5)
        assert tst_5 == 'https://clusterfuzz-external.appspot.com/download/AMIfv97UJ_XegpDWBsRbTqTw-2GXGnM9sFyyhbLgIpxY2I5jzNAiwJF8mF_cBinyVep976oB_sAB_UFxDc_pVduWNXhlHryizcDM7MctFvyTv_IRwGzOvsCkBGkK2xF-83gFeQsuAPS9cVpjOVLxuz3my3T6pEG0D3XyduSUqv6VnLTAKGvtp7E'
        tst_126 = _get_testcase_url(test_input_126, 126)
        assert tst_126 == 'https://clusterfuzz-external.appspot.com/download/AMIfv94e2eucet3LDQplzG1u73sGldGgS5OJyDfv2uramuXF209jN8Ouy--5rjrrjmsStzerBsPvdYMW0Q4-HM-qvseSDZl1DEqVtGx8Ajwsuvt5Zcql9E42Jt_CACwxxvp0CTz4JeuLyfsdxJPcSop-TKtSb_PNT_X-ONwVEtErCSRsXlAdBg4?testcase_id=6544078783119360'
        tst_22076 = _get_testcase_url(test_input_22076, 22076)
        assert tst_22076 == 'https://oss-fuzz.com/download?testcase_id=5196721950031872'
